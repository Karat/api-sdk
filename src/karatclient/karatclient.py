from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from gql.transport.exceptions import TransportServerError
from .queries import UserQuery, GroupQuery, RoleQuery
from .mutations import InviteMutation, DispositionMutation
from .exceptions import UnknownQueryError, UnknownEnvironmentError
from .setup_logging import get_logger

log = get_logger(__name__)

envs = {
    'production': {'url': 'https://{}.karat.io/api/v1/graphql'},
    'test': {'url': 'https://{}.cotrain.io/api/v1/graphql'},
    'development': {'url': 'http://{}.localtest.me:3000/api/v1/graphql'},
}

QUERIES = {
  'users': UserQuery,
  'groups': GroupQuery,
  'roles': RoleQuery
}
MUTATIONS = {
  'invite': InviteMutation,
  'disposition': DispositionMutation
}

class KaratClient:
  def __init__(self, **kwargs):
    self.token = kwargs.get('token')
    environment = kwargs.get('environment') or 'development'
    subdomain = kwargs.get('subdomain')
    log.info(f'Environment is {environment}, subdomain is {subdomain}')

    # We'll mark the client as usable after setup is complete. If setup doesn't
    # complete, any subsequent attempts to use Operations will throw an exception.

    self.usable = False

    if environment not in envs:
      raise UnknownEnvironmentError(f'Unknown environment: {environment}')
    url = envs[environment]['url']

    # The API 
    self.transport = RequestsHTTPTransport(
      url=url.format(subdomain),
      headers={'Authorization': f'Bearer {self.token}'}
    )

    try:
      self.client = Client(transport=self.transport, fetch_schema_from_transport=True)

      # Test to ensure we can call the endpoint
      log.info(f'Authorized as {self.whoami()}')

      # Mark this client as usable
      self.usable = True
    except TransportServerError as error:
      self.reason = f'Unable to retrieve initial query: {error}'

  def execute(self, query, params=None):
    # We can add any generic error handling etc. here
    result = self.client.execute(query, variable_values=params)
    return result

  def queries(self):
    return list(QUERIES.keys())

  def query(self, query_name):
    if query_name in QUERIES:
      return QUERIES[query_name](self)

    raise UnknownQueryError()

  def mutations(self):
    return list(MUTATIONS.keys())

  def mutation(self, query_name):
    if query_name in MUTATIONS:
      return MUTATIONS[query_name](self)

    raise UnknownQueryError()

  def whoami(self):
    result = self.execute(gql('{ me { name }}'))
    actor = result['me']['name']
    return actor
