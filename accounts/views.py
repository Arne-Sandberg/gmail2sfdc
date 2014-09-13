import json

from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.contrib import auth as django_auth

from utils.google import Google
from accounts.models import MyUser, Gmail, Salesforce
from utils.sfdc import Sfdc


def google_login(request):
    return redirect(Google.get_auth_url())


def gmail_oauth(request):
    return redirect(Google.get_gmail_oauth_url())


def google_oauth_callback(request):
    state = request.GET['state']
    credentials = Google.exchange_code(request.GET['code'], state)
    if state == 'login':
        profile_str = Google.get_profile(credentials)
        profile = json.loads(profile_str)
        try:
            user = MyUser.objects.get(email=profile['email'])
        except ObjectDoesNotExist:
            user = None

        if user is None:
            user = MyUser(name=profile['name'], email=profile['email'], picture_url=profile['picture'])
            user.save()
        request.session['user_id'] = user.id
        return redirect(reverse('connect_apps'))
    elif state == 'gmail':
        # store gmail oauth credentials in db
        try:
            gmail_auth = Gmail.objects.get(user__id=request.session['user_id'])
        except ObjectDoesNotExist:
            gmail_auth = None

        if gmail_auth is None:
            user = MyUser.objects.get(id=request.session['user_id'])
            gmail_auth = Gmail(user=user, credentials_json=credentials.to_json())
            gmail_auth.save()
        else:
            gmail_auth.credentials_json = credentials.to_json()
            gmail_auth.save()

        return redirect(reverse('close_window'))


def sfdc_oauth(request):
    return redirect(Sfdc.get_auth_url())


def sfdc_oauth_callback(request):
    credentials_str = Sfdc.exchange_code(request.GET['code'])
    credentials = json.loads(credentials_str)
    try:
        sfdc_auth = Salesforce.objects.get(user__id=request.session['user_id'])
    except ObjectDoesNotExist:
        sfdc_auth = None

    if sfdc_auth is None:
        user = MyUser.objects.get(id=request.session['user_id'])
        sfdc_auth = Salesforce(user=user, access_token=credentials['access_token'], refresh_token=credentials['refresh_token'])
        sfdc_auth.save()
    else:
        sfdc_auth.access_token = credentials['access_token']
        sfdc_auth.refresh_token = credentials['refresh_token']
        sfdc_auth.save()

    return redirect(reverse('close_window'))


def logout(request):
    django_auth.logout(request)
    return redirect(reverse('home'))