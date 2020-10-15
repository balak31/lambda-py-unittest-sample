import sys
import StringIO
import unittest

from moto import mock_s3

from sample_project.s3 import get_client, list_s3_buckets, list_s3_objects, \
    read_s3_object, main


class S3TestCase(unittest.TestCase):

    def setUp(self):
        """
        setUp will run before execution of each test case
        """

        self.bucket = 'static'
        self.key = 'style.css'
        self.value = 'value'

    @mock_s3
    def __moto_setup(self):
        """
        Simulate s3 file upload
        """

        s3 = get_client()
        s3.create_bucket(Bucket=self.bucket)
        s3.put_object(Bucket=self.bucket, Key=self.key, Body=self.value)

    def tearDown(self):
        """
        tearDown will run after execution of each test case
        """
        pass

    def test_get_client(self):
        """
        check that out get_client function has a valid endpoint
        """

        s3 = get_client()
        self.assertEqual(s3._endpoint.host, 'https://s3.amazonaws.com')

    @mock_s3
    def test_list_s3_buckets(self):
        """
        check that our bucket shows as expected
        """

        # setup s3 environment
        self.__moto_setup()

        buckets = [b for b in list_s3_buckets()]
        self.assertTrue(self.bucket in buckets)

    @mock_s3
    def test_list_s3_objects(self):
        """
        check that object is in bucket as expected
        """

        # setup s3 environment
        self.__moto_setup()

        objects = [o for o in list_s3_objects(self.bucket)]
        self.assertTrue(self.key in objects)

    @mock_s3
    def test_read_s3_object(self):
        """
        check the objects content is as expected
        """

        # setup s3 environment
        self.__moto_setup()

        content = read_s3_object(self.bucket, self.key)
        self.assertTrue(self.value == content)

    @mock_s3
    def test_main(self):
        """
        verifies the execution of the main function
        """

        # setup s3 environment
        self.__moto_setup()

        # capture stdout for processing
        sys.stdout = mystdout = StringIO.StringIO()

        # run main function
        main()

        # store stdout
        content = mystdout.getvalue()

        self.assertTrue('[ {} ]'.format(self.bucket) in content)
        self.assertTrue('=> {}'.format(self.key) in content)
