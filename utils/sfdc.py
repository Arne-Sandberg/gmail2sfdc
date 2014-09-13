import json
import urllib
import logging
import urllib2

import httplib2

from gmail2sfdc import settings


class Sfdc:
    logger = logging.getLogger(__name__)
    auth_endpoint = 'https://login.salesforce.com/services/oauth2'
    api_endpoint = 'https://ap1.salesforce.com/services/data/v29.0'

    def __init__(self):
        pass

    @staticmethod
    def get_auth_url():
        params = {
            'response_type': 'code',
            'client_id': settings.SFDC_CLIENT_ID,
            'redirect_uri': settings.SFDC_REDIRECT_URI,
            'display': 'popup'
        }
        auth_url = Sfdc.auth_endpoint + '/authorize?' + urllib.urlencode(params)
        return auth_url

    @staticmethod
    def exchange_code(code):
        params = {
            'code': code,
            'grant_type': 'authorization_code',
            'client_id': settings.SFDC_CLIENT_ID,
            'client_secret': settings.SFDC_CLIENT_SECRET,
            'redirect_uri': settings.SFDC_REDIRECT_URI
        }
        http = httplib2.Http()
        resp, content = http.request(Sfdc.auth_endpoint + '/token',
                                     'POST', urllib.urlencode(params),
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return content

    @staticmethod
    def refresh_token(refresh_token):
        params = {
            'grant_type': 'refresh_token',
            'client_id': settings.SFDC_CLIENT_ID,
            'client_secret': settings.SFDC_CLIENT_SECRET,
            'refresh_token': refresh_token
        }
        http = httplib2.Http()
        resp, content = http.request(Sfdc.auth_endpoint + '/token',
                                     'POST', urllib.urlencode(params),
                                     headers={'Content-Type': 'application/x-www-form-urlencoded'})
        return json.loads(content)

    @staticmethod
    def insert_document(sf_auth, folder_id, file_name, file_data):
        access_token = Sfdc.refresh_token(sf_auth.refresh_token)['access_token']
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        print headers
        params = {
            'folderId': folder_id,
            'name': file_name,
            'body': file_data
        }
        url = Sfdc.api_endpoint + '/sobjects/Document/'

        # http = httplib2.Http()
        # resp, content = http.request(Sfdc.api_endpoint+'/sobjects/Document/',
        # 'POST', json.dumps(params),
        #                              headers=headers)
        try:
            req = urllib2.Request(url, json.dumps(params), headers)
            response = urllib2.urlopen(req)
            content = response.read()
            print content
        except urllib2.HTTPError, e:
            print e.code
            print e.read()

        return content