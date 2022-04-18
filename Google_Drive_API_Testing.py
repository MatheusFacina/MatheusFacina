#!/usr/bin/env python
# coding: utf-8

# In[2]:


# !pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

import pandas as pd
import os

sheet_id = "1gJ8Gtb6r9vMIWSmE26KAuhoGGSf3FCVWpfPG1JqjPwc"

sheet_name = "form test"

url = f"https://docs.google.com/spreadsheets/d/1gJ8Gtb6r9vMIWSmE26KAuhoGGSf3FCVWpfPG1JqjPwc/edit?usp=sharing"

sheet_url = "https://docs.google.com/spreadsheets/d/1gJ8Gtb6r9vMIWSmE26KAuhoGGSf3FCVWpfPG1JqjPwc/edit#gid=1207319876"
url_1 = sheet_url.replace("/edit#gid=", "/export?format=csv&gid=")

pd.read_csv(url_1)

# In[22]:

os.getcwd()

# **primeiro fluxo de autenticação Drive API**

# [START drive_quickstart]
from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']


def main():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('drive', 'v3', credentials=creds)

        # Call the Drive v3 API
        results = service.files().list(
            pageSize=10, fields="nextPageToken, files(id, name)").execute()
        items = results.get('files', [])

        if not items:
            print('No files found.')
            return
        print('Files:')
        for item in items:
            print(u'{0} ({1})'.format(item['name'], item['id']))
    except HttpError as error:
        # TODO(developer) - Handle errors from drive API.
        print(f'An error occurred: {error}')


if __name__ == '__main__':
    main()
# [END drive_quickstart]

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()
gauth.LocalWebserverAuth() # client_secrets.json need to be in the same directory as the script
drive = GoogleDrive(gauth)

# https://stackoverflow.com/questions/24419188/automating-pydrive-verification-process

gauth = GoogleAuth()

# Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there

    # This is what solved the issues:
    gauth.GetFlow()
    gauth.flow.params.update({'access_type': 'offline'})
    gauth.flow.params.update({'approval_prompt': 'force'})

    gauth.LocalWebserverAuth()

elif gauth.access_token_expired:

    # Refresh them if expired

    gauth.Refresh()

else:

    # Initialize the saved creds

    gauth.Authorize()

# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")  

drive = GoogleDrive(gauth)

# View all folders and file in your Google Drive
fileList = drive.ListFile({'q': "mimeType = 'application/vnd.google-apps.folder' and title contains '8 - Anexe' and trashed=false"}).GetList()

for file in fileList:
    print('Title: %s, ID: %s' % (file['title'], file['id']))
    # Get the folder ID that you want
    if "Anexe as fotos do equipamento" in file['title']:
        fileID = file['id']

print(fileID)

fileList = drive.ListFile({'q': "'%s' in parents and trashed=false" % fileID}).GetList()
for file in fileList:
    print(file['modifiedDate'], "\n")

print(file)

file1 = drive.CreateFile({'id': "1yC1LFz1rlFkb0lh63fuQYmY78J7DXSJc"})
file1.Upload()
file1['parents'] = [{"kind": "drive#parentReference", "id": "destination_folder_id"}]
file1.Upload()

import quickstart

"""Shows basic usage of the Drive v3 API.
Prints the names and ids of the first 10 files the user has access to.
"""
creds = None
# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('drive', 'v3', credentials=creds)
    page_token = None
    while True:
        response = service.files().list(q= "mimeType = 'application/vnd.google-apps.folder' and name contains '8 - Anexe as fotos'",
                                              spaces='drive',
                                              fields='nextPageToken, files(id, name)',
                                              pageToken=page_token).execute()
        for file in response.get('files', []):
            # Process change
            print('Found file: %s (%s)' % (file.get('name'), file.get('id')))
        page_token = response.get('nextPageToken', None)
        if page_token is None:
            break
except HttpError as error:
    # TODO(developer) - Handle errors from drive API.
    print(f'An error occurred: {error}')
    

# View all folders and file in your Google Drive

creds = None
# The file token.json stores the user's access and refresh tokens, and is created automatically when the authorization flow completes for the first time.

if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

try:
    service = build('drive', 'v3', credentials=creds)

    fileList = service.files().list(q = 'mimeType = application/vnd.google-apps.folder and title contains "8 - Anexe" and trashed=false',
                                                  spaces='drive',
                                                  fields='nextPageToken, files(id, name)',
                                                  pageToken=page_token).execute() 
    for file in fileList.get('files', []):
        print('Title: %s, ID: %s' % (file['title'], file['id']))
        # Get the folder ID that you want
        if "Anexe as fotos do equipamento" in file['title']:
            fileID = file['id']

