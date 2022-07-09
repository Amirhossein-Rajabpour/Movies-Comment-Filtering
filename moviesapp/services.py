from moviesapp.models import Comment
import requests

API_key_STT = "Neh8_ZXoY5FJIpI08hjcGyFkHrncP73OAsVxDPDkG3oM"
url_STT = "https://api.eu-gb.speech-to-text.watson.cloud.ibm.com/instances/cc5d615b-dd84-460e-9c13-3cd8f2a9f919/v1/recognize"

API_key_NLU = "M8S4-iglkuWREF04JTS9G-GGKQgRRs1EZVOZ_Hyf0qTw"
url_NLU = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/25e1e806-17b8-414b-bd21-9e005a6eb584/v1/analyze?version=2019-07-12"

API_key_translate = "KIWVoirx8TOsHY_K5gOUy7VyHrxKeCrN1eznXH3PPm-H"
url_translate = "https://api.eu-gb.language-translator.watson.cloud.ibm.com/instances/1088ef74-1c3a-4b44-bd2e-66e84164d229/v3/translate?version=2018-05-01"

ANGER_THRESHOLD = 0.7

# send request to IBM for STT
def speech_to_text(file):
    headers = {
        'Content-Type': 'audio/flac',
    }
    # data = open(file, 'rb').read()
    response = requests.post(url_STT, headers=headers, data=file, auth=('apikey', API_key_STT))
    return response.json()['results'][0]['alternatives'][0]['transcript']


# send request to IBM for NLU
def analyze_tone(text):
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('version', '2019-07-12'),
    )
    data_json = {
        "text": text,
        "features": {
            "emotion": {}
        }
    }

    response = requests.post(url_NLU, headers=headers, params=params, json=data_json,
                             auth=('apikey', API_key_NLU))
    anger = response.json()['emotion']['document']['emotion']['anger']
    return anger


# send request to IBM for translation
def translate_to_german(text):
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('version', '2018-05-01'),
    )
    json_data = {
        'text': [text],
        'model_id': 'en-de',
    }

    response = requests.post(url_translate, headers=headers, params=params, json=json_data,
                             auth=('apikey', API_key_translate))

    translation = response.json()['translations'][0]['translation']
    return translation


def translate_to_french(text):
    headers = {
        'Content-Type': 'application/json',
    }
    params = (
        ('version', '2018-05-01'),
    )
    json_data = {
        'text': [text],
        'model_id': 'en-fr',
    }

    response = requests.post(url_translate, headers=headers, params=params, json=json_data,
                             auth=('apikey', API_key_translate))

    translation = response.json()['translations'][0]['translation']
    return translation


def save_comment_to_db(english_text, german_text, french_text, user, movie_id):
    Comment.objects.create(writer=user,
                           movie_id=movie_id,
                           comment_in_english=english_text,
                           comment_in_german=german_text,
                           comment_in_french=french_text)


def run_IBM_services(username, voice_file, movie_id):
    comment_text = speech_to_text(voice_file)
    print('plain commet: ', comment_text)
    anger = analyze_tone(comment_text)
    print('anger level: ', anger)
    if anger < ANGER_THRESHOLD:
        # comment is safe and we can save it
        comment_in_german = translate_to_german(comment_text)
        print('german: ', comment_in_german)
        comment_in_french = translate_to_french(comment_text)
        print('french: ', comment_in_french)

        save_comment_to_db(comment_text, comment_in_german, comment_in_french, username, movie_id)
