from pathlib import Path
import requests
from ..config import get_flomo_url


def save_to_flomo(text: str):
    url = get_flomo_url()
    response = requests.post(url, json={"content": text})
    if response.status_code != 200:
        raise Exception(f"Failed to save to flomo: {response.status_code}")


def save_file_to_flomo(file_path: Path):
    text = file_path.read_text()
    save_to_flomo(text)


def save_dir_to_flomo(dir_path: Path):
    for file_path in dir_path.iterdir():
        try:
            save_file_to_flomo(file_path)
        except UnicodeDecodeError as e:
            print(f"Failed to save file {file_path.name}.")
