from datapackage_pipelines_plus_plus.base_processors.base_resource import BaseResourceProcessor
from itertools import chain


class FilterResourceBaseProcessor(BaseResourceProcessor):

    def _process(self, datapackage, resources):
        for resource_number, resource_descriptor in enumerate(datapackage["resources"]):
            if self._is_input_resource(resource_descriptor):
                self._resource_number = resource_number
                datapackage["resources"][self._resource_number] = self._filter_resource_descriptor(resource_descriptor)
        return datapackage, self._filter_resources(resources)

    def _get_input_resource_name(self):
        return self._get_output_resource_name()

    def _is_input_resource(self, resource_descriptor):
        return resource_descriptor["name"] == self._get_input_resource_name()

    def _get_output_resource_name(self):
        return self._parameters.get("resource")
