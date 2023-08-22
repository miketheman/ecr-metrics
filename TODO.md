# TODO

Anything that hasn't been fully implemented yet.

- create deployment via Serverless, CDK, SAM, etc.

The only dependency is `boto3` which is available in Lambda runtime,
so we don't need to sort out packaging.

There's no simple way to deploy this to multiple regions.
It's a manual process, and that's not great.

And setting up the CloudWatch Event Schedule is also manual.

We should also supply an IAM role that allows
`ECR.DescribeRepositories/DescribeImages` and
`CloudWatch.PutMetricData` to be used from the deployed Lambda function

- split put_metric_data() into batches

Defaults allow for some headroom, but if you have a lot of repositories,
you may need to split the batches.

- add service quota metrics

These could prove useful if you're worried about limits.

- add safety in get/put

Nothing does any retries outside of whatever the boto3 client does.
This is probably fine, but it's worth considering.

- add tests

Completely skipped, since this ought to be a feature of ECR, not something
you need to implement yourself.
