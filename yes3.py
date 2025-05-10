import boto3
import botocore
import argparse

def check_bucket_limit(session):
    
    #Service Quota Code: L-DC2B2D3D
    #Hardcoded region for us-east-1 to see Global Quota for S3 Buckets
    sq_client = session.client('service-quotas', 'us-east-1')

    try:
        response = sq_client.get_service_quota(
            ServiceCode='s3',
            QuotaCode='L-DC2B2D3D'
        )

        if response['Quota']['Value'] > 10000:
            print("NOTE: There may be more buckets in account due to a service limit increase that will not be scanned by YES3 Scanner.")

    except botocore.exceptions.ClientError as error:
        print("Error with Service Quotas, continuing scan")
    #Does not return utilization.

def access_issue(category, bucket):
    if access_issues.get(bucket):
        access_issues[bucket].append(category)
    else:
        access_issues.update({bucket: [category]})

def potential_public(bucket_results, account_results):

    #This does not account for Resource Control Policies.
    potential_public = []

    for bucket in bucket_results:
    #ACLs Enabled and Public ACLs and account BPA off and bucket BPA off
        public_reason = []
        if not account_results['AccountBlockPublicAccess']['IgnorePublicAcls']:
            if bucket['BucketACLEnabled'] == 'enabled' and bucket['BucketACL'] == 'public' and not bucket['BucketBPA']['IgnorePublicAcls']: 
                public_reason.append('acl')

        #Public Bucket Policy and account BPA off and bucket BPA off    
        if not account_results['AccountBlockPublicAccess']['RestrictPublicBuckets']:
            if bucket['BucketPolicyStatus'] == 'public' and not bucket['BucketBPA']['RestrictPublicBuckets']:
                public_reason.append('policy')
        
        if len(public_reason) > 0:
            potential_public.append({
                'bucket': bucket['Bucket'],
                'public': public_reason
            })

    return potential_public

def summarize_results(bucket_results, account_results, bucket_results_summary):
    #Process and print out results
    sts_client = session.client('sts', 'us-east-1')
    aws_account = sts_client.get_caller_identity()['Account']

    #Account Results
    print("YES3 SCANNER RESULTS")
    print("----------------------------")
    print("AWS Account: " + aws_account)
    print("Account Settings")

    if account_results['AccountBlockPublicAccess']['BlockPublicAcls'] and account_results['AccountBlockPublicAccess']['IgnorePublicAcls'] and account_results['AccountBlockPublicAccess']['BlockPublicPolicy'] and account_results['AccountBlockPublicAccess']['RestrictPublicBuckets']:
        print("Account Block Public Access Overall Status: " + "OK")
    else:
        print("Account Block Public Access Overall Status: " + "WARN")

    if account_results['AccountBlockPublicAccess']['BlockPublicAcls'] == False:
        account_BlockPublicAcls = "WARN"
        print("Account BPA Block Public ACLs " + "WARN")
    else:
        account_BlockPublicAcls = "OK"

    if account_results['AccountBlockPublicAccess']['IgnorePublicAcls'] == False:
        account_IgnorePublicAcls = "WARN"
        print("Account BPA Ignore Public ACLs: " + "WARN")
    else:
        account_IgnorePublicAcls = "OK"

    if account_results['AccountBlockPublicAccess']['BlockPublicPolicy'] == False:
        account_BlockPublicPolicy = "WARN"
        print("Account BPA Block Public Policy: " + "WARN")
    else:
        account_BlockPublicPolicy = "OK"

    if account_results['AccountBlockPublicAccess']['RestrictPublicBuckets'] == False:
        account_RestrictPublicBuckets = "WARN"
        print("Account BPA Restrict Public Buckets: " + "WARN")
    else:
        account_RestrictPublicBuckets = "OK"
        
    # Bucket Summary
    print("----------------------------")
    print("Bucket Summary")

    total_buckets = len(bucket_results)

    print("Total Buckets: " + str(total_buckets))
    print("----------------------------")

    potentially_public = potential_public(bucket_results, account_results)

    print("Buckets potentially public: " + str(len(potentially_public)))
    for bucket in potentially_public:
        print(bucket['bucket'] + " | Public Method: " + str(bucket['public']))

    print("----------------------------")
    print("Buckets with Visibility Issues: " + str(len(access_issues)))
    print(*access_issues.keys(), sep=', ')
    
    print("----------------------------")
    print("Buckets with default S3-Owned Encryption: " + str(len(bucket_results_summary['BucketEncryption'])))
    print("Buckets with a Block Public Access setting disabled: " + str(len(bucket_results_summary['BucketBPA'])))
    print("Buckets with Bucket ACLs Enabled: " + str(len(bucket_results_summary['BucketACLEnabled'])))
    print("Buckets with ACLs set to public: " + str(len(bucket_results_summary['BucketACL'])))
    print("Buckets with Bucket Policy set to public: " + str(len(bucket_results_summary['BucketPolicyStatus'])))
    print("Buckets with Object Lock disabled: " + str(len(bucket_results_summary['ObjectLock'])))
    print("Buckets with Versioning disabled: " + str(len(bucket_results_summary['Versioning'])))
    print("Buckets with Lifecycle Config Set to Expiration: " + str(len(bucket_results_summary['LifecycleConfig'])))
    print("Buckets with Public Access from Website Setting: " + str(len(bucket_results_summary['Website'])))
    print("Buckets with Server Access Logs Disabled: " + str(len(bucket_results_summary['AccessLogging'])))
    
    print("----------------------------")
    print("Additional Bucket Details")
    print("Buckets with default S3-Owned Encryption: ", end="")
    print(*bucket_results_summary['BucketEncryption'], sep=', ')
    print("\n" + "Buckets with a Block Public Access setting disabled: ", end="")
    print(*bucket_results_summary['BucketBPA'], sep=', ')
    print("\n" + "Buckets with Bucket ACLs Enabled: ", end="")
    print(*bucket_results_summary['BucketACLEnabled'], sep=', ')
    print("\n" + "Buckets with ACLs set to public: ", end="")
    print(*bucket_results_summary['BucketACL'], sep=', ')
    print("\n" + "Buckets with Bucket Policy set to public: ", end="")
    print(*bucket_results_summary['BucketPolicyStatus'], sep=', ')
    print("\n" + "Buckets with Object Lock disabled: ", end="")
    print(*bucket_results_summary['ObjectLock'], sep=', ')
    print("\n" + "Buckets with Versioning disabled: ", end="")
    print(*bucket_results_summary['Versioning'], sep=', ')
    print("\n" + "Buckets with Lifecycle Config Set to Expiration: ", end="")
    print(*bucket_results_summary['LifecycleConfig'], sep=', ')
    print("\n" + "Buckets with Public Access from Website Setting: ", end="")
    print(*bucket_results_summary['Website'], sep=', ')
    print("\n" + "Buckets with Server Access Logs Disabled: ", end="")
    print(*bucket_results_summary['AccessLogging'], sep=', ')


    #print("Recommendation: Use CMKs and non-transparent encryption if possible")
    #print("Recommendation: Ensure Block Public Access settings are all enabled for S3 Buckets")
    #print("Recommendation: Disable ACLs and use IAM to manage access to S3")
    #print("Recommendation: Ensure Block Public Access settings are all enabled for S3 Buckets")
    #print("Recommendation: Do not grant public access to S3 Buckets unless necessary")
    #print("Recommendation: Do not grant public access to S3 Buckets unless necessary")
    #print("Recommendation: Object Lock can help protect against ransomware and deletion of data")
    #print("Recommendation: Versioning can help protect against ransomware and deletion of data")
    #print("Recommendation: Lifecycle Configuration set to Expiration can make it easier for Ransomware to automatically delete data in S3")
    #print("Recommendation: Do not grant public access to S3 via S3 Website unless necessary")

def add_to_bucket_summary(category, bucket_name):
    bucket_results_summary[category].append(bucket_name)


parser = argparse.ArgumentParser(prog='YES3 Scanner') 
parser.add_argument("--profile")
parser.add_argument("--region")

args = parser.parse_args()
session = boto3.Session(profile_name = args.profile)

s3_client = session.client('s3')
s3_control_client = session.client('s3control', 'us-east-1')
# Account Configuration Checks
# Account Public Access Block 

sts_client = session.client('sts')
account = sts_client.get_caller_identity()['Account']

check_bucket_limit(session)

try:
    account_block_settings = s3_control_client.get_public_access_block(
        AccountId = account
    )

    account_results = {'AccountBlockPublicAccess': account_block_settings['PublicAccessBlockConfiguration']}

except botocore.exceptions.ClientError as error:
    account_results = []
    if error.response['Error']['Code'] == 'AccessDenied':
        print("Error with retrieving BPA settings for AWS Account")
    elif error.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
        account_results = {'AccountBlockPublicAccess':
            {'BlockPublicAcls': False,
            'IgnorePublicAcls': False,
            'BlockPublicPolicy': False,
            'RestrictPublicBuckets': False
            }}
    else:
        print("Error with Account BPA")
    

bucket_results = []

bucket_results_summary = {
    'BucketEncryption': [],
    'BucketBPA': [],
    'BucketACLEnabled': [],
    'BucketACL': [],
    'BucketPolicyStatus': [],
    'ObjectLock': [],
    "Versioning": [],
    "LifecycleConfig": [],
    "Website": [],
    "AccessLogging": []
    }

access_issues = {}

#Pagination is needed if quotas above 10,000

try:
    s3_buckets = s3_client.list_buckets()
except botocore.exceptions.ClientError as error:
    raise error

for bucket in s3_buckets['Buckets']:

    #TODO: Check Directory Buckets?
    bucket_name = bucket['Name']

    try:
        encryption = s3_client.get_bucket_encryption(
            Bucket=bucket_name
        )

        encryption_setting = encryption['ServerSideEncryptionConfiguration']['Rules'][0]['ApplyServerSideEncryptionByDefault']
        encryption_algorithm = encryption_setting['SSEAlgorithm']

        if encryption_algorithm != 'AES256' and 'KMSMasterKeyID' in encryption_setting.keys():
            encryption_key = encryption_setting['KMSMasterKeyID']
        else:
            #Bucket uses S3 Managed (AWS Owned)
            add_to_bucket_summary("BucketEncryption", bucket_name)
            encryption_key = 'None'
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("BucketEncryption", bucket_name)
        else:
            raise error
        
    
    # BPA Settings 
    try:
        bpa_settings = s3_client.get_public_access_block(
            Bucket=bucket_name
        )
        bucket_bpa_config = bpa_settings['PublicAccessBlockConfiguration']
        
        if not bucket_bpa_config['BlockPublicAcls'] or not bucket_bpa_config['IgnorePublicAcls'] or not bucket_bpa_config['BlockPublicPolicy'] or not bucket_bpa_config['RestrictPublicBuckets']:
            add_to_bucket_summary("BucketBPA", bucket_name)

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("BucketBPA", bucket_name)
            bucket_bpa_config = "access_error"
        elif error.response['Error']['Code'] == 'NoSuchPublicAccessBlockConfiguration':
            bucket_bpa_config = {'BlockPublicAcls': False,
                'IgnorePublicAcls': False,
                'BlockPublicPolicy': False,
                'RestrictPublicBuckets': False
            }
            
            add_to_bucket_summary("BucketBPA", bucket_name)
        else:
            raise error

    # ACL Settings
    try:
        bucket_object_ownership_response = s3_client.get_bucket_ownership_controls(
            Bucket=bucket_name
        )
        bucket_object_ownership = bucket_object_ownership_response['OwnershipControls']['Rules'][0]['ObjectOwnership']
    
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("BucketACLEnabled", bucket_name)
            bucket_object_ownership = 'access_error'
        elif error.response['Error']['Code'] == 'OwnershipControlsNotFoundError':
            bucket_object_ownership = 'ObjectWriter'
        else:
            raise error
                
    if bucket_object_ownership == 'BucketOwnerEnforced':
        bucket_acls_enabled = 'disabled'

    elif bucket_object_ownership == 'ObjectWriter' or bucket_object_ownership == 'BucketOwnerPreferred':
        bucket_acls_enabled = 'enabled'
        add_to_bucket_summary("BucketACLEnabled", bucket_name)
        

    #Get Bucket Public Status
    #GetBucketAcl - This returns effective ACLs
    try:
        bucket_acl_response = s3_client.get_bucket_acl(
            Bucket=bucket_name
        )
        acl_status = 'private'

        acl_grants = bucket_acl_response['Grants']
    
        public_groups = [
            "http://acs.amazonaws.com/groups/global/AllUsers",
            "http://acs.amazonaws.com/groups/global/AuthenticatedUsers"
        ]
        
        for grant in acl_grants:
            if grant['Grantee'].get('URI') in public_groups:
                acl_status = 'public'
                add_to_bucket_summary("BucketACL", bucket_name)
                break 

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("BucketACL", bucket_name)
        else:
            raise error
    

    #Bucket Policy
    try:
        policy_status_response = s3_client.get_bucket_policy_status(
            Bucket=bucket_name
        )
        if policy_status_response['PolicyStatus']['IsPublic'] == True:
            policy_status = "public"
            add_to_bucket_summary("BucketPolicyStatus", bucket_name)
        else:
            policy_status = "private"

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("BucketPolicyStatus", bucket_name)
            policy_status = "access_error"
        elif error.response['Error']['Code'] == 'NoSuchBucketPolicy':
            policy_status = "private"
        else:
            raise error

    try:
        website_response = s3_client.get_bucket_website(
            Bucket=bucket_name
        )

        #If configuration found
        website = 'enabled'
        add_to_bucket_summary("Website", bucket_name)

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("Website", bucket_name)
            website = "access_error"
        elif error.response['Error']['Code'] == 'NoSuchWebsiteConfiguration':
            website = 'disabled'
        else:
            raise error

    #Check for Ransomware Protection
    # Object Lock Configuration
    # Bucket Versioning Settings
    # Bucket Lifecycle Configuration

    try:
        object_lock_response = s3_client.get_object_lock_configuration(
            Bucket=bucket_name
        )

        object_lock = object_lock_response['ObjectLockConfiguration']['ObjectLockEnabled']
        add_to_bucket_summary("ObjectLock", bucket_name)
        #Object lock is enabled or not present
    except botocore.exceptions.ClientError as error:

        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("ObjectLock", bucket_name)
            object_lock = "access_error"
        elif error.response['Error']['Code'] == 'ObjectLockConfigurationNotFoundError':
            object_lock = "disabled"
            add_to_bucket_summary("ObjectLock", bucket_name)
        else:
            raise error

    try:
        versioning_response = s3_client.get_bucket_versioning(
            Bucket=bucket_name
        )
        #Versioning can be Enabled or Suspended

        versioning = versioning_response.get('Status')
        if versioning == "Suspended":
            add_to_bucket_summary("Versioning", bucket_name)

        if versioning == None:
            versioning = 'disabled'
            add_to_bucket_summary("Versioning", bucket_name)

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("Versioning", bucket_name)
        else:
            raise error

    try:
        lifecycle_response = s3_client.get_bucket_lifecycle_configuration(
            Bucket=bucket_name
        )

        lifecycle_rules = lifecycle_response['Rules']

        #Check for Expiration + Days, NoncurrentVersionExpiration.
        #Does not check for Transition, Abort, or ExpiredObjectDeleteMarker (that would require all versions to be deleted)
        for rule in lifecycle_rules:
            lifecycle = "no_expiration"

            if rule.get("Expiration") or rule.get("NoncurrentVersionExpiration"):
                lifecycle = "expiration"
                add_to_bucket_summary("LifecycleConfig", bucket_name)
                break

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("LifecycleConfig", bucket_name)
        elif error.response['Error']['Code'] == 'NoSuchLifecycleConfiguration':
            lifecycle = 'disabled'
        else:
            raise error

    try:
        bucket_logging = s3_client.get_bucket_logging(
            Bucket=bucket_name
        )
        if bucket_logging.get('LoggingEnabled'):
            access_logging = 'enabled'
        else:
            access_logging = 'disabled'
            add_to_bucket_summary("AccessLogging", bucket_name)

    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] == 'AccessDenied':
            access_issue("AccessLogging", bucket_name)
    
    bucket_results.append({
        'Bucket': bucket_name,
        'BucketEncryption': encryption_setting,
        'EncryptionKey': encryption_key,
        'BucketBPA': bucket_bpa_config,
        'BucketACLEnabled': bucket_acls_enabled,
        'BucketACL': acl_status,
        'BucketPolicyStatus': policy_status,
        'ObjectLock': object_lock,
        "Versioning": versioning,
        "LifecycleConfig": lifecycle,
        "Website": website,
        "AccessLogging": access_logging
    })

summarize_results(bucket_results, account_results, bucket_results_summary)


#Output Bucket Results

