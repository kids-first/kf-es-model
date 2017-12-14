# Kids First Elasticsearch Model

Elasticsearch mappings/settings are generated programmatically and archived under `generated-es-model-archive`.

To create ES index for `file-centric` with the latest version of mapping/settings, simply do this:
```
curl -XPUT -H 'Content-Type: application/json' "localhost:9200/file-centric" -d @generated-es-model-archive/kf-es-model-latest/file-centric.mapping.json
```

