from datapackage_pipelines_plus_plus.base_processors.add_resource import AddResourceBaseProcessor


DEFAULT_COMMIT_EVERY = 1000


class Processor(AddResourceBaseProcessor):

    def _get_schema(self, resource_descriptor):
        schema = self._parameters["schema"]
        fields = []
        for field_name, field_type in schema["fields"].items():
            field = {"name": field_name}
            if field_type in ["number", "integer", "string"]:
                field["type"] = field_type
            else:
                field["value_format"] = field_type
                field["type"] = "string"
                field["es:type"] = "keyword"
            fields.append(field)
        schema["fields"] = fields
        return schema

    def _get_new_resource(self):
        for i in range(self._parameters["num-rows"]):
            j = int(i/self._parameters["num-rows"]*100)
            row = {}
            for field in self._schema["fields"]:
                if "value_format" in field:
                    row[field["name"]] = field["value_format"].format(i=i, j=j)
                elif field["type"] == "number":
                    row[field["name"]] = float(i) + float(i/200)
                elif field["type"] == "integer":
                    row[field["name"]] = i
                else:
                    row[field["name"]] = "{}_{}".format(field["name"], i)
            yield row


if __name__ == '__main__':
    Processor.main()
