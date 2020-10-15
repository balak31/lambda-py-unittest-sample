import boto3


def get_client():
    """
    Returns the s3 boto3 client
    """

    return boto3.client('s3')


def list_s3_buckets():
    """
    List s3 bucket names
    """

    s3 = get_client()

    response = s3.list_buckets()
    if response:
        for bucket in response.get('Buckets', []):
            yield bucket['Name']


def list_s3_objects(bucket):
    """
    List s3 objects in a bucket
    """

    s3 = get_client()

    response = s3.list_objects(Bucket=bucket)
    if response:
        for _object in response.get('Contents', []):
            yield _object['Key']


def read_s3_object(bucket, key):
    """
    Returns the content of a s3 file
    """

    s3 = get_client()

    response = s3.get_object(Bucket=bucket, Key=key)
    if response:
        return response['Body'].read()


def main():
    """
    Main entry
    """

    # loop over all the s3 buckets in the account
    for bucket in list_s3_buckets():

        # print out bucket name
        print '[ {} ]'.format(bucket)

        # loop over all keys for a given bucket
        for key in list_s3_objects(bucket):
            print ' => {}'.format(key)
