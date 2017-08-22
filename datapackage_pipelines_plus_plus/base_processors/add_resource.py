from datapackage_pipelines_plus_plus.base_processors.base_resource import BaseResourceProcessor
from itertools import chain


class AddResourceBaseProcessor(BaseResourceProcessor):

    def _process(self, datapackage, resources):
        self._resource_number = len(datapackage["resources"])
        datapackage["resources"].append(self._filter_resource_descriptor(self._get_resource_descriptor()))
        return datapackage, chain(resources, self._filter_resources([self._get_resource()]))

    def _get_resource_descriptor(self):
        # you can use this to add attributes (other then schema / path / name - which are added automatically)
        return {}

    def _get_resource(self):
        # should yield the new resource rows
        # the rows will be processed further via the standard filter_resources / filter_resource / filter_ros methods
        yield from []
