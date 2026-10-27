"""Outbound provider calls; no credentials are persisted in the database."""
import base64
import json
import os
import urllib.error
import urllib.parse
import urllib.request


def credentials_ready():
    return bool(os.environ.get('TWILIO_ACCOUNT_SID') and os.environ.get('TWILIO_AUTH_TOKEN'))


def verify_ready():
    return credentials_ready() and bool(os.environ.get('TWILIO_VERIFY_SERVICE_SID'))


def _post(url, params):
    if not credentials_ready():
        raise ValueError('Twilio credentials are not configured.')
    token = base64.b64encode((os.environ['TWILIO_ACCOUNT_SID'] + ':' + os.environ['TWILIO_AUTH_TOKEN']).encode()).decode()
    req = urllib.request.Request(url, data=urllib.parse.urlencode(params).encode(), headers={
        'Authorization': 'Basic ' + token,
        'Content-Type': 'application/x-www-form-urlencoded',
    })
    try:
        with urllib.request.urlopen(req, timeout=12) as res:
            return json.load(res)
    except urllib.error.HTTPError as exc:
        # Provider error text may contain identifiers. Show only the status.
        raise ValueError(f'Provider rejected the request (HTTP {exc.code}).') from exc
    except urllib.error.URLError as exc:
        raise ValueError('Unable to connect to the provider.') from exc


def send_whatsapp(phone, variables, config, content_sid=None):
    if config.whatsapp_provider != 'twilio' or not credentials_ready():
        raise ValueError('WhatsApp integration is not ready.')
    if not config.whatsapp_sender or not (content_sid or config.whatsapp_content_sid):
        raise ValueError('Approved WhatsApp sender and content template are required.')
    sid = os.environ['TWILIO_ACCOUNT_SID']
    return _post(f'https://api.twilio.com/2010-04-01/Accounts/{sid}/Messages.json', {
        'From': 'whatsapp:' + config.whatsapp_sender,
        'To': 'whatsapp:' + phone,
        'ContentSid': content_sid or config.whatsapp_content_sid,
        'ContentVariables': json.dumps(variables),
    })


def start_verification(phone):
    sid = os.environ['TWILIO_VERIFY_SERVICE_SID']
    return _post(f'https://verify.twilio.com/v2/Services/{sid}/Verifications', {'To': phone, 'Channel': 'sms'})


def check_verification(phone, code):
    sid = os.environ['TWILIO_VERIFY_SERVICE_SID']
    return _post(f'https://verify.twilio.com/v2/Services/{sid}/VerificationCheck', {'To': phone, 'Code': code})


def message_status(message_sid):
    if not credentials_ready() or not message_sid.startswith('SM'):
        raise ValueError('Missing credentials or invalid message ID.')
    account_sid = os.environ['TWILIO_ACCOUNT_SID']
    token = base64.b64encode((account_sid + ':' + os.environ['TWILIO_AUTH_TOKEN']).encode()).decode()
    url = f'https://api.twilio.com/2010-04-01/Accounts/{account_sid}/Messages/{message_sid}.json'
    req = urllib.request.Request(url, headers={'Authorization': 'Basic ' + token})
    try:
        with urllib.request.urlopen(req, timeout=12) as res:
            return json.load(res)
    except (urllib.error.HTTPError, urllib.error.URLError) as exc:
        raise ValueError('Unable to retrieve message delivery status.') from exc
