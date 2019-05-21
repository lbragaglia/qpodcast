from __future__ import print_function
import pickle
import os.path
import sys
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Copyright 2018 Google LLC
# Licensed under the Apache License, Version 2.0
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']
def auth():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds

def main():
    service = build('drive', 'v3', credentials=auth())

    results = service.files().list(
        pageSize=200,
        fields="nextPageToken, files(id, name, owners, createdTime, size, webContentLink)",
        q="'1DvratOsY0QJxO-dcMFQYR4gLkRHPuJ7E' in parents",
        orderBy='name'
    ).execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        sys.exit(1)

    for item in items:
        print(u'{0},{1},{2},{3},{4},{5}'.format(item['id'], item['name'], item['owners'][0]['displayName'], item['createdTime'], item['size'], item['webContentLink']).encode('utf-8'))

if __name__ == '__main__':
    main()
