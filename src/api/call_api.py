import requests
from helpers import json
from constants import API_BASE_URL, API_KEY
from helpers.class_dict import ClassDictionary


class Requester:
    def __init__(self, base_url="", return_as_class=False):
        self.base = base_url
        self.return_as_class = return_as_class
        self.headers = { "Authozization": API_KEY }

    def decode(self, status, text):
        if status < 200 or status > 299:
            return

        dictionary = json.decode(text)

        if not self.return_as_class:
            return dictionary

        return ClassDictionary(dictionary)

    def get_url(self, url):
        return self.base + "/" + url

    def get(self, url=""):
        result = requests.get(self.get_url(url), headers=self.headers)
        text = result.text

        return self.decode(result.status_code, text)

    def post(self, url="", payload={}):
        result = requests.post(self.get_url(url), json=payload, headers=self.headers)
        text = result.text

        return self.decode(result.status_code, text)

    def put(self, url="", payload={}):
        result = requests.put(self.get_url(url), json=payload, headers=self.headers)
        text = result.text

        return self.decode(result.status_code, text)

    def patch(self, url="", payload={}):
        result = requests.patch(self.get_url(url), json=payload, headers=self.headers)
        text = result.text

        return self.decode(result.status_code, text)

    def delete(self, url=""):
        result = requests.delete(self.get_url(url), headers=self.headers)
        text = result.text

        return self.decode(result.status_code, text)

class BaseAPI:
    def __init__(self, entity):
        self.requester = Requester(API_BASE_URL + entity, True)

    def get_all(self):
        return self.requester.get()

    def get_one(self, pk):
        return self.requester.get("%s/" % pk)

    def create(self, **data):
        return self.requester.post(payload=data)

    def update(self, pk, **data):
        return self.requester.put("%s/" % pk, data)

    def partial_update(self, pk, **data):
        return self.requester.patch("%s/" % pk, data)

    def delete(self, pk):
        return self.requester.delete("%s/" % pk)
