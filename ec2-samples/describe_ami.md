This code describes AMIs available to you across all regions.


```
{
    'Images': [
        {
            'Architecture': 'i386'|'x86_64'|'arm64',
            'CreationDate': 'string',
            'ImageId': 'string',
            'ImageLocation': 'string',
            'ImageType': 'machine'|'kernel'|'ramdisk',
            'Public': True|False,
            'KernelId': 'string',
            'OwnerId': 'string',
            'Platform': 'Windows',
            'ProductCodes': [
                {
                    'ProductCodeId': 'string',
                    'ProductCodeType': 'devpay'|'marketplace'
                },
            ],
            'RamdiskId': 'string',
            'State': 'pending'|'available'|'invalid'|'deregistered'|'transient'|'failed'|'error',
            'BlockDeviceMappings': [
                {
                    'DeviceName': 'string',
                    'VirtualName': 'string',
                    'Ebs': {
                        'DeleteOnTermination': True|False,
                        'Iops': 123,
                        'SnapshotId': 'string',
                        'VolumeSize': 123,
                        'VolumeType': 'standard'|'io1'|'gp2'|'sc1'|'st1',
                        'Encrypted': True|False,
                        'KmsKeyId': 'string'
                    },
                    'NoDevice': 'string'
                },
            ],
            'Description': 'string',
            'EnaSupport': True|False,
            'Hypervisor': 'ovm'|'xen',
            'ImageOwnerAlias': 'string',
            'Name': 'string',
            'RootDeviceName': 'string',
            'RootDeviceType': 'ebs'|'instance-store',
            'SriovNetSupport': 'string',
            'StateReason': {
                'Code': 'string',
                'Message': 'string'
            },
            'Tags': [
                {
                    'Key': 'string',
                    'Value': 'string'
                },
            ],
            'VirtualizationType': 'hvm'|'paravirtual'
        },
    ]
}
```
