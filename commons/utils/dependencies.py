from typing import Union
from functools import lru_cache

from ..impl import GithubService, SSMSecretsManager, MongoDBService
from ..interfaces import RepositoryServiceInterface, SecretsManagerInterface, DatabaseServiceInterface
from .token_manager import TokenManager


@lru_cache(maxsize=1)
def get_secrets_manager(aws_region_name: str) -> SecretsManagerInterface:
    return SSMSecretsManager(aws_region_name)


@lru_cache(maxsize=1)
def get_token_manager(secrets_manager: SecretsManagerInterface) -> TokenManager:
    return TokenManager(secrets_manager)


@lru_cache(maxsize=1)
def get_repository_service(
    aws_region_name: str, repo_private_key_path: str, ca_certs: Union[str, None] = None
) -> RepositoryServiceInterface:
    return GithubService(
        secrets_manager=get_secrets_manager(aws_region_name),
        token_manager=get_token_manager(get_secrets_manager(aws_region_name)),
        repo_private_key_path=repo_private_key_path,
        ca_certs=ca_certs,
    )

@lru_cache(maxsize=1)
def get_database_service(
    conn_string: str,
    database_name: str,
    username: str,
    password: str,
) -> DatabaseServiceInterface:
    return MongoDBService(
        conn_string=conn_string,
        db_name=database_name,
        username=username,
        password=password,
    )
