from typing import Union

import boto3
from mypy_boto3_ssm.client import SSMClient

from ..interfaces.secrets_manager import SecretsManagerInterface


class SSMSecretsManager(SecretsManagerInterface):
    def __init__(self, aws_region_name: str) -> None:
        self.ssm_client: SSMClient = boto3.client("ssm", region_name=aws_region_name)  # type: ignore

    def get_secret(self, secret_name: str) -> Union[str, None]:
        response = self.ssm_client.get_parameter(Name=secret_name, WithDecryption=True)
        return response.get("Parameter", {}).get("Value", None)
