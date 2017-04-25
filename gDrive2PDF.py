#!/usr/bin/env python

"""
You will need the following before running this script
1) The google api python client. Available at https://developers.google.com/api-client-library/python/ 
   sudo pip install setuptools
   sudo pip install --upgrade google-api-python-client
   
2) A client_secret.json file which can be created and downloaded once the Drive API is enabled for your account
   https://console.cloud.google.com/apis/dashboard

This script is mainly stitched together from the following sources:
http://wescpy.blogspot.com/2015/12/migrating-to-new-google-drive-api-v3.html
https://developers.google.com/drive/v3/web/manage-downloads
"""

from __future__ import print_function
import os

from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://www.googleapis.com/auth/drive'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store, flags) \
            if flags else tools.run(flow, store)
DRIVE = build('drive', 'v3', http=creds.authorize(Http()))

FILE_ID = 'XXXXXXXXXXXXXXXXXXXXX'
FILENAME = 'XXXXXXXXXXXXXXXXXXXXX'
if True:
    MIMETYPE = 'application/pdf'
    data = DRIVE.files().export(fileId=FILE_ID, mimeType=MIMETYPE).execute()
    if data:
        fn = '%s.pdf' % os.path.splitext(FILENAME)[0]
        with open(fn, 'wb') as fh:
            fh.write(data)
        print('Downloaded "%s" (%s)' % (fn, MIMETYPE))