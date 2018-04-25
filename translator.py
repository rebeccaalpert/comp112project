import urllib3, json, certifi
from models import Cache
from server import db, session
from difflib import SequenceMatcher
import re

MODE_TRANSLATE = "translate"
MODE_DETECT = "detect"
FORMAT_PLAIN = "plain"
RESPONSE_JSON = "tr.json"
RESPONSE_XML = "tr"
HOST = "https://translate.yandex.net/api/v1.5/"
KEY = "trnsl.1.1.20180323T002815Z.931efcfa06f08dc6."\
      "585e129a89a9ad92ac700de57bf10c55bd482438"
TRANS_API = HOST + RESPONSE_JSON + "/" + MODE_TRANSLATE
DETECT_API = HOST + RESPONSE_JSON + "/" + MODE_DETECT
ACCEPT_RATIO = 0.9
PATTERN = '[!@#$%^&*()_+=\-<>?/|\\,.]'
SUBWITH = ''

ERR_MSG = "Something bad happend during the request"

REQ_OBJ = {
    'key': KEY,
    'text': '',
    'lang': '',
    'target_lang': ''
}

RES_OBJ = {
    'code': 0,
    'lang': '',
    'msg_id': -1,
    'match': -1
}

# type == 0 => it is the translation
# type == 1 => it is the source language code
DB_OBJ = {
    'type': 0,
    'data': ''
}


def make_request(mode, url, args):
    http = urllib3.PoolManager(
            cert_reqs='CERT_REQUIRED',
            ca_certs=certifi.where())
    resp = http.request(mode, url, fields=args)

    if resp.status != 200:
        raise ValueError(ERR_MSG)

    return resp.data


def parse_response(resp_data):
    parsed = json.loads(resp_data.decode('utf-8'))
    if 'text' in parsed:
        return parsed['text'][0]
    if 'lang' in parsed:
        return parsed['lang']

    raise ValueError("Error occured parsing the response")


def detect_language(text):
    REQ_OBJ['text'] = text

    req = make_request('GET', DETECT_API, REQ_OBJ)
    parsed = parse_response(req)
    return parsed


def parse_request(text, source, target):

    # check if text is empty
    if not text:
        raise ValueError("'text' field is empty.")

    # check if source is empty
    if not source:
        raise ValueError("'source' field is empty.")

    # check if target is empty
    if not target:
        raise ValueError("'target' is empty")

    REQ_OBJ['text'] = text
    REQ_OBJ['lang'] = join_lang(source, target)

    return REQ_OBJ

def generate_response(code, lang='', msg_id='', match=''):
    RES_OBJ['code'] = code
    RES_OBJ['lang'] = lang
    RES_OBJ['msg_id'] = msg_id
    RES_OBJ['match'] = match

    return RES_OBJ

def translate(text, target, source='', msg_id=-1):
    """Attempts to translate the given text by making a request to Yandex API.

        text => Represents the text that the user wants translated
        source => the language that is being translated from.
        target => language that the receiver uses

        If source is empty then translate will do additional request to figure
        out the language of the sender.

        If there is any issue with the translation (API code != 200 or
        if API is down) translate function will raise ValueError.
        It is clients responsability to deal with the Errors returned.

    """

    # remove special characters as specified in the global varriable PATTER
    text = remove_special_chars(text)
    print(text)

    # first check the cache for the translation
    if (msg_id != -1):
          data = check_cache_by_id(msg_id, target)
          # check if the cache contains the requested translation
          if data is not None:
            if data['type'] == 0:
                return generate_response(200, data['data'], 
                                         msg_id, data['match'])
            else:
                source = data['data']
        
    # looking for the matching sentence/word and comparing it to source text
    data = check_cache_by_text(text, target)
    print(data)
    if data is not None:
        if data['type'] == 0:
            match = calc_match(text, data['old_txt'])
            print("check match")
            if match >= ACCEPT_RATIO:
                print("Match accepted")
                return generate_response(200, data['data'], 
                                         msg_id, data['match'])

    print("The source is: ", source, target)
    if source == target:
        return generate_response(200, text, msg_id, 1.0)

    try:
        # check if there is a need to detect a languge
        # if the source for particular message was found in the cache then skip
        if not source:
            source = detect_language(text)
            if source == target:
                return generate_response(200, text, msg_id, 1.0)

        req_data = parse_request(text, source, target)
        resp = make_request('GET', TRANS_API, req_data)
        trans = parse_response(resp)

        match = calc_match(target, source)

        addto_cache(source, target, text, trans, msg_id, match)

        return generate_response(200, trans, msg_id, match)

    except ValueError:
        return generate_response(500)
    except KeyError:
        return generate_response(500)

# cache functions

def check_cache_by_id(id, target):
    row = Cache.query.filter_by(msg_id=id, target_code=target).first()
    if row is not None:
        DB_OBJ['type'] = 0
        DB_OBJ['data'] = row.translated_text
        DB_OBJ['match'] = row.match
        return DB_OBJ

    row = Cache.query.filter_by(msg_id=id).first()

    if row is not None:
        DB_OBJ['type'] = 1
        DB_OBJ['data'] = row.source_code
        return DB_OBJ

    return None

def check_cache_by_text(text, target):
    row = Cache.query.filter(
        Cache.original_text.ilike('%' + text + '%')).filter_by(target_code=target).first()
    print(row)
    if row is not None:
        print('NOT NONE')
        print(row.target_code, target)
        if row.target_code == target:
            DB_OBJ['type'] = 0
            DB_OBJ['data'] = row.translated_text
            DB_OBJ['match'] = row.match
            DB_OBJ['old_txt'] = row.original_text
            return DB_OBJ
        else:
            DB_OBJ['type'] = 1
            DB_OBJ['data'] = row.source_code
            return DB_OBJ

    return None     

def remove_special_chars(text):
    return re.sub(PATTERN, SUBWITH,text)   

def addto_cache(source, target, text, translated, msg_id, match):
    cache_row = Cache(source, target, text, translated, msg_id, match)
    db.session.add(cache_row)
    db.session.commit()

# 'Private' functions

def join_lang(lang, target):
    return '-'.join([lang, target])


def calc_match(source, target):
    return SequenceMatcher(None, source, target).ratio()

# main function which executes if this module is used on its own
if __name__ == '__main__':

    print(translate('thank you for everything', 'en', 'ru'))
