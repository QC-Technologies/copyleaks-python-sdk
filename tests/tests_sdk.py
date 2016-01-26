"""
Tests for Copyleaks SDK. Please use your credentials. Also, kind keep in mind that probably we cannot run these
tests periodically because limited number of credits available for free accounts.
"""
import unittest
from copyleaks_sdk.copyleaks import CopyLeaks

class CopyleaksTests(unittest.TestCase):

    def setUp(self):
        # Your API Key here
        self.api_key = '933a0d87-f268-538d-403f-f612ca4802b0'
        # Your username here
        self.username = 'wyounas6'
        self.copyleak = CopyLeaks(self.username, self.api_key)
        credit = self.copyleak.count_credits()
        assert 'Amount' in credit and credit['Amount'] > 0, "Oops, credits expired."
        self.process_id = None


    def test_create_process_by_file(self):
        response = self.copyleak.create_process_by_file('test_file.txt')
        assert 'CreationTimeUTC' in response.json()
        assert 'ProcessId' in response.json()
        self.process_id = response.json()['ProcessId']
        response = self.copyleak.get_process_status(self.process_id)
        assert 'Status' in response
        # Now get all processes
        response = self.copyleak.get_all_processes()
        record = [record for record in response if record['ProcessId'] == self.process_id][0]
        assert 'ProcessId' in record and 'Status' in record


    def test_create_process_by_url(self):
        response = self.copyleak.create_process_by_url('http://www.newyorker.com/magazine/1981/12/14/a-i')
        assert 'CreationTimeUTC' in response
        assert 'ProcessId' in response
        self.process_id = response['ProcessId']
        response = self.copyleak.get_process_status(self.process_id)
        assert 'Status' in response
        # Now get all processes
        response = self.copyleak.get_all_processes()
        record = [record for record in response if record['ProcessId'] == self.process_id][0]
        assert 'ProcessId' in record and 'Status' in record


if __name__ == "__main__":
    unittest.main()


