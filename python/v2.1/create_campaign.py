#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""This example creates a campaign in a given advertiser.

To create an advertiser, run create_advertiser.py.
"""

import argparse
import sys

from apiclient import sample_tools
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to add a campaign for')
argparser.add_argument(
    'advertiser_id', type=int,
    help='The ID of the advertiser to associate the campaign with')


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'dfareporting', 'v2.1', __doc__, __file__, parents=[argparser],
      scope=['https://www.googleapis.com/auth/dfareporting',
             'https://www.googleapis.com/auth/dfatrafficking'])

  profile_id = flags.profile_id
  advertiser_id = flags.advertiser_id

  try:
    # Construct and save campaign.
    campaign = {
        'name': 'Test Campaign',
        'advertiserId': advertiser_id,
        'archived': 'false',
        'startDate': '2014-01-01',
        'endDate': '2020-01-01'
    }

    request = service.campaigns().insert(
        profileId=profile_id, defaultLandingPageName='Test Landing Page',
        defaultLandingPageUrl='http://www.google.com', body=campaign)

    # Execute request and print response.
    response = request.execute()

    print ('Created campaign with ID %s and name "%s".'
           % (response['id'], response['name']))

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


if __name__ == '__main__':
  main(sys.argv)
