# Karat API SDK

This repository is an example Python SDK for using the Karat API. It leverages the Python `gql` library,
which can be found here: [gql GitHub repository](https://github.com/graphql-python/gql).

Refer to `examples.py` for code samples demonstrating how to instantiate and use the SDK.

Other GraphQL libraries exist for Python, and for other languages. This repository is intended to be a
starting point and set of examples for your own implementation, rather than an exhaustive client in its own right.

## Karat API documentation

For full documentation of the Karat API see the following resources:

* [Overview](https://karat.slab.com/posts/karat-api-overview-6l4gprc3)
* [Documentation](https://karat.slab.com/posts/karat-api-documentation-dezzam7y)

# Installation

To set up the SDK in a Python virtual environment, run the following commands:

```bash
$ python -m venv .venv
$ source ./.venv/bin/activate
$ pip install -r requirements.txt
$ TOKEN=your-token-here ENVIRONMENT=[production/test/development] SUBDOMAIN=your-subdomain-here python examples.py
```

# Examples

Several examples are provided in the `examples.py` script. You can run it standalone as shown above. Key points to note:

* **Queries**: The script includes working examples of queries, such as retrieving the first of your groups. These are generic and should work for any user.
* **Mutations**: The mutations provided may fail unless you supply specific IDs for entities like Candidacies or Roles You can retrieve your own IDs for the relevant mutations by running queries and update the calls.

Copyright © 2024 Karat Inc.
