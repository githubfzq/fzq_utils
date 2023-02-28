import requests
from .. import config

def save_to_flomo(text: str):
    url = config.get('flomo', 'url')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {config.FLOMO_TOKEN}'
    }
    data = {
        'text': text
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code!= 200:
        raise Exception(f'Failed to save to flomo: {response.status_code}')