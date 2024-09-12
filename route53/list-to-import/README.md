# list-to-import

## Description

This small tool gets the output of the command 
`aws route53 list-resource-record-sets` and converts it to the input used by the
command `aws route53 change-resource-record-sets`.

It is designed to ease the migration one hosted domain from one account to 
another.

## Usage

Copy the script `list-to-import.py` to any location in your disk.

Export the source domain list with the command:

```
aws route53 list-resource-record-sets --hosted-zone-id hosted-zone-id > path-to-list-file.json
```

Convert it to required input file by using the command:

```
python list-to-import.py -i path-to-list-file.json -o path-to-change-file.json
```

Import the new entries into the new account with the command:

```
aws route53 change-resource-record-sets --hosted-zone-id id-of-new-hosted-zone --change-batch file://path-to-change-file.json
```

To check the results, use the command on the new account:

```
aws route53 list-resource-record-sets --hosted-zone-id hosted-zone-id > path-to-new-list-file.json
```

and compare `path-to-new-list-file.json` with `path-to-list-file.json`. If every
thing is correct, the only differences will be on the records of type `SOA` and `NS` that are filtered out by `list-to-import.py`.

## Dependencies

This script requires only Python 3.11 without any additional dependencies.

## References

1. [Migrating a hosted zone to a different AWS account - docs.aws.amazon.com](https://docs.aws.amazon.com/Route53/latest/DeveloperGuide/hosted-zones-migrating.html#hosted-zones-migrating-create-file)