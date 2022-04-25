# api-sdk

An example Python SDK for using the Karat API. It relies on the Python `gql` library, which can be found at https://github.com/graphql-python/gql

Please see `examples.py` for a selection of code samples, showing how to instantiate and use the SDK.

Other GraphQL libraries exist for Python, and for other languages. This is intended to be a starting point and set of examples for your own implementation, rather than an exhaustive client in its own right.

# API Documentation

The documentation for this API can be found at https://karat.slab.com/posts/karat-api-documentation-3aua4q64

Comprehensive documentation for GraphQL can be found at https://graphql.org/learn/

# Installation

Using a Python virtual environment:

```bash
$ python -m venv .venv
$ source ./.venv/bin/activate
$ pip install -r requirements.txt
$ TOKEN=your-token-here ENVIRONMENT=[production/test/development] SUBDOMAIN=your-subdomain-here python examples.py
```

# Examples

There are several examples provided as part of the `examples.py` script, which can be run standalone as shown above. Several things to note:

* Working examples of queries are included, as 'retrieve the first of my groups' and similar operations are generic - everyone will be able to execute those.
* For the mutations demonstrated, it is expected that these calls will fail, as they require specific IDs (for Candidacies or Roles respectively). You can retrieve your own IDs for the relevant mutations by running queries and update the calls.

# TODO
- Add postprocessing to most queries and mutations
- Add tests