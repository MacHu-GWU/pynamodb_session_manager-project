# -*- coding: utf-8 -*-

import pytest

import botocore.exceptions
from pynamodb_session_manager.impl import use_boto_session, reset_connection

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute
from pynamodb.constants import PAY_PER_REQUEST_BILLING_MODE

from boto_session_manager import BotoSesManager


def test_this_boto_session_manager():
    print("")
    print("=== Demo Started ===")
    # Configuration constants
    aws_region = "us-east-1"

    # Initialize session managers for different AWS accounts/profiles
    # THE default AWS PROFILE on your machine (usually from ~/.aws/credentials [default])
    # By default, PynamoDB will use this profile
    default_bsm = BotoSesManager(region_name=aws_region)
    print(f"default aws account: {default_bsm.aws_account_id = }")

    # THE TARGET AWS PROFILE YOU WANT TO USE (specific profile from ~/.aws/credentials)
    project_bsm = BotoSesManager(
        profile_name="bmt_app_dev_us_east_1",
        region_name=aws_region,
    )
    print(f"project aws account: {project_bsm.aws_account_id = }")

    dynamodb_table_name = "pynamodb_session_manager_test"

    class User(Model):
        """
        Example PynamoDB model for demonstration purposes.

        This model represents a simple user table with an ID as the primary key.
        It's configured to use pay-per-request billing mode for cost optimization
        during testing.
        """

        class Meta:
            table_name = dynamodb_table_name
            region = aws_region
            billing_mode = PAY_PER_REQUEST_BILLING_MODE

        id: str = UnicodeAttribute(hash_key=True)

    # Example 1: Create table in the target account
    print("=== Creating table in target account ===")
    with use_boto_session(project_bsm, User):
        # This will create the table in the project AWS account
        # because we're using project_bsm credentials within the context
        User.create_table(wait=True)

    try:
        project_bsm.dynamodb_client.describe_table(TableName=dynamodb_table_name)
    except botocore.exceptions.ClientError as e:
        assert e.response["Error"]["Code"] == "ResourceNotFoundException"

    # Example 2: Attempt operation with default credentials (should fail)
    print("\n=== Attempting operation with default credentials ===")
    # This will use the default AWS account credentials
    # Since the table doesn't exist in the default account, it will raise an exception
    with pytest.raises(Exception) as e:
        user = User(id=default_bsm.aws_account_id)
        user.save()
        print("Unexpected success - table exists in default account")
    print(f"Expected error (table not in default account): {e}")

    # Example 3: Insert item in target account
    print("\n=== Inserting item in target account ===")
    with use_boto_session(
        project_bsm,
        User,
        restore_on_exit=False,  # Keep the connection to the target account
    ):
        # This will insert item to the table in the project AWS account
        # because we're using project_bsm credentials within the context
        user = User(id=project_bsm.aws_account_id)
        user.save()
        print(
            f"User with ID={project_bsm.aws_account_id} saved to account: {project_bsm.aws_account_id}"
        )

    res = project_bsm.dynamodb_client.get_item(
        TableName=dynamodb_table_name,
        Key={"id": {"S": project_bsm.aws_account_id}},
    )
    item = res["Item"]
    assert item["id"]["S"] == project_bsm.aws_account_id

    # Example 4: Retrieve item from target account
    print("\n=== Retrieving item from target account ===")
    # since we set restore_connection=False, we can continue
    # using the same connection without re-entering the context manager
    # This will retrieve the item from the table in the project AWS account
    user = User.get(project_bsm.aws_account_id)
    assert user.id == project_bsm.aws_account_id
    print(
        f"Retrieved user from account {project_bsm.aws_account_id}: {user.attribute_values}"
    )

    # Example 5: Reset connection to default account
    print("\n=== Resetting connection to default account ===")
    reset_connection(User)
    # This will use the default AWS account credentials
    # Since the table doesn't exist in the default account, it will raise an exception
    with pytest.raises(Exception) as e:
        user = User(id=default_bsm.aws_account_id)
        user.save()

    print("\n=== Demo completed ===")


if __name__ == "__main__":
    from pynamodb_session_manager.tests import run_cov_test

    run_cov_test(
        __file__,
        "pynamodb_session_manager.impl",
        preview=False,
    )
