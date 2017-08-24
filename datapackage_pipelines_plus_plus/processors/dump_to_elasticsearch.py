from datapackage_pipelines_plus_plus.base_processors.base_dump import BaseDumpProcessor
from elasticsearch import NotFoundError, helpers
import logging


class Processor(BaseDumpProcessor):

    def _get_mappings(self):
        mappings = {}
        for field in self._schema["fields"]:
            name = field["name"]
            type = field["type"]
            mapping = None
            if field.get("es:type"):
                mapping = {"type": field["es:type"]}
            elif name in self._update_keys:
                mapping = {"type": "keyword"}
            elif type == "string":
                mapping = {"type": "text"}
            elif type == "integer":
                mapping = {"type": "long"}
            elif type == "number":
                mapping = {"type": "double"}
            if not mapping:
                raise Exception()
            mappings[name] = mapping
        return mappings

    def _create_index(self):
        level = logging.getLogger().level
        logging.getLogger().setLevel(logging.ERROR)
        self.elasticsearch.indices.create(self._index_name,
                                          body={"mappings": {"data": {"properties": self._get_mappings()}}})
        self.elasticsearch.indices.refresh(index=self._index_name)
        logging.getLogger().setLevel(level)
        logging.info("index created: {}".format(self._index_name))

    def _get_row_id(self, row):
        if len(self._update_keys) == 1:
            return row[self._update_keys[0]]
        else:
            return "_".join([row[k] for k in self._update_keys])

    def _commit(self, rows):
        actions = [{"_index": self._index_name,
                    "_type": "data",
                    "_id": self._get_row_id(row),
                    "_source": row} for row in rows]
        level = logging.getLogger().level
        logging.getLogger().setLevel(logging.ERROR)
        success, errors = helpers.bulk(self.elasticsearch, actions)
        logging.getLogger().setLevel(level)
        if not success:
            logging.info(errors)
            raise Exception("encountered errors while bulk inserting to elasticsearch")
        self._incr_stat("indexed docs", len(actions))
        logging.info("{}: commit ({} indexed)".format(self._log_prefix, self._get_stat("indexed docs")))

    def _filter_resource(self, resource_number, resource_data):
        self._update_keys = self._schema["primaryKey"]
        if not self._update_keys or len(self._update_keys) == 0:
            raise Exception("dump requires a primaryKey")
        self._index_name = self._parameters["index-name"]
        if self._parameters.get("drop-index"):
            try:
                self.elasticsearch.indices.delete(self._index_name)
            except NotFoundError:
                pass
        else:
            raise Exception("updating existing index is not supported")
        self._create_index()
        yield from super(Processor, self)._filter_resource(resource_number, resource_data)

    @property
    def _log_prefix(self):
        return self._index_name


if __name__ == "__main__":
    Processor.main()
