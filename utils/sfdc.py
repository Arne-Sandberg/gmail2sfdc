import json
import urllib
import logging
import urllib2

import httplib2

from gmail2sfdc import settings


class Sfdc:
    logger = logging.getLogger(__name__)
    auth_endpoint = 'https://login.salesforce.com/services/oauth2'
    api_endpoint = '/services/data/v29.0'

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
        content = json.loads(content)
        # make one more api call to get user id
        identity_service_url = content['id']
        resp, user_data = http.request(identity_service_url,
                                       headers={'Authorization': 'Bearer ' + content['access_token']})
        user_data = json.loads(user_data)
        content['user_id'] = user_data['user_id']
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
    def insert_document(sf_auth, file_name, file_data):
        new_auth = Sfdc.refresh_token(sf_auth.refresh_token)
        access_token = new_auth['access_token']
        headers = {
            'Authorization': 'Bearer ' + access_token,
            'Content-Type': 'application/json'
        }
        # upload to 'My Documents' folder, folder is is same as user_id in this case
        params = {
            'folderId': sf_auth.sf_used_id,
            'name': file_name,
            'body': file_data
        }
        url = new_auth['instance_url'] + Sfdc.api_endpoint + '/sobjects/Document/'

        # http = httplib2.Http()
        # resp, content = http.request(Sfdc.api_endpoint+'/sobjects/Document/',
        # 'POST', json.dumps(params),
        #                              headers=headers)
        try:
            req = urllib2.Request(url, json.dumps(params), headers)
            response = urllib2.urlopen(req)
            content = response.read()
        except urllib2.HTTPError, e:
            print e.code
            print e.read()

        return content