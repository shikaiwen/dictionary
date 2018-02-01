from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import io
from googleapiclient.http import MediaIoBaseDownload


# https://developers.google.com/drive/v3/web/manage-downloads#downloading_google_documents
# https://developers.google.com/apis-explorer/#p/drive/v3/
# https://developers.google.com/oauthplayground/

# https://developers.google.com/identity/protocols/googlescopes
# https://developers.google.com/identity/protocols/OAuth2WebServer

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/drive-python-quickstart.json
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly',
          "https://www.googleapis.com/auth/drive"]
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Drive API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'drive-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
#         else: # Needed only for compatibility with Python 2.6
#             credentials = tools.run(flow, store)

        print('Storing credentials to ' + credential_path)
    return credentials

from googleapiclient.discovery import build 
def main():
    """Shows basic usage of the Google Drive API.

    Creates a Google Drive API service object and outputs the names and IDs
    for up to 10 files.
    """
    
#     这种app key只能访问统计信息，不能访问个人数据
#     service = build('drive', 'v3', developerKey='AIzaSyCIbeHytuJm-7AsRrEtW91GIywQGNipIEA')
    
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('drive', 'v3', http=http)

    results = service.files().list(
        pageSize=10,fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])
    
    fname = "jpword-2018/02/01.txt"
    wantlist = list(filter(lambda x: x["name"] == fname ,results.get('files')))
    
    
    if(len(wantlist) > 0):
        todayfile = wantlist[0]
        contentobj = service.files().get(fileId=todayfile["id"])
        print(contentobj)
        fileId = todayfile["id"]
        request = service.files().export_media(fileId=fileId,mimeType='text/plain')
        fh = io.BytesIO()
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print("Download %d%%." % int(status.progress() * 100))        
        aa = fh.getvalue().decode("utf-8")
        print(aa)
    if not items:
        print('No files found.')
    else:
        print('Files:')
        for item in items:
            print('{0} ({1})'.format(item['name'], item['id']))

if __name__ == '__main__':
    main()