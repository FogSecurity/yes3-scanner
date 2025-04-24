# YES3 Scanner: Yet Another S3 Scanner

YES3 scans an AWS Account for potential S3 security issues in the following categories:

* Access Issues such as Public Access
* Preventative S3 Security Settings
* Additional Security such as Encryption
* Ransomware Protection, Data Protection, and Recovery

For help or feedback, contact us at [info@fogsecurity.io](mailto:info@fogsecurity.io).  We are continuing to build in this space and are developing a more comprehensive scanner with multi-account (Organization) and object-level scanning.  If you're interested in joining a private beta, reach out to us.

Blog Post: [fogsecurity.io/blog/yes3-amazon-s3](http://www.fogsecurity.io/blog/yes3-amazon-s3)

## Checks

YES3 Scanner checks for the following S3 configuration items:

### Access Issues and Public Access
- Bucket Access Control Lists (ACLs)
- Bucket Policy (Resource-Based Policy)
- Bucket Website Settings

#### Preventative S3 Security Settings
- Account Public Access Block
- Bucket Public Access Block
- Disabled ACLs (via Ownership Controls)

#### Additional Security
- Bucket Encryption Settings
- S3 Server Access Logging

#### Ransomware Protection & Recovery
- Object Lock Configuration
- Bucket Versioning Settings
- Bucket Lifecycle Configuration

## Running YES3 Scanner

```
python3 yes3.py --profile <your_profile_here>
```

Note: While S3 is global, certain clients in AWS's boto3 require regions such as Service Quotas, S3 Control, and STS.  YES3 Scanner uses Service Quotas to check for bucket limits and the global limit only shows up in us-east-1.  Due to this, YES3 scanner will use `us-east-1 ` as the default region for Service Quotas, STS, and S3 Control. YES3 Scanner will account for buckets in all regions due to the global nature of S3.  Thus, YES3's API calls will be in CloudTrail in us-east-1.

Example output:

```
YES3 SCANNER RESULTS
----------------------------
AWS Account: 123412341234
Account Settings
Account Block Public Access Overall Status: OK
----------------------------
Bucket Summary
Total Buckets: 14
----------------------------
Buckets potentially public: 3
fog-pub-sample-bucket | Public Method: ['acl']
fog-pub-sample | Public Method: ['policy', 'acl]
fog-pub-policy-sample | Public Method: ['policy']
----------------------------
Buckets with Access Issues: 1
sample-locked-bucket
----------------------------
Buckets with default S3-Owned Encryption: 6
Buckets with a Block Public Access setting disabled: 3
Buckets with Bucket ACLs Enabled: 2
Buckets with ACLs set to public: 0
Buckets with Bucket Policy set to public: 1
Buckets with Object Lock disabled: 5
Buckets with Versioning disabled: 4
Buckets with Lifecycle Config Set to Expiration: 1
Buckets with Public Access from Website Setting: 0
Buckets with Server Access Logs Disabled: 5
----------------------------
Additional Bucket Details
Buckets with default S3-Owned Encryption: sample-bucket-1, sample-bucket-2, sample-bucket-3, sample-bucket-4, sample-bucket-5, sample-bucket-6

Buckets with a Block Public Access setting disabled: sample-bucket-1, sample-bucket-2, sample-bucket-3

Buckets with Bucket ACLs Enabled: sample-bucket-1, sample-bucket-2

Buckets with ACLs set to public: 

Buckets with Bucket Policy set to public: sample-bucket-1

Buckets with Object Lock disabled: sample-bucket-1, sample-bucket-2, sample-bucket-3, sample-bucket-4, sample-bucket-5

Buckets with Versioning disabled: sample-bucket-1, sample-bucket-2, sample-bucket-3, sample-bucket-4

Buckets with Lifecycle Config Set to Expiration: sample-bucket-7

Buckets with Public Access from Website Setting:

Buckets with Server Access Logs Disabled: sample-bucket-1, sample-bucket-2, sample-bucket-3, sample-bucket-4, sample-bucket-5


``` 

## Installing YES3 Scanner and Requirements

- Python 3 and AWS's boto3 library are required.
- AWS credentials and appropriate access are needed to run YES3.  For more information about IAM Requirements for this tool, see our [IAM documentation](iam/iam.md) which details how to install IAM for YES3 and required IAM permissions.

Requirements can be installed via pip3 install and the requirements.txt file. A python virtual environment can be used if desired.

```
pip3 install -r requirements.txt
```

For information on configuring your AWS Credentials, see AWS's documentation [here](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-quickstart.html)

## Contact

Contact us at info@fogsecurity.io for support and more information.
