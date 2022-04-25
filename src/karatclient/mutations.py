from gql import gql
from .operation import Operation
from .exceptions import InvalidOperationError, MissingMandatoryParameterError

class InviteMutation(Operation):
  """ A simple mutation that accepts standard parameters and creates an invitation
  """

  args = [
    "name",
    "email",
    "roleId",
    "phone",
    "atsUrl",
    "resume",
    "githubUrl",
    "linkedinUrl"
  ]

  mandatory_parameters = set(["name", "email", "roleId"])

  query = gql("""
    mutation CreateInvitation(
      $name: String!
      $email: String!
      $roleId: ID!
      $phone: String
      $atsUrl: String
      $resume: String
      $githubUrl: String
      $linkedinUrl: String
    ) {
      createInvitation (
        input: {
          name: $name
          email: $email
          roleId: $roleId
          phone: $phone
          atsUrl: $atsUrl
          resume: $resume
          githubUrl: $githubUrl
          linkedinUrl: $linkedinUrl
        }
      )
      {
      assessment {
        id
      }
      errors {
          message
      }
      }
    }
  """)

class DispositionMutation(Operation):
  """ A more interesting one. This has an alternative method of adding parameters (as parameters are 
      non-simple), and preprocesses them into what the GraphQL API is expecting. It also does
      basic postprocessing.
  """

  args = [
    "updates"
  ]

  mandatory_parameters = set(["updates"])

  query = gql("""
    mutation($updates: [CandidacyStatusWithCandidacies!]!) {
    bulkUpdateCandidacyStatus(input: {updates: $updates}) {
      successfulUpdates
      failedUpdates
      errors {
      message
      }
    }
    }
  """)

  def set_params(self, params):
    """ Override this method to expose alternative means of adding
    """

    raise InvalidOperationError('Not valid for this mutation type. Please use add_outcomes(outcome, ids) instead')

  def set_param(self, field, value):
    """ Override this method to expose alternative means of adding
    """
    raise InvalidOperationError('Not valid for this mutation type. Please use add_outcome(outcome, ids) instead')

  def add_outcomes(self, outcomes):
    """ Set multiple outcomes at once from a dict. Returns self for fluent chaining.
    """

    for key, value in outcomes.items():
      self.add_outcome(key, value)
    return self

  def add_outcome(self, outcome, ids):
    """ Builds outcomes in an easy-to-manipulate form. Returns self for fluent chaining.
    """

    if not isinstance(ids, list):
      ids = [ids]

    if 'updates' not in self.params:
      self.params['updates'] = {}
      self.set_parameters.add('updates')

    if outcome not in self.params['updates']:
      self.params['updates'][outcome] = []

    self.params['updates'][outcome].extend(ids)

    return self

  def pre_process(self):
    """ Converts our manageable internal format to what the GraphQL API is expecting
    """

    processed = list(map(lambda item: {'status': item[0], 'ids': item[1]}, self.params['updates'].items()))
    self.final_params = {'updates': processed}

  def post_process(self):
    self.result = self.raw_result['bulkUpdateCandidacyStatus']

  def validate_params(self):
    """ Ensures all parameters for self.mandatory_parameters are set
    """

    if 'updates' not in self.params:
      raise MissingMandatoryParameterError(
        f'Missing mandatory parameters: no disposition parameters added'
      )
