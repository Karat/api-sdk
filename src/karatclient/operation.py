from .exceptions import UnexpectedArgumentError, UnusableClientError, MissingMandatoryParameterError

class Operation:
  # Set up some defaults...
  args = {}
  mandatory_parameters = set()

  # Is this a GraphQL connection type? Override in your subclass if so
  connection_type = False

  # If this is a connection type, the following parameters are assumed to exist
  connection_type_extra_params = set([
    'first',
    'last',
    'before',
    'after'
  ])

  # We can either instantiate these through KaratClient's internal list
  # (via KaratClient.query('name')/KaratClient.mutation('name')), or
  # instantiate them manually from some subclass (i.e. UserQuery(karat_client))

  def __init__(self, karat_client):
    self.karat_client = karat_client

    if self.connection_type:
      for item in self.connection_type_extra_params:
        self.args[item] = []
    self.params = {}
    self.set_parameters = set()

  def possible_args(self):
    """ List the possible arguments expected by this Operation
    """

    args = list(self.args.keys()) if isinstance(self.args, dict) else self.args

    return args

  def mandatory_args(self):
    """ List the mandatory arguments, without which this Operation
        cannot be executed
    """

    return list(self.mandatory_parameters)

  def execute(self):
    """ Perform the actual operation. This validates usability of the client,
        calls the Operation's preprocess and postprocess steps and returns the
        result
    """

    if not self.karat_client.usable:
      raise UnusableClientError(self.karat_client.reason)

    self.validate_params()
    self.pre_process() 
    self.raw_result = self.karat_client.execute(self.query, self.final_params)
    self.post_process()

    return self.result
  
  def pre_process(self):
    """ Any pre-processing that needs to happen. This is a default
        that just mirrors the input to the actual passed parameters,
        and can be overridden in any actual operations that are defined.
    """

    self.final_params = self.params

  def post_process(self):
    """ Any post-processing that needs to happen to the raw result.
        This is a default that just mirrors the raw result to the
        final result, and can be overridden in any actual
        operations that are defined.
    """

    self.result = self.raw_result

  def validate_params(self):
    """ Ensures all parameters for self.mandatory_parameters are set
    """

    expected = self.mandatory_parameters.copy()

    for item in self.set_parameters:
      if item in expected:
        expected.remove(item)
    
    if not len(expected) == 0:
      raise MissingMandatoryParameterError(
        f'Missing mandatory parameters: expected {list(expected)}'
      )

  def set_param(self, field, value):
    """ Drops passed parameters in the right place for the GraphQL operation, based
        on self.args. Returns self for fluent chaining.
    """

    if field not in self.args:
      raise UnexpectedArgumentError(f'Unexpected argument: {field}')

    if isinstance(self.args, list):
      self.params[field] = value
      self.set_parameters.add(field)
      return self

    if isinstance(self.args, dict):
      target = self.params
      for key in self.args[field]:
        if key not in target:
          target[key] = {}

        target = target[key]
      
      target[field] = value
      self.set_parameters.add(field)

      return self

  def set_params(self, params):
    """ Set multiple parameters at once from a dict. Returns self for fluent chaining.
    """

    for key, value in params.items():
      self.set_param(key, value)

    return self