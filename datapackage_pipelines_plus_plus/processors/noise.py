from datapackage_pipelines_plus_plus.base_processors.add_resource import AddResourceBaseProcessor


DEFAULT_COMMIT_EVERY = 1000


class Processor(AddResourceBaseProcessor):

    def _get_schema(self, resource_descriptor):
        schema = self._parameters["schema"]
        schema["fields"] = [{"name": field_name, "type": field_type}
                            for field_name, field_type
                            in schema["fields"].items()]
        return schema

    def _get_resource(self):
        for i in range(self._parameters["num-rows"]):
            row = {}
            for field in self._schema["fields"]:
                if field["type"] == "number":
                    row[field["name"]] = float(i) + float(i/200)
                elif field["type"] == "integer":
                    row[field["name"]] = i
                else:
                    row[field["name"]] = "{}_{}".format(field["name"], i)
            yield row


if __name__ == '__main__':
    Processor.main()
