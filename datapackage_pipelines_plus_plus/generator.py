from datapackage_pipelines.generators import GeneratorBase
import os, yaml


class Generator(GeneratorBase):

    @classmethod
    def get_schema(cls):
        return {
            "$schema": "http://json-schema.org/draft-04/schema#",
            "type": "object"
        }

    @classmethod
    def generate_pipeline(cls, source):
        override_filename = "plus_plus.source-spec.override.yaml"
        override_pipelines = {}
        if os.path.exists(override_filename):
            with open("plus_plus.source-spec.override.yaml") as f:
                override_pipelines = yaml.load(f)
        for pipeline_id, pipeline_details in source.items():
            override_pipeline = override_pipelines.get(pipeline_id)
            if override_pipeline:
                pipeline_steps = pipeline_details.get("pipeline")
                if not pipeline_steps:
                    pipeline_steps = []
                override_steps = override_pipeline.get("pipeline")
                if not override_steps:
                    override_steps = []
                delete_steps = []
                for override_step in override_steps:
                    for i, pipeline_step in enumerate(pipeline_steps):
                        override_match = True
                        if "run" in override_step and override_step["run"] != pipeline_step["run"]:
                            override_match = False
                        if override_match:
                            if override_step.get("disable"):
                                delete_steps.append(i)
                pipeline_details["pipeline"] = [step for i, step in enumerate(pipeline_steps) if i not in delete_steps]
            yield pipeline_id, pipeline_details
