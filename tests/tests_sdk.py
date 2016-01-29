"""
Tests for Copyleaks SDK. Please use your credentials. Also, kind keep in mind that probably we cannot run these
tests periodically because limited number of credits available for free accounts.
"""
import unittest
from copyleaks_sdk.copyleaks import CopyLeaks
from config import username, api_key
class CopyleaksTests(unittest.TestCase):

    def setUp(self):
        """
        Define a file named 'config.py' under e.g. tests/config.py and put your
        api_key and username in that file
        :return:
        """
        self.api_key = api_key
        self.username = username
        self.copyleak = CopyLeaks(self.username, self.api_key, test_mode=True)

    def test_count_credits(self):
        credit = self.copyleak.count_credits()
        assert 'Amount' in credit and credit['Amount'] > 0, "Oops, credits expired."

    def test_create_process_by_file(self):
        response = self.copyleak.create_process_by_file('test_file.txt')
        assert 'CreationTimeUTC' in response
        assert 'ProcessId' in response
        process_id = response['ProcessId']
        response = self.copyleak.get_process_status(process_id)
        assert 'Status' in response
        # Now get all processes
        response = self.copyleak.get_all_processes()
        record = [record for record in response if record['ProcessId'] == process_id][0]
        assert 'ProcessId' in record and 'Status' in record


    def test_create_process_by_ocr(self):
        response = self.copyleak.create_process_by_ocr('ocr_test.jpeg')
        assert 'CreationTimeUTC' in response
        assert 'ProcessId' in response
        process_id = response['ProcessId']
        response = self.copyleak.get_process_status(process_id)
        assert 'Status' in response
        # Now get all processes
        response = self.copyleak.get_all_processes()
        record = [record for record in response if record['ProcessId'] == process_id][0]
        assert 'ProcessId' in record and 'Status' in record



    def test_create_process_by_url(self):
        response = self.copyleak.create_process_by_url('http://www.newyorker.com/magazine/1981/12/14/a-i')
        assert 'CreationTimeUTC' in response
        assert 'ProcessId' in response
        process_id = response['ProcessId']
        response = self.copyleak.get_process_status(process_id)
        assert 'Status' in response
        # Now get all processes
        response = self.copyleak.get_all_processes()
        record = [record for record in response if record['ProcessId'] == process_id][0]
        assert 'ProcessId' in record and 'Status' in record


if __name__ == "__main__":
    unittest.main()
