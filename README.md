# Kids First Elasticsearch Model

Elasticsearch mappings/settings are generated programmatically and archived under `generated-es-model-archive`.

To create ES index with specific versioned mapping/settings, simply do this:
```
curl -XPUT -H 'Content-Type: application/json' "localhost:9200/file-centric" -d @generated-es-model-archive/kf-es-model-v0.0.2/file-centric.mapping.json
```

