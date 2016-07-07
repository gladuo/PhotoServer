# coding=utf-8

import requests
import json
from contextlib import closing

HOST = 'http://127.0.0.1:5000'
URL = HOST + '/api/get'


def fetch_url():
    response = requests.get(URL)
    info = json.loads(response.text)
    filename = info['file_name']
    src = info['src']
    return filename, HOST+src


def download():
    filename, src = fetch_url()
    with closing(requests.get(url=src, stream=True)) as response:
        chunk_size = 1024
        content_size = int(response.headers['content-length'])
        chunk_size = min(chunk_size, content_size)
        with open('./newest.png', "wb") as file:
            for data in response.iter_content(chunk_size=chunk_size):
                file.write(data)


if __name__ == '__main__':
    download()
