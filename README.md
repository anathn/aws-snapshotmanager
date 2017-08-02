# aws-snapshotmanager
Serverless (Lambda) EBS Snapshot Manager

## Overview
The AWS Cloud Formation for this utility will create a Lambda function (Snapshot Manager) and a CloudWatch trigger.  By default, CloudWatch will trigger the Snapshot Manager every minute. The Snap Shot Manger will then look through the region for instances tagged with 'snapshot'.  It will then check the value of that tag for when to snapshot the volumes attached to that instance, then create any snapshots that fall into the time slot. Finally, it will cleanup any snapshots that have expired or are past the retention value.

## Deployment
Setting up using the AWS cli:
```
aws cloudformation create-stack --stack-name aws-snapshotmanager --template-body file://cf-snapshotmanager.yaml
```
Tearing down using the AWS cli:
```
aws cloudformation delete-stack --stack-name aws-snapshotmanager
```

Or just log into the AWS console and deploy it there.

## The Snapshot Tag Format
In order for the Snapshot Manager to find your instance, you need to add a specific tag with a formatted value. The tag key is configurable by modifying the line:

```tag_names = ['snapshot', 'Snapshot', 'SNAPSHOT']```

Or just add a tag with the key using the default value `snapshot` with the proper value formatting.  The value should be padded-0 runtimes, separated by commas, in parentheses, followed by the retention value. The retention value is the number of snapshots to keep per attached volume.

Example:

```(05:00,10:00,14:05)21```

The example will create a snapshot at 5am, 10am, and 2:05pm and will keep 21 snapshots per volume. Because it triggers three times a day, the value 21 will cover the instance for an entire week. Also note that Lambda uses **UTC Time** when you setup your tags.

NOTE: For the minute value to work the Snapshot Manager must run during that minute. This means if your Cloud Watch rule runs every hour the only values that will work would be the top of the hour values. Missed time windows are forever missed.

## Saving a snapshot
To prevent Snapshot Manager from deleting a snapshot add the tag ```preserve_snapshot```. Just the presence of this tag will forever prevent the snapshot from being deleted, and it will not count against the retention number.  If you add a date in the value field the snapshot will be deleted ON that date - regardless of the retention value.

Example:

Tag:```preserve_snapshot```  Value:```2017-12-31```

This tag will save that snapshot until December 31, 2017.  On that day at midnight the snapshot will be deleted.

## TODO ##
* Cron-format for snapshot scheduling
* Snapshot Creation verification
* Add parameters to Cloud Formation (trigger intervals, etc.)
