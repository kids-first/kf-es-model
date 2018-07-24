# Feature Name: KFDRP Index Naming Schema

## Summary
[summary]: #summary

The Kids First Data Portal will need a service to manage which indices are
made available for display, faceted and text based search, and data exploration.

In order for these indices to be managed in a way that allows for growth and
consistency, there is a need for a schema for the naming convention to these
indices.

## Motivation
[motivation]: #motivation

As the Kids First Data Resource Portal (DRP) grows in terms of the data size
searchable through it, there will be an ever increasing number of elasticsearch
indices that are in use at any given time.

It had been established, given the need for many studies to have their data
indexed, supporting updated of only a few studies of a time, we had decided to
shard the domain by creating an index per study per entity type.

As the number of studies and entities being tracked by the portal grows the
number of indices being used will grow in terms of `#studies * #entities` and
if we take into account the possibility of using indices with different purposes
such as centric for faceted search and text indices for text search then we have
potential growth of `#studies * #entities * #types`. The management of the
publishing of different indices through the maniuplation of aliases will become
a large and important task that will be greately aided through the establishment
of a schema for the naming of an elasticsearch index.

- [Elasticsearch](https://www.elastic.co/products/elasticsearch)

## Detailed design
[design]: #detailed-design

The schema for index naming in terms of a Context-Free Grammar is as follows:

```
index_name --> <entity>_<index_type>_<shard_prefix>_<shard_id>_<release_id>

<entity> --> "^[a-z]*$"
<index_type> --> centric | text | entity
<shard_prefix> --> "^[a-z]{0,2}$"
<shard_id> --> "^[a-zA-Z0-9]*$"
<release_id> --> "^[a-zA-Z0-9]*$"

```

## Drawbacks
[drawbacks]: #drawbacks

The primary drawback is if a need arises to generate versioned indices that
are feature specific and do not conform to the enitity/shard design, our schema
will be unable to describe these indicies.

## Alternatives
[alternatives]: #alternatives

The use of a schema is simply an aid and to help maintain the source of truth
on what an index describes with the data itself. An alternative will be to build
a service that tracks the metadata about releases and studies to act as a source of truth for which index pertains to a particular dataset or usecase.


## Unresolved questions
[unresolved]: #unresolved-questions

TODO
