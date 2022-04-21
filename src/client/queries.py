from gql import gql
from .operation import Operation

class Query(Operation):
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
