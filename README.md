# Kids First Elasticsearch Model

Information and setting for ES mapping generation are configured in `es_mapper.yaml`. Elasticsearch mappings/settings can then be generated programmatically with this command:
```
python es-mapping-gen.py
```

To create ES index for `file_centric` with the latest version of mapping/settings, simply do this:
```
curl -XPUT -H 'Content-Type: application/json' "localhost:9200/file_centric" -d @es-model-latest/file_centric.mapping.json
```
