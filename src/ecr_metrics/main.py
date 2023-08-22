"""
Use Boto3 to describe ECR repositories, and print the results.
"""
import logging

import boto3


cloudwatch_client = boto3.client("cloudwatch")
ecr_client = boto3.client("ecr")


def collect_all_repositories() -> list[dict]:
    """Paginates through all ECR repositories and returns a list of them."""
    repositories = []
    paginator = ecr_client.get_paginator("describe_repositories")
    response_iterator = paginator.paginate(PaginationConfig={"PageSize": 1000})

    for page in response_iterator:
        repositories.extend(page["repositories"])

    return repositories


def report_all_repositories(repository_count: int) -> None:
    """Emits a CloudWatch metric total."""
    cloudwatch_client.put_metric_data(
        Namespace="ECR",
        MetricData=[
            {
                "MetricName": "RepositoryCount",
                "Dimensions": [
                    {
                        "Name": "RegionName",
                        "Value": ecr_client.meta.region_name,
                    },
                ],
                "Value": repository_count,
                "Unit": "Count",
            },
        ],
    )


def report_per_repository(
    repository_name: str,
    image_count: int,
    total_bytes: int,
) -> None:
    """Emits CloudWatch metrics per repository."""
    common_dimensions = [
        {
            "Name": "RepositoryName",
            "Value": repository_name,
        },
    ]

    cloudwatch_client.put_metric_data(
        Namespace="ECR",
        MetricData=[
            {
                "MetricName": "ImageCount",
                "Dimensions": common_dimensions,
                "Value": image_count,
                "Unit": "Count",
            },
            {
                "MetricName": "TotalBytes",
                "Dimensions": common_dimensions,
                "Value": total_bytes,
                "Unit": "Bytes",
            },
        ],
    )


def main():
    """
    Use Boto3 to describe ECR repositories, and print the results.
    """
    repositories = collect_all_repositories()

    repository_count = len(repositories)
    logging.debug(f"Total repositories: {repository_count}")
    report_all_repositories(repository_count)

    for repository in repositories:
        repository_name = repository["repositoryName"]
        logging.debug(f"Repository: {repository_name}")

        paginator = ecr_client.get_paginator("describe_images")
        response_iterator = paginator.paginate(repositoryName=repository_name)

        image_count = 0
        total_bytes = 0
        for page in response_iterator:
            image_count += len(page["imageDetails"])

            for image in page["imageDetails"]:
                total_bytes += image["imageSizeInBytes"]

        logging.debug(f"Image count: {image_count}")
        logging.debug(f"Total bytes: {total_bytes}")

        report_per_repository(repository_name, image_count, total_bytes)

    logging.info("Done.")


def handler(_context, _event):
    """Lambda handler entrypoint."""
    main()


def cli():
    """CLI entrypoint."""
    logging.basicConfig(level=logging.DEBUG)
    main()
