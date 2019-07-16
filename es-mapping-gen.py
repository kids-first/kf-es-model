#!/usr/bin/env python

import os
import json
import yaml
import requests
from shutil import copyfile


def expand_es_mapping(mapping, source_models, mapper):
    next_mappings = {}
    config = {}
    for k, v in mapping.items():
        if k == 'properties':
            next_mappings = v
        else:
            config[k] = v

    for next_mapping in next_mappings:  # recursion
        expand_es_mapping(next_mappings[next_mapping], source_models, mapper)

    # add new properties
    if config.get('source'):
        source_model = source_models.get(config.get('source'), {}).get('properties', {})
        exclude_list = config.get('exclude')

        for p in source_model:
            if p in exclude_list:
                continue
            source_property = source_model.get(p)
            source_type = source_property.get('type')
            source_format = 'format:%s' % source_property.get('format') \
                if source_property.get('format') else 'format:null'

            es_type = mapper.get('field_type_map').get(source_type, {}).get(source_format)
            if es_type and p not in next_mappings:  # do NOT overwrite manually defined existing mapping type
                next_mappings.update({p: es_type})

        mapping.pop('source', None)
        mapping.pop('exclude', None)


class SchemaGenerator(object):
    def __init__(self, mapper_file):
        self._read_mapper(mapper_file)
        self._source_models = {}
        self._target_models = {}
        self._get_sources()
        #print json.dumps(self._source_models, indent=2)

    @property
    def mapper(self):
        return self._mapper

    @property
    def source_models(self):
        return self._source_models

    @property
    def source_model_version(self):
        return self._source_model_version

    def _read_mapper(self, mapper_file):
        with open(mapper_file, 'r') as m:
            self._mapper = yaml.load(m)

    def _get_sources(self):
        # we only have one source now, the follow code needs update when new
        # source schema is added (not sure will have or not)
        for source in self._mapper['sources']:
            if not source.get('api_endpoint'):
                continue

            api_endpoint = source['api_endpoint']
            source_name = source['name']

            try:
                json_str = requests.get(api_endpoint).text
                kf_source = json.loads(json_str)
                if not os.path.exists('cache'):
                    os.makedirs('cache')
                with open('cache/%s.json' % source_name, 'w') as f:
                    f.write(json.dumps(kf_source, indent=2))
            except:  # offline mode use cached dictionary
                with open('cache/%s.json' % source_name, 'r') as f:
                    kf_source = json.load(f)

            if source_name == 'kf-api-dataservice':
                self._source_models.update(kf_source.get('definitions'))
                self._source_model_version = kf_source.get('info', {}).get('version')

    def generate_mappings(self):
        target_version = self.mapper.get('target-mappings').get('version')
        mappings = self.mapper.get('target-mappings').get('mappings')
        settings = self.mapper.get('target-mappings').get('settings')

        for mapping_name in mappings:
            mapping = mappings[mapping_name]
            expand_es_mapping(mapping, self.source_models, self.mapper)

            # add meta in mapping
            mapping.update({
                "_meta": {
                    "kf-dataservice-version": self.source_model_version
                }
            })
            export_dir = os.path.join('es-model-latest')
            if not os.path.exists(export_dir):
                os.makedirs(export_dir)
            export_file = os.path.join(export_dir, '%s.mapping.json' % mapping_name)
            with open(export_file, 'w') as f:
                f.write(json.dumps(
                        {"mappings": {mapping_name: mapping}, "settings": settings},
                        indent=2,
                        sort_keys=True))

            archive_dir = os.path.join('es-model-archive',
                'kf-es-model-v%s_%s' % (target_version, self.source_model_version))
            if not os.path.exists(archive_dir):
                os.makedirs(archive_dir)

            copyfile(export_file, os.path.join(archive_dir, '%s.mapping.json' % mapping_name))


if __name__ == '__main__':
    sg = SchemaGenerator("es_mapper.yaml")
    sg.generate_mappings()
