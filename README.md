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

## Architecture

This project deploys the following infrastructure:

* Amazon EventBridge Scheduler - Invokes the Lambda function on a schedule of your choice
* AWS Lambda - Runs the Python code to gather metrics
* Amazon CloudWatch - Stores and displays the metrics for monitoring

On a schedule, the Lambda function:
1. Uses the AWS SDK to fetch metadata about your ECR repositories
2. Calculates metrics about repository count, image count per repository, and total size per repository
3. Puts the metadata into CloudWatch as metrics for monitoring and alerting

## Usage

### Manual

Note: This assumes you have [Poetry](https://python-poetry.org/)
and Python 3.13 installed.

```shell
git clone https://github.com/miketheman/ecr-metrics.git
poetry install
ecr-metrics
```

### AWS SAM Deployment (Recommended)

The recommended way to deploy this solution is using AWS SAM (Serverless Application Model). This allows for easy deployment of the Lambda function, EventBridge schedule, and required IAM permissions.

#### Prerequisites

- [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- AWS CLI credentials configured

#### Deployment Steps

1. Clone the repository:
```shell
git clone https://github.com/miketheman/ecr-metrics.git
cd ecr-metrics
```

2. Build the application:
```shell
sam build
```

3. Deploy the application:
```shell
sam deploy \
  --capabilities CAPABILITY_IAM \
  --resolve-s3 \
  --resolve-image-repos \
  --stack-name ecr-metrics
```

4. Wait a few minutes and check CloudWatch Metrics. You will see a new custom namespace called "ECR" with metrics for each of your ECR repositories.

#### Testing Locally

You can test the Lambda function locally using SAM:

```shell
sam local invoke
```

#### Removing the Deployment

If you no longer need to track ECR metrics, you can remove the deployment:

```shell
sam delete --stack-name ecr-metrics
```

### Manual Lambda Deployment (Alternative)

If you prefer to set up the Lambda function manually instead of using SAM:

1. Create a new Lambda function with a container image
2. Set the runtime to `Python 3.13` (via container image)
3. Set the handler to `src/ecr_metrics/main.handler`
4. Set the timeout to `5 minutes` or an interval you find acceptable
5. Set the memory to `128 MB`
6. Ensure the Lambda has IAM permissions for:
   - `ecr:DescribeRepositories`
   - `ecr:DescribeImages`
   - `cloudwatch:PutMetricData`
7. (Optional) For cost savings, select ARM architecture (Graviton2) when creating the function

Note: The code assumes it runs in the region where you have repositories.
Amazon ECR is a regional service, and the quotas are regional as well.
Deploy the Lambda Function to each region in which you have repositories.

#### CloudWatch Events/EventBridge Schedule

1. Create a new EventBridge Scheduler rule
2. Set the schedule to `rate(30 minutes)` (or another interval based on your needs)
3. Add a target of the Lambda function you created above

## Project Structure

```
ecr-metrics
├── Dockerfile
├── LICENSE
├── README.md
├── TODO.md
├── poetry.lock
├── pyproject.toml
├── src
│   └── ecr_metrics
│       └── main.py
├── template.yml
└── tests
    ├── responses.md
    └── test_main.py
```

- `src` contains the Lambda function code
- `Dockerfile` defines how to build the container image for Lambda
- `template.yml` is the SAM template for deployment
- `tests` contains unit tests

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
