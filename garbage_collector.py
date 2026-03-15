import boto3

def find_unattached_volumes(region='us-east-2'):
    """Finds EBS volumes with 'available' status (not attached to any instance)."""
    ec2 = boto3.client('ec2', region_name=region)

    # Filter only volumes that are available (not in use)
    volumes = ec2.describe_volumes(Filters=[{'Name': 'status', 'Values': ['available']}])

    unattached_volumes = []
    for volume in volumes['Volumes']:
        unattached_volumes.append({
            'VolumeId': volume['VolumeId'],
            'Size': volume['Size'],
            'Type': volume['VolumeType'],
            'CreationTime': volume['CreateTime'].strftime("%Y-%m-%d %H:%M:%S")
        })

    return unattached_volumes

if __name__ == '__main__':
    print("Scanning for unused EBS volumes...")
    volumes_to_delete = find_unattached_volumes()

    if not volumes_to_delete:
        print("No orphaned volumes found. The environment is clean!")
    else:
        print(f"Warning: Found {len(volumes_to_delete)} volumes generating cost with no use:")
        for vol in volumes_to_delete:
            print(f" - ID: {vol['VolumeId']} | Size: {vol['Size']}GB | Created at: {vol['CreationTime']}")

        # In a real automation scenario, you would use:
        # ec2.delete_volume(VolumeId=vol['VolumeId'])