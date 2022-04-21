from gql import gql
from .operation import Operation

class Query(Operation):
  pass

class ExampleQuery(Query):
  """ Examples of what can be overriden on an Operation

      You can also override any methods that a given Operation shouldn't be
      able to do, for instance if you have custom parameter setting you
      can override set_params() to throw an exception
  """

  # Whether this is a GraphQL connection type and should allow the paging vars
  connection_type = False

  # Can be either a dict or a list
  args = {
    'fieldName1': [],
    'fieldName2': ['subfield'],
    'fieldName3': ['subfield'],
    'fieldName3': ['subfield', 'subsubfield']
  }
  # Creates the following when fully populated:
  # {
  #   fieldName1: value,
  #   subfield: {
  #     fieldName2: value,
  #     fieldName3: value,
  #     subsubfield: {
  #       fieldName3: value
  #     }
  #   }
  # }

  args = [
    'fieldName1',
    'fieldName2',
    'fieldName3',
    'fieldName3'
  ]
  # Creates the following when fully populated:
  # {
  #   fieldName1: value,
  #   fieldName2: value,
  #   fieldName3: value,
  #   fieldName3: value
  # }

  query = gql("""
    your query goes here!
  """)

  # Need custom pre-processing? This method is for you!
  # It needs to read from self.params and write to self.final_params
  def pre_process():
    pass

  # Need custom post-processing? This method is for you!
  # It needs to read from self.raw_result and write to self.result
  def pre_process():
    pass

class UserQuery(Query):
  connection_type = True

  args = {
    'orderBy': [],
    'search': [],
    'clientUserType': ['filter'],
    'group': ['filter'],
    'disabled': ['filter']
  }

  query = gql("""
    query(
      $filter: UserFilter, $orderBy: [UserOrderBy!], $search: String,
      $first: Int, $last: Int, $before: String, $after: String
    ) {
      users(
        filter: $filter, orderBy: $orderBy, search: $search,
        first: $first, last: $last, before: $before, after: $after
      ) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          id
          name
          email
          phone
          timeZone
          clientUserType
          lastSeen
          groups {
            nodes {
              id
              name
            }
          }
        }
      }
    }
  """)

class GroupQuery(Query):
  connection_type = True

  args = {
    'search': [],
    'id': ['filter']
  }

  query = gql("""
    query(
      $filter: GroupFilter, $search: String,
      $first: Int, $last: Int, $before: String, $after: String
    ) {
      groups(
        filter: $filter, search: $search,
        first: $first, last: $last, before: $before, after: $after
      )
      {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          id
          name
        }
      }
    }
  """)

class RoleQuery(Query):
  connection_type = True

  args = {
    "orderBy": [],
    "search": [],
    
    "archived": ['filter'],
    "demo": ['filter'],
    "group": ['filter'],
    "id": ['filter']
  }

  query = gql("""
    query(
      $filter: RoleFilter, $orderBy: RoleOrderBy, $search: String,
      $first: Int, $last: Int, $before: String, $after: String
    ) {
      roles(
        filter: $filter, orderBy: $orderBy, search: $search,
        first: $first, last: $last, before: $before, after: $after
      )
      {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          id
          name
          group {
            id
            name
          }
        }
      }
    }
  """)

class CandidacyQuery(Query):
  connection_type = True

  args = {
    "orderBy": [],
    "search": [],
    
    "id": ['filter'],
    "group": ['filter'],
    "role": ['filter'],
    "recruiter": ['filter'],
    "candidate": ['filter'],
    "archived": ['filter'],
    "demo": ['filter'],
    "codeChallengeState": ['filter'],
    "interviewState": ['filter'],
    "status": ['filter'],
    "atsUrl": ['filter'],
    "atsUrlSubstring": ['filter'],
    "createdAfter": ['filter'],
    "createdBefore": ['filter'],
    "lastStatusUpdateAfter": ['filter'],
    "lastStatusUpdateBefore": ['filter'] 
  }

  query = gql("""
    query(
      $orderBy: [CandidacyOrderBy!], $filter: CandidacyFilter,
      $first: Int, $last: Int, $before: String, $after: String
    ) {
      candidacies(
        orderBy: $orderBy, filter: $filter,
        first: $first, last: $last, before: $before, after: $after
      ) {
        totalCount
        pageInfo {
          endCursor
          hasNextPage
        }
        nodes {
          id
          status
          atsUrl
          atsCandidateId
          atsApplicationId
          race
          gender
          lastStatusUpdate
          candidate {
            id
            name
            email
            safeResumeUrl
          }
          recruiter {
            id
            name
            email
          }
          role {
            id
            name
            group {
              id
              name
            }
          }
          codeChallenges {
            nodes {
              id
              createdAt
              state
              endTime
              recommendation
            }
          }
          interviews {
            nodes {
              id
              createdAt
              state
              endTime
              recommendation
              isRedo
              shippedTime
              result {
                id
                overallThoughts
                updatedAt
                createdAt
              }
              nextRedoInterview {
                id
                createdAt
                state
                endTime
                recommendation
                isRedo
              }
            }
          }
        }
      }
    }
  """)
