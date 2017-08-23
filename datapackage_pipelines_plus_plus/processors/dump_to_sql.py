from datapackage_pipelines_plus_plus.base_processors.base_dump import BaseDumpProcessor
from jsontableschema_sql.mappers import descriptor_to_columns_and_constraints
from sqlalchemy import Table
import logging
from sqlalchemy.orm import mapper


DEFAULT_COMMIT_EVERY = 1000


class Processor(BaseDumpProcessor):

    def __init__(self, *args, **kwargs):
        super(Processor, self).__init__(*args, **kwargs)
        self._db_table = None

    @property
    def db_table(self):
        if self._db_table is None:
            self._db_table = self.db_meta.tables.get(self._tablename)
            if self._db_table is None:
                columns, constraints, indexes = self._descriptor_to_columns_and_constraints("", self._tablename, self._schema,
                                                                                            (), None)
                self._db_table = Table(self._tablename, self.db_meta, *(columns + constraints + indexes))
                self._db_table.create()
                self._set_stat("created table", True)
                logging.info("table created: {}".format(self._tablename))
        return self._db_table

    def _descriptor_to_columns_and_constraints(self, *args):
        return descriptor_to_columns_and_constraints(*args)

    def _get_mapper(self):
        class Model(object):
            pass
        mapper(Model, self.db_table)
        return Model

    def _commit(self, rows):
        self.db_connect(retry=True)
        mapper = self._get_mapper()
        update_rows = []
        insert_rows = []
        for row in rows:
            filter_args = (getattr(self.db_table.c, field)==row[field] for field in self._update_keys)
            if self.db_session.query(self.db_table).filter(*filter_args).count() > 0:
                update_rows.append(row)
            else:
                insert_rows.append(row)
        if len(insert_rows) > 0:
            self.db_session.bulk_insert_mappings(mapper, insert_rows)
            self._incr_stat("inserted rows", len(insert_rows))
        if len(update_rows) > 0:
            if self._get_stat("created table"):
                logging.info(update_rows[-1])
                raise Exception("table was just created, how come we are updating rows!?!?!")
            self.db_session.bulk_update_mappings(mapper, update_rows)
            self._incr_stat("updated rows", len(update_rows))
        self.db_commit()
        logging.info("{}: commit ({} updated, {} inserted)".format(self._log_prefix,
                                                                   self._get_stat("updated rows", 0),
                                                                   self._get_stat("inserted rows", 0)))
        # force a new session on next commit
        self._db_session = None

    def _filter_resource(self, resource_data):
        self._update_keys = self._schema["primaryKey"]
        if not self._update_keys or len(self._update_keys) == 0:
            raise Exception("dump requires a primaryKey")
        self._tablename = self._parameters["table"]
        self.db_connect()
        table = self.db_meta.tables.get(self._tablename)
        if table is not None and self._parameters.get("drop-table"):
            table.drop()
            self._db_session = None
            self._db_meta = None
            self._set_stat("dropped table", True)
            logging.info("table dropped: {}".format(self._tablename))
        yield from super(Processor, self)._filter_resource(resource_data)

    @property
    def _log_prefix(self):
        return self._tablename


if __name__ == '__main__':
    Processor.main()
