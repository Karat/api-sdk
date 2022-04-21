# api-sdk

An example Python SDK for using the Karat API. It relies on the Python `gql` library, which can be found at https://github.com/graphql-python/gql

Please see `examples.py` for a selection of code samples, showing how to instantiate and use the SDK.

# Installation
```bash
$ python -m venv .venv
$ source ./.venv/bin/activate
$ pip install -r requirements.txt
$ TOKEN=your-token-here ENVIRONMENT=[production/staging/development] SUBDOMAIN=your-subdomain-here python examples.py
```

# TODO
- Add postprocessing to most queries and mutations
- Add tests