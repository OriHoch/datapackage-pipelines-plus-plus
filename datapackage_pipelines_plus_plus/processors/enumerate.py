from datapackage_pipelines_plus_plus.base_processors.filter_resource import FilterResourceBaseProcessor


DEFAULT_COMMIT_EVERY = 1000


class Processor(FilterResourceBaseProcessor):

    def _filter_resource_descriptor(self, resource_descriptor):
        self._i = 0
        self._field = self._parameters.get("field")
        descriptor = super(Processor, self)._filter_resource_descriptor(resource_descriptor)
        descriptor["schema"]["fields"].append({"name": self._field, "type": "integer"})
        if self._parameters.get("primary-key"):
            descriptor["schema"]["primaryKey"] = [self._field]
        return descriptor

    def _filter_row(self, row):
        for row in super(Processor, self)._filter_row(row):
            row[self._field] = self._i
            yield row
            self._i += 1



if __name__ == '__main__':
    Processor.main()
