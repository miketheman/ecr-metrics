# ecr-metrics

In a perfect world, this wouldn't exist.

[Amazon Elastic Container Registry (ECR)](https://aws.amazon.com/ecr/) is a great service,
but it lacks a few key features that would make it easier for end users.
Specifically, some metrics around usage and limits are important for end users,
so that you don't learn about the limits the hard way.

This project is a simple Python script that will query the AWS API
and report on the following metrics:

* Total number of repositories
* Total number of images in each repository (default limit is 10k)
* Total size of all images in each repository

Ideally the ECR team should implement these (and any others)
and then I can retire this project.

Go ahead and add your 👍 reaction to [this issue](https://github.com/aws/containers-roadmap/issues/578)
to signal your desire for this feature.

Until then, you can run this script manually,
or even better - run it as a Lambda function on a schedule.

While [ECR does support Service Quotas integration](https://aws.amazon.com/about-aws/whats-new/2020/03/now-proactively-manage-your-ecr-api-use-with-cloudwatch-metrics-and-service-quotas/),
it's not granular enough to help operators figure out which repositories are using the most space,
and when they might need to request a limit increase or handle the situation themselves.

## Usage

### Manual

Note: This assumes you have [Poetry](https://python-poetry.org/)
and Python 3.10 installed.

```shell
git clone https://github.com/miketheman/ecr-metrics.git
poetry install
ecr-metrics
```

### Automated

A better solution is to run this as a Lambda function on a schedule.

#### Lambda

1. Create a new Lambda function
2. Upload the `ecr-metrics.py` file as the function code
3. Set the handler to `ecr-metrics.lambda_handler`
4. Set the runtime to `Python 3.10`
5. Set the timeout to `5 minutes` or an interval you find acceptable
6. Set the memory to `128 MB`

Note: The code assumes it runs in the region where you have repositories.
Amazon ECR is a regional service, and the quotas are regional as well.
Deploy the Lambda Function to each region in which you have repositories.

#### CloudWatch Events

1. Create a new CloudWatch Events rule
2. Set the schedule to `rate(30 minutes)`
3. Add a target of the Lambda function you created above

## License

This project is licensed under the MIT License.
See the [LICENSE](LICENSE) file for details.

## Contributing

See [TODO](TODO.md) for a list of things that need to be done.

Pull requests are welcome.
For major changes, please open an issue first to discuss what you would like to change.

## Disclaimer

This project is not affiliated with Amazon Web Services (AWS) or Amazon.

## Author

[Mike Fiedler](https://github.com/miketheman)
