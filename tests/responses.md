# response

Use these when creating Stubber responses.

## ecr.describe_repositories

```python
{'ResponseMetadata': {'HTTPHeaders': {'connection': 'keep-alive',
                                      'content-length': '379',
                                      'content-type': 'application/x-amz-json-1.1',
                                      'date': 'Tue, 22 Aug 2023 15:52:02 GMT',
                                      'x-amzn-requestid': '2ecd52d0-2eb9-4905-83d8-318dce278399'},
                      'HTTPStatusCode': 200,
                      'RequestId': '2ecd52d0-2eb9-4905-83d8-318dce278399',
                      'RetryAttempts': 0},
 'repositories': [{'createdAt': datetime.datetime(2023, 8, 22, 11, 33, 12, tzinfo=tzlocal()),
                   'encryptionConfiguration': {'encryptionType': 'AES256'},
                   'imageScanningConfiguration': {'scanOnPush': False},
                   'imageTagMutability': 'MUTABLE',
                   'registryId': '366328713202',
                   'repositoryArn': 'arn:aws:ecr:us-east-1:366328713202:repository/sample1',
                   'repositoryName': 'sample1',
                   'repositoryUri': '366328713202.dkr.ecr.us-east-1.amazonaws.com/sample1'}]}
```
