from src.client import client
from pprint import pprint
import os

if 'TOKEN' not in os.environ or 'SUBDOMAIN' not in os.environ:
  print('No token found. Please run this script as `TOKEN=your-token-here ENVIRONMENT=[production/staging/development] SUBDOMAIN=your-subdomain-here python examples.py`')
  exit()

print('\n------ Instantiating a client\n')

kc = client.KaratClient(
  token=os.environ['TOKEN'],
  environment=os.environ.get('ENVIRONMENT'),
  subdomain=os.environ.get('SUBDOMAIN')
)

print('\n------ Listing available operations\n')

print('Available mutations:', kc.mutations())
print('Available queries:', kc.queries())

print('\n------ Getting an operation and reporting what it expects\n')

print('Args for \'users\' query:')
user_query = kc.query('users')
print('All:', user_query.possible_args())
print('Mandatory:', user_query.mandatory_args())

print()

print('Args for \'invite\' mutation:')
invite_mutation = kc.mutation('invite')
print('All:', invite_mutation.possible_args())
print('Mandatory:', invite_mutation.mandatory_args())

print('\n------ Fluent querying\n')

print('Getting users:')
result = kc.query('users').set_param('clientUserType', 'ADMIN').set_params({'disabled': False, 'first': 1}).execute()
pprint(result)

print()

print('\n------ non-fluent querying\n')

print('Getting groups:')
group_query = kc.query('groups')
group_query.set_param('first', 1)
result2 = group_query.execute()
pprint(result2)

print('\n------ fluent mutations\n')

print('Sending an invite (This will fail due to missing arguments!):')

invite_mutation = kc.mutation('invite')
invite_mutation.set_param('email', 'user@example.com')

try:
  result2 = invite_mutation.execute()
except Exception as ex:
  print(f'Exception received! {ex}')

print('\n------ non-fluent mutations\n')

print('Sending disposition (This will fail for a variety of reasons!):')
disposition_mutation = kc.mutation('disposition')

try:
  # This method isn't available for disposition mutations, and is reported via exception:
  disposition_mutation.set_param('email', 'user@example.com')
except Exception as ex:
  print(f'Exception received! {ex}')

# Now we know which method to use instead!

disposition_mutation.add_outcome('DECLINED_AT_ONSITE_INTERVIEW', ['1', '24'])
disposition_mutation.add_outcome('OFFER_ACCEPTED', ['153', '123'])
disposition_mutation.add_outcome('OFFER_ACCEPTED', '17') # can accept either lists or individual IDs
try:
  disposition_mutation.execute()
except Exception as ex:
  print(f'Exception received (likely invalid permissions): {ex}')
