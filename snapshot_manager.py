import boto3
from time import strftime

ec = boto3.client('ec2')
tag_names = ['snapshot', 'Snapshot', 'SNAPSHOT']

def lambda_handler(event, context):
    current_time = strftime("%H:%M")
    reservations = ec.describe_instances(
        Filters=[
            {'Name': 'tag-key', 'Values': tag_names},
        ]
    ).get(
        'Reservations', []
    )

    instances = sum(
        [
            [i for i in r['Instances']]
            for r in reservations
        ], [])

    print "Checking %d instances..." % len(instances)

    for instance in instances:
        lower_tags = {tag['Key']:  tag['Value'] for tag in instance['Tags']}
        params = lower_tags['snapshot'].replace('(','').split(')')
        trigger_times = params[0].split(',')
        retention_days = params[1]
        if cur_time not in trigger_times:
            continue

        for dev in instance['BlockDeviceMappings']:
            if dev.get('Ebs', None) is None:
                continue
            vol_id = dev['Ebs']['VolumeId']
            print "Found EBS volume %s on instance %s" % (
                vol_id, instance['InstanceId'])

            ec.create_snapshot(
                VolumeId=vol_id,
            )
