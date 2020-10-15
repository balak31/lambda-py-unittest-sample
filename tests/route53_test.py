import sys
import StringIO
import unittest

from moto import mock_route53

from sample_project.route53 import get_client, list_route53_zones, \
    list_route53_record_sets, main


class Route53TestCase(unittest.TestCase):

    def setUp(self):
        """
        setUp will run before execution of each test case
        """

        self.zone_name = 'example.com'
        self.record_name = 'www.example.com'

        self.record_set = {
            'Name': self.record_name,
            'ResourceRecords': [
                {'Value': '1.1.1.1'}
            ],
            'TTL': 300,
            'Type': 'A'
        }

    @mock_route53
    def __moto_setup(self):
        """
        Simulate route53 zone and record creation
        """

        # create the hosted zone using moto
        route53 = get_client()
        response = route53.create_hosted_zone(
            Name=self.zone_name, CallerReference='None')

        # assign the newly created zone_id
        self.zone_id = response['HostedZone']['Id']

        # create the new record set change request
        change = [dict(Action='CREATE', ResourceRecordSet=self.record_set)]
        changes = dict(Changes=change)

        # add a new record set to the hosted zone using change request
        route53.change_resource_record_sets(
            HostedZoneId=self.zone_id, ChangeBatch=changes)

    def tearDown(self):
        """
        tearDown will run after execution of each test case
        """
        pass

    def test_get_client(self):
        """
        check that out get_client function has a valid endpoint
        """

        route53 = get_client()
        self.assertEqual(
            route53._endpoint.host, 'https://route53.amazonaws.com')

    @mock_route53
    def test_list_route53_zones(self):
        """
        check that our zones shows as expected
        """

        # setup route53 environment
        self.__moto_setup()

        zones = [z[1] for z in list_route53_zones()]
        self.assertTrue(self.zone_name in zones)

    @mock_route53
    def test_list_route53_record_sets(self):
        """
        check that record is in zone
        """

        # setup route53 environment
        self.__moto_setup()

        records = [record for record in list_route53_record_sets(self.zone_id)]
        self.assertTrue(self.record_name in records)

    @mock_route53
    def test_main(self):
        """
        verifies the execution of the main function
        """

        # setup route53 environment
        self.__moto_setup()

        # capture stdout for processing
        sys.stdout = mystdout = StringIO.StringIO()

        # run main function
        main()

        # store stdout
        content = mystdout.getvalue()

        self.assertTrue('[ {} ]'.format(self.zone_name) in content)
        self.assertTrue('=> {}'.format(self.record_name) in content)
