"""
Python SDK for Copyleaks. More details can be read at https://api.copyleaks.com/Documentation.
First register on Copyleaks and get the API key.
"""

import requests
import json
import os
from retrying import retry


class CopyLeaks(object):
    def __init__(self, username, api_key, **kwargs):
        """
        Creates a Copyleak object which is used to make calls
        :param username: Username used to login
        :param api_key: API key used to make calls
        :param kwargs:
        :return:
        """
        self.api_key = api_key
        self.username = username
        self.base_url = kwargs.get('base_url') or 'https://api.copyleaks.com'
        self.headers = kwargs.get('headers') or {'content-type': 'application/json'}
        self.access_token = None
        self.test_mode = kwargs.get('test_mode') or False
        self._login()

    @retry
    def _login(self):
        """
        Does the login and saves access token for subsequent requests
        :return:
        """
        assert self.api_key and self.username
        url = self.base_url + '/v1/account/login'
        data = dict(
            Username=self.username,
            Apikey=self.api_key

        )
        data = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=data)
        assert response.status_code == 200
        self.access_token = response.json()['access_token']
        self._set_headers()

    def _set_headers(self):
        assert self.access_token
        self.headers['Authorization'] = 'Bearer %s' % self.access_token
        if self.test_mode:
            self.headers['copyleaks-sandbox-mode'] = ''

    @retry
    def count_credits(self):
        """
        Counds credits and returns a response of the form:
        {
          "Amount": 1
        }
        :return:
        """
        url = self.base_url + '/v1/account/count-credits'
        response = requests.get(url, headers=self.headers)
        assert 'Amount' in response.json()
        return response.json()

    @retry
    def create_process_by_url(self, url_to_process):
        """
        Creates a process by scanning a URL and returns a response of the following format:
        {
          "ProcessId": "1074ae9d-ec1c-46ff-adc2-c294abed29f3",
          "CreationTimeUTC": "01/01/2016 18:36:10"
        }
        :param url: URL to scan
        :return:
        """
        assert url_to_process
        url = self.base_url + '/v1/detector/create-by-url'
        data = dict(
            Url=url_to_process
        )
        data = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=data)
        assert response.status_code == 200
        assert 'ProcessId' in response.json()
        assert 'CreationTimeUTC' in response.json()
        return response.json()

    @retry
    def _upload_file(self, url, file_path):
        """
        Uploads a file for processing.
        :param url: URL to hit e.g. either 'create-by-file' or 'create-by-ocr'
        :param file_path: Valid file path
        :return:
        """
        file_name, file_extension = os.path.splitext(file_path)
        valid_extensions = ['.html', '.txt', '.pdf', '.docx', '.doc', '.rtef', '.jpeg']
        assert file_extension in valid_extensions
        if file_extension == '.jpeg':
            files = {'media': (file_path, open(file_path, 'rb').read())}
        else:
            files = {'file': (file_path, open(file_path, 'rb').read())}
        headers = self.headers.copy()
        headers.pop('content-type')
        response = requests.post(url, headers=headers, files=files)
        assert 'CreationTimeUTC' in response.json()
        assert 'ProcessId' in response.json()
        assert response.status_code == 200
        return response.json()

    @retry
    def create_process_by_file(self, file_path):
        """
        Creates a process by uploading a file to scan. Returns a response of the format:
        {
          "ProcessId": "23af0314-2fb9-4b91-959f-87848572df1f",
          "CreationTimeUTC": "01/01/2016 18:36:10"
        }
        :param file_path: Valid file path
        :return:
        """
        assert file_path
        assert os.path.isfile(file_path)
        
        url = self.base_url + '/v1/detector/create-by-file'
        return self._upload_file(url, file_path)

    @retry
    def create_process_by_ocr(self, file_path, language='English'):
        """
        Creates a process by uploading a file to scan. Returns a response of the format:
        {
          "ProcessId": "23af0314-2fb9-4b91-959f-87848572df1f",
          "CreationTimeUTC": "01/01/2016 18:36:10"
        }
        :param file_path: Valid file path
        :param language: OCR language codes as given here https://api.copyleaks.com/Documentation/OcrLanguages
        :return:
        """
        assert file_path and language
        url = self.base_url + ('/v1/detector/create-by-file-ocr?language=%s' % language)
        return self._upload_file(url, file_path)

    @retry
    def get_process_status(self, process_id):
        """
        Gets the scan progress and response looks like:
        {
          "Status": "Processing",
          "ProgressPercents": 50
        }
        :param process_id: A valid active process id
        :return:
        """
        assert process_id
        url = self.base_url + ('/v1/detector/%s/status' % (process_id))
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        assert 'ProgressPercents' in response.json()
        assert 'Status' in response.json()
        return response.json()

    @retry
    def get_process_result(self, process_id):
        """
        Gets the scan result and response looks like:
        [
          {
            "URL": "http://site1.com/result",
            "Percents": 99,
            "NumberOfCopiedWords": 250
          },
          {
            "URL": "http://site2.com/result",
            "Percents": 50,
            "NumberOfCopiedWords": 162
          }
        ]
        :param process_id: A valid active process id
        :return:
        """
        assert process_id
        url = self.base_url + ('/v1/detector/%s/result' % (process_id))
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        return response.json()

    @retry
    def get_all_processes(self):
        """
        Retusn list of all active processes. Response looks like:
        [
              {
                "ProcessId": "e4d544af-da8c-4767-8dd0-f044191fa161",
                "CreationTimeUTC": "01/01/2016 18:36:10",
                "Status": 0,
                "CustomFields": {
                  "key 1": "sample string 1",
                  "key 2": "sample string 2"
                }
              },
              {
                "ProcessId": "ai282ns9-1jss-2918-11ks-sj29s2992kk1",
                "CreationTimeUTC": "02/02/2016 11:31:20",
                "Status": 0,
                "CustomFields": {
                  "key 3": "sample string 3",
                  "key 4": "sample string 4"
                }
              }
            ]
        :return:
        """
        url = self.base_url + '/v1/detector/list'
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        return response.json()

    @retry
    def delete_process(self, process_id):
        """
        Deletes a process and returns status code of 200 in case of success.
        :param process_id: A valid active process id
        :return:
        """
        assert process_id
        url = self.base_url + ('/v1/detector/%s/delete' % (process_id))
        response = requests.delete(url, headers=self.headers)
        assert response.status_code == 200

