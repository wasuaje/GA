"""A simple example of how to access the Google Analytics API."""

import argparse

from apiclient.discovery import build
from oauth2client.client import SignedJwtAssertionCredentials

import httplib2


from oauth2client import client
from oauth2client import file
from oauth2client import tools



def get_service(api_name, api_version, scope, key_file_location,
                service_account_email):
  """Get a service that communicates to a Google API.

  Args:
    api_name: The name of the api to connect to.
    api_version: The api version to connect to.
    scope: A list auth scopes to authorize for the application.
    key_file_location: The path to a valid service account p12 key file.
    service_account_email: The service account email address.

  Returns:
    A service that is connected to the specified API.
  """

  f = open(key_file_location, 'rb')
  key = f.read()
  f.close()

  credentials = SignedJwtAssertionCredentials(service_account_email, key,
    scope=scope)

  http = credentials.authorize(httplib2.Http())

  # Build the service object.
  service = build(api_name, api_version, http=http)

  return service

def user_by_account(service):
  cuentas=['344727',]
  try:
    account_links = service.management().accountUserLinks().list(
      accountId='3447275').execute()

  except TypeError, error:
  # Handle errors in constructing a query.
    print 'There was an error in constructing your query : %s' % error

  # except HttpError, error:
  # # Handle API errors.
  #   print ('There was an API error : %s : %s' %
  #        (error.resp.status, error.resp.reason))


# Example #2:
# The results of the list method are stored in the account_links object.
# The following code shows how to iterate through them.
  #print account_links
  for accountUserLink in account_links.get('items', []):
    entity = accountUserLink.get('entity', {})
    accountRef = entity.get('accountRef', {})
    userRef = accountUserLink.get('userRef', {})
    permissions = accountUserLink.get('permissions', {})

    print 'Account User Link Id   = %s' % accountUserLink.get('id')
    print 'Account User Link kind = %s' % accountUserLink.get('kind')
    print 'User Email             = %s' % userRef.get('email')
    print 'Permissions effective  = %s' % permissions.get('effective')
    print 'Permissions local      = %s' % permissions.get('local')
    print 'Account Id             = %s' % accountRef.get('id')
    print 'Account Kind           = %s' % accountRef.get('kind')
    print 'Account Name           = %s\n' % accountRef.get('name')

def user_by_profile(service):
  # Note: This code assumes you have an authorized Analytics service object.
# See the User Permissions Developer Guide for details.

# Example #1:
# Requests a list of profile-user links for a given view (profile).
  try:
    profile_links = service.management().profileUserLinks().list(
        accountId='344727',
        webPropertyId='~all',
        profileId='~all'
    ).execute()

  except TypeError, error:
    # Handle errors in constructing a query.
    print 'There was an error in constructing your query : %s' % error

  # except HttpError, error:
  #   # Handle API errors.
  #   print ('There was an API error : %s : %s' %
  #          (error.resp.status, error.resp.reason))


  # Example #2:
  # The results of the list method are stored in the profile_links object.
  # The following code shows how to iterate through them.
  print "\"%s\";\"%s\";\"%s\"\n" % ('User Email','Permissions effective','Profile Name')
  for profileUserLink in profile_links.get('items', []):
    entity = profileUserLink.get('entity', {})
    profileRef = entity.get('profileRef', {})
    userRef = profileUserLink.get('userRef', {})
    permissions = profileUserLink.get('permissions', {})

    #print 'Profile User Link Id   = %s' % profileUserLink.get('id')
    #print 'Profile User Link kind = %s' % profileUserLink.get('kind')
    #print 'User Email             = %s' % userRef.get('email')
    #print 'Permissions effective  = %s' % permissions.get('effective')
    #print 'Permissions local      = %s' % permissions.get('local')
    #print 'Profile Id             = %s' % profileRef.get('id')
    #print 'Profile kind           = %s' % profileRef.get('kind')
    #print 'Profile Name           = %s\n' % profileRef.get('name')
    print "\"%s\";\"%s\";\"%s\"" % (userRef.get('email'),permissions.get('effective'),profileRef.get('name'))




def get_first_profile_id(service):
  # Use the Analytics service object to get the first profile id.

  # Get a list of all Google Analytics accounts for this user
  accounts = service.management().accounts().list().execute()

  if accounts.get('items'):
    # Get the first Google Analytics account.
    account = accounts.get('items')[0].get('id')

    # Get a list of all the properties for the first account.
    properties = service.management().webproperties().list(
        accountId=account).execute()

    if properties.get('items'):
      # Get the first property id.
      property = properties.get('items')[0].get('id')

      # Get a list of all views (profiles) for the first property.
      profiles = service.management().profiles().list(
          accountId=account,
          webPropertyId=property).execute()

      if profiles.get('items'):
        # return the first view (profile) id.
        return profiles.get('items')[0].get('id')

  return None


def get_results(service, profile_id):
  # Use the Analytics Service Object to query the Core Reporting API
  # for the number of sessions within the past seven days.
  return service.data().ga().get(
      ids='ga:' + profile_id,
      start_date='7daysAgo',
      end_date='today',
      metrics='ga:sessions').execute()


def print_results(results):
  # Print data nicely for the user.
  if results:
    print 'View (Profile): %s' % results.get('profileInfo').get('profileName')
    print 'Total Sessions: %s' % results.get('rows')[0][0]

  else:
    print 'No results found'


def main():
  # Define the auth scopes to request.
  scope = ['https://www.googleapis.com/auth/analytics.readonly',\
        'https://www.googleapis.com/auth/analytics.manage.users',
        'https://www.googleapis.com/auth/analytics.manage.users.readonly']

  # Use the developer console and replace the values with your
  # service account email and relative location of your key file.
  service_account_email = '1066381970584-169u2vk4gghqjf9tk0clpan3bm0j8o5t@developer.gserviceaccount.com'

  key_file_location = 'wasuaje-5363cf76ffd9.p12'

  # Authenticate and construct service.
  service = get_service('analytics', 'v3', scope, key_file_location,
    service_account_email)
  #profile = get_first_profile_id(service)
  #print_results(get_results(service, profile))
  #user_by_account(service)
  user_by_profile(service)

if __name__ == '__main__':
  main()
