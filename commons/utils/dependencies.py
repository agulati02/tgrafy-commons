from typing import Union

from ..impl import GithubService, SSMSecretsManager
from ..interfaces import RepositoryServiceInterface, SecretsManagerInterface
from .token_manager import TokenManager


def get_secrets_manager(aws_region_name: str) -> SecretsManagerInterface:
    return SSMSecretsManager(aws_region_name)


def get_token_manager(secrets_manager: SecretsManagerInterface) -> TokenManager:
    return TokenManager(secrets_manager)


def get_repository_service(
    aws_region_name: str, repo_private_key_path: str, ca_certs: Union[str, None] = None
) -> RepositoryServiceInterface:
    return GithubService(
        secrets_manager=get_secrets_manager(aws_region_name),
        token_manager=get_token_manager(get_secrets_manager(aws_region_name)),
        repo_private_key_path=repo_private_key_path,
        ca_certs=ca_certs,
    )
