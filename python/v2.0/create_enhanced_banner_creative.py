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

"""This example creates an enhanced banner creative.

Requires an HTML5/flash asset, backup image asset, and an advertiser ID as
input. To get an advertiser ID, run get_advertisers.py.
"""

import argparse
import sys

from apiclient import sample_tools
from apiclient.http import MediaFileUpload
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument(
    'profile_id', type=int,
    help='The ID of the profile to add a user role for')
argparser.add_argument(
    'advertiser_id', type=int,
    help='The ID of the advertiser to associate this creative with.')
argparser.add_argument(
    'size_id', type=int,
    help='The ID of the size of this creative.')
argparser.add_argument(
    'html_asset_name',
    help='Suggested name to use for the uploaded creative asset.')
argparser.add_argument(
    'path_to_html_asset_file',
    help='Path to the asset file to be uploaded.')
argparser.add_argument(
    'image_name',
    help='Suggested name to use for the uploaded creative asset.')
argparser.add_argument(
    'path_to_image_file',
    help='Path to the asset file to be uploaded.')


def main(argv):
  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv, 'dfareporting', 'v2.0', __doc__, __file__, parents=[argparser],
      scope=['https://www.googleapis.com/auth/dfareporting',
             'https://www.googleapis.com/auth/dfatrafficking'])

  profile_id = flags.profile_id
  advertiser_id = flags.advertiser_id
  html_asset_name = flags.html_asset_name
  image_name = flags.image_name
  path_to_html_asset_file = flags.path_to_html_asset_file
  path_to_image_file = flags.path_to_image_file
  size_id = flags.size_id

  try:
    # Upload the HTML asset
    html_asset_id = upload_creative_asset(
        service, profile_id, advertiser_id, html_asset_name,
        path_to_html_asset_file, 'HTML')

    # Upload the backup image asset
    backup_image_asset_id = upload_creative_asset(
        service, profile_id, advertiser_id, image_name, path_to_image_file,
        'HTML_IMAGE')

    # Construct the creative structure.
    creative = {
        'advertiserId': advertiser_id,
        'backupImageClickThroughUrl': 'https://www.google.com',
        'backupImageReportingLabel': 'backup_image_exit',
        'backupImageTargetWindow': {'targetWindowOption': 'NEW_WINDOW'},
        'clickTags': [{
            'eventName': 'exit',
            'name': 'click_tag',
            'value': 'https://www.google.com'
        }],
        'creativeAssets': [
            {'assetIdentifier': html_asset_id, 'role': 'PRIMARY'},
            {'assetIdentifier': backup_image_asset_id, 'role': 'BACKUP_IMAGE'},
        ],
        'name': 'Test enhanced banner creative',
        'size': {'id': size_id},
        'type': 'ENHANCED_BANNER'
    }

    request = service.creatives().insert(profileId=profile_id, body=creative)

    # Execute request and print response.
    response = request.execute()

    print ('Created enhanced banner creative with ID %s and name "%s".'
           % (response['id'], response['name']))

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')


def upload_creative_asset(
    service, profile_id, advertiser_id, asset_name, path_to_asset_file,
    asset_type):
  """Uploads a creative asset and returns an assetIdentifier."""
  # Construct the creative asset metadata
  creative_asset = {
      'assetIdentifier': {
          'name': asset_name,
          'type': asset_type
      }
  }

  media = MediaFileUpload(path_to_asset_file)
  if not media.mimetype():
    media = MediaFileUpload(path_to_asset_file, 'application/octet-stream')

  response = service.creativeAssets().insert(
      advertiserId=advertiser_id,
      profileId=profile_id,
      media_body=media,
      body=creative_asset).execute()

  return response['assetIdentifier']


if __name__ == '__main__':
  main(sys.argv)
