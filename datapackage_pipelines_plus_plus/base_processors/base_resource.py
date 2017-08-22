from datapackage_pipelines_plus_plus.base_processors.base import BaseProcessor


class BaseResourceProcessor(BaseProcessor):
    """Base class for processing a single resource"""

    def __init__(self, *args, **kwargs):
        super(BaseResourceProcessor, self).__init__(*args, **kwargs)
        self._resource_descriptor, self._resource_number = None, None

    def _filter_resource_descriptor(self, resource_descriptor):
        self._schema = self._get_schema(resource_descriptor)
        resource_descriptor =  dict(resource_descriptor, **{"name": self._get_output_resource_name(),
                                                            "path": self._get_output_resource_path(),
                                                            "schema": self._schema})
        self._resource_descriptor = resource_descriptor
        return resource_descriptor

    def _get_schema(self, resource_descriptor):
        return resource_descriptor.get("schema", {"fields": []})

    def _get_output_resource_name(self):
        return self._parameters.get("resource")

    def _get_output_resource_path(self):
        return "data/{}.csv".format(self._get_output_resource_name())

    def _is_matching_resource_number(self, resource_number):
        return resource_number == self._resource_number

    def _filter_resources(self, resources):
        for resource_number, resource_data in enumerate(resources):
            if self._is_matching_resource_number(resource_number):
                yield self._filter_resource(resource_data)
            else:
                yield resource_data

    def _filter_resource(self, resource_data):
        for row in resource_data:
            yield from self._filter_row(row)

    def _filter_row(self, row):
        yield {field_name: self._filter_row_value(field_name, value)
               for field_name, value in row.items()}

    def _filter_row_value(self, field_name, value):
        return value
