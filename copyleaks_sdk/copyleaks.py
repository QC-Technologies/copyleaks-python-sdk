"""

"""
import requests
import json
import os


class CopyLeaks(object):
    def __init__(self, username, api_key, **kwargs):
        self.api_key = api_key
        self.username = username
        self.base_url = kwargs.get('base_url') or 'https://api.copyleaks.com'
        self.headers = kwargs.get('headers') or {'content-type': 'application/json'}
        self.access_token = None
        self.login()

    def login(self):
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
        self._set_authorized_headers()

    def _set_authorized_headers(self):
        assert self.access_token
        self.headers['Authorization'] = 'Bearer %s' % self.access_token

    def count_credits(self):
        url = self.base_url + '/v1/account/count-credits'
        response = requests.get(url, headers=self.headers)
        assert 'Amount' in response.json()
        return response.json()

    def create_process_by_url(self, url):
        assert url
        url = self.base_url + '/v1/detector/create-by-url'
        data = dict(
            Url=url
        )
        data = json.dumps(data)
        response = requests.post(url, headers=self.headers, data=data)
        assert response.status_code == 200
        assert 'ProcessId' in response.json()
        assert 'CreationTimeUTC' in response.json()
        return response.json()

    def _upload_file(self, url, file_path):
        files = {'file': (file_path, open(file_path, 'rb').read())}
        headers = self.headers.copy()
        headers.pop('content-type')
        response = requests.post(url, headers=headers, files=files)
        assert 'CreationTimeUTC' in response.json()
        assert 'ProcessId' in response.json()
        assert response.status_code == 200
        return response


    def create_process_by_file(self, file_path):
        assert file_path
        assert os.path.isfile(file_path)
        
        url = self.base_url + '/v1/detector/create-by-file'
        return self._upload_file(url, file_path)

    def create_process_by_ocr(self, file_path):
        assert file_path
        url = self.base_url + '/v1/detector/create-by-ocr'
        return self._upload_file(url, file_path)

    def get_process_status(self, process_id):
        assert process_id
        url = self.base_url + ('/v1/detector/%s/status' % (process_id))
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        assert 'ProgressPercents' in response.json()
        assert 'Status' in response.json()
        return response.json()

    def get_process_result(self, process_id):
        assert process_id
        url = self.base_url + ('/v1/detector/%s/result' % (process_id))
        response = requests.get(url, headers=self.headers)
        assert response.status_code == 200
        assert 'NumberOfCopiedWords' in response.json()
        assert 'Percents' in response.json()
        assert 'URL' in response.json()
        return response.json()

    def get_all_processes(self):
        url = self.base_url + '/v1/detector/list'
        response = requests.get(url, header=self.headers)
        assert response.status_code == 200
        return response.json()

    def delete_process(self, process_id):
        assert process_id
        url = self.base_url + ('/v1/detector/%s/delete' % (process_id))
        response = requests.delete(url)
        assert response.status_code == 200











if __name__ == "__main__":
    api_key = '32a93db7-d309-87bf-e432-31c18df7fc13'
    leaks = CopyLeaks('wyounas', api_key)
    process_id = leaks.create_process_by_file('test_file.txt')['ProcessId']
    print leaks.get_process_status(process_id)
    print leaks.get_process_result(process_id)


