from datetime import datetime, timedelta
import json
import base64

from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.utils.datetime_safe import strftime

from accounts.models import Salesforce, Gmail
from utils.google import Google
from utils.sfdc import Sfdc


def connect_apps(request):
    # check if user is already connected to both gmail and salesforce
    # if so, redirect to emails page
    try:
        gmail_auth = Gmail.objects.get(user__id=request.session['user_id'])
    except Gmail.DoesNotExist:
        gmail_auth = None
    try:
        sf_auth = Salesforce.objects.get(user__id=request.session['user_id'])
    except Salesforce.DoesNotExist:
        sf_auth = None

    if gmail_auth and sf_auth:
        return redirect('emails')
    else:
        return render(request, "zaps/connect-apps.html", {'is_gmail_connected': True if gmail_auth else False,
                                                          'is_salesforce_connected': True if sf_auth else False})


def emails(request):
    return render(request, "zaps/emails.html", {})


def list_threads(request):
    gmail_service = Google.get_gmail_service(request.session['user_id'])

    last_synced_at = datetime.now()-timedelta(days=1)
    user_id = 'me'
    query = "after:%s AND has:attachment" % strftime(last_synced_at, "%Y/%m/%d", )
    page_token = 0

    threads_resp = gmail_service.users().threads().list(userId=user_id, q=query).execute()
    threads = threads_resp['threads'] if 'threads' in threads_resp else []
    threads_with_messages = []
    for thread in threads:
        # do a get on thread using id to fill messages
        thread = gmail_service.users().threads().get(userId=user_id, id=thread['id']).execute()
        messages = thread['messages']
        parsed_messages = []

        if messages:
            # parse the message content
            for message in messages:
                parsed_messages.append(parse_message(message))

        thread['messages'] = parsed_messages
        threads_with_messages.append(thread)

    data = json.dumps(threads_with_messages)
    return HttpResponse(data, mimetype='application/json')


def parse_message(message):
    parsed_message = {'id': message['id'],
                      'headers': message['payload']['headers'],
                      'content': parse_message_part(message['payload'])}
    return parsed_message


def parse_message_part(message_part):
    text_content = ''
    html_content = ''
    attachments = []
    mime_type = message_part['mimeType']
    if mime_type.startswith('multipart'):
        for part in message_part['parts']:
            parsed_part = parse_message_part(part)
            text_content += parsed_part['text_content']
            html_content += parsed_part['html_content']
            attachments.extend(parsed_part['attachments'])
    elif mime_type == 'text/html' and message_part['filename'] == "":
        html_content += decode_base64(message_part['body']['data'])
    elif mime_type == 'text/plain' and message_part['filename'] == "":
        text_content += decode_base64(message_part['body']['data'])
    else:
        # we are expecting an attachment here, no effect if attachment id is not encountered
        body = message_part['body']
        if 'attachmentId' in body:
            attachment = {'id': body['attachmentId'],
                          'filename': message_part['filename']}
            attachments.append(attachment)

    parsed_message = {'text_content': text_content,
                      'html_content': html_content,
                      'attachments': attachments}
    return parsed_message


def upload_to_sfdc(request):
    gmail_service = Google.get_gmail_service(request.session['user_id'])
    attachment_id = request.GET['att_id']
    message_id = request.GET['msg_id']
    file_name = request.GET['file_name']
    attachment = gmail_service.users().messages().attachments().get(userId='me',
                                                                    messageId=message_id, id=attachment_id).execute()
    file_data = attachment['data']
    if file_data:
        sf_auth = Salesforce.objects.get(user__id=request.session['user_id'])
        Sfdc.insert_document(sf_auth, '00l90000000g5up', file_name, file_data)
    return HttpResponse('success')


def decode_base64(b64_string):
    b64_string += "=" * (4 - len(b64_string) % 4)
    return base64.urlsafe_b64decode(b64_string.encode("utf-8"))