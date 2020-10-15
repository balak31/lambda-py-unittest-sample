import boto3


def get_client():
    """
    Returns the s3 boto3 client
    """

    return boto3.client('route53')


def list_route53_zones():
    """
    List route53 zone ids
    """

    route53 = get_client()

    response = route53.list_hosted_zones()
    if response:
        for zone in response.get('HostedZones', []):
            yield zone['Id'], zone['Name']


def list_route53_record_sets(zone_id):
    """
    List route53 record names for zone
    """

    route53 = get_client()

    response = route53.list_resource_record_sets(HostedZoneId=zone_id)
    if response:
        for record in response.get('ResourceRecordSets', []):
            yield record['Name']


def main():
    """
    Main entry
    """

    # loop over all the route53 zones
    for zone_id, zone_name in list_route53_zones():

        # print zone name
        print '[ {} ]'.format(zone_name)

        # loop over records for our zone
        for record in list_route53_record_sets(zone_id):
            print ' => {}'.format(record)
