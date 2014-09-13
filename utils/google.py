import logging
from apiclient.discovery import build

import httplib2
from oauth2client.client import OAuth2WebServerFlow, OAuth2Credentials
from apiclient import errors
from accounts.models import Gmail
from gmail2sfdc import settings


class Google:
    logger = logging.getLogger(__name__)
    GOOGLE_PROFILE_SCOPE = 'profile email'
    GMAIL_READ_SCOPE = 'https://www.googleapis.com/auth/gmail.readonly'

    def __init__(self):
        pass

    @staticmethod
    def get_auth_url():
        flow = Google.__get_login_flow()
        auth_url = flow.step1_get_authorize_url()
        return auth_url

    @staticmethod
    def get_gmail_oauth_url():
        flow = Google.__get_gmail_flow()
        auth_url = flow.step1_get_authorize_url()
        return auth_url

    @staticmethod
    def __get_login_flow():
        flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_CLIENT_ID,
                                   client_secret=settings.GOOGLE_CLIENT_SECRET,
                                   scope=Google.GOOGLE_PROFILE_SCOPE,
                                   state='login',
                                   redirect_uri=settings.GOOGLE_REDIRECT_URI)
        return flow

    @staticmethod
    def __get_gmail_flow():
        flow = OAuth2WebServerFlow(client_id=settings.GOOGLE_CLIENT_ID,
                                   client_secret=settings.GOOGLE_CLIENT_SECRET,
                                   scope=Google.GMAIL_READ_SCOPE,
                                   state='gmail',
                                   access_type='offline',
                                   approval_prompt='force',
                                   redirect_uri=settings.GOOGLE_REDIRECT_URI)
        return flow

    @staticmethod
    def exchange_code(code, state):
        if state == 'login':
            flow = Google.__get_login_flow()
            return flow.step2_exchange(code)
        elif state == 'gmail':
            flow = Google.__get_gmail_flow()
            return flow.step2_exchange(code)

    @staticmethod
    def get_profile(credentials):
        http = httplib2.Http()
        http = credentials.authorize(http)
        resp, content = http.request('https://www.googleapis.com/userinfo/v2/me')
        return content

    @staticmethod
    def get_gmail_service(user_id):
        http = httplib2.Http()
        gmail_auth = Gmail.objects.get(user__id=user_id)
        credentials = OAuth2Credentials.new_from_json(gmail_auth.credentials_json)
        http = credentials.authorize(http)
        return build('gmail', 'v1', http=http)
