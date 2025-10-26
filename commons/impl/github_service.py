from typing import Union

from httpx import Client

from ..interfaces import RepositoryServiceInterface, SecretsManagerInterface
from ..utils.token_manager import TokenManager


class GithubService(RepositoryServiceInterface):
    def __init__(
        self,
        secrets_manager: SecretsManagerInterface,
        token_manager: TokenManager,
        repo_private_key_path: str,
        connection_timeout: float = 10.0,
        ca_certs: Union[str, None] = None,
    ) -> None:
        self.secrets_manager = secrets_manager
        self.client = Client(
            timeout=connection_timeout,
            verify=ca_certs if ca_certs else True,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                "Connection": "keep-alive",
            },
        )
        self.token_manager = token_manager
        self.private_key = self.secrets_manager.get_secret(repo_private_key_path)

    def get_diff(
        self,
        pull_request_url: str,
        installation_id: int,
        app_client_id: str,
    ) -> str:
        """Fetches the diff for a given pull request payload from GitHub."""
        if not self.private_key:
            raise ValueError("Private key could not be retrieved from secrets manager.")

        jwt_token = self.token_manager.get_jwt_token(
            private_key=self.private_key,
            iss=app_client_id,
        )
        access_token = self.token_manager.get_installation_access_token(
            jwt_token, installation_id
        )
        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github.v3.diff",
        }
        response = self.client.get(pull_request_url, headers=headers)
        response.raise_for_status()
        return response.text

    def post_issue_comment(
        self,
        comments_url: str,
        installation_id: int,
        content: str,
        app_client_id: str,
    ) -> None:
        """Posts review comments to a given pull request on GitHub."""
        if not self.private_key:
            raise ValueError("Private key could not be retrieved from secrets manager.")

        jwt_token = self.token_manager.get_jwt_token(
            private_key=self.private_key,
            iss=app_client_id,
        )
        access_token = self.token_manager.get_installation_access_token(
            jwt_token, installation_id
        )

        headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/vnd.github+json",
        }

        payload = {"body": content, "event": "COMMENT"}
        response = self.client.post(comments_url, headers=headers, json=payload)
        response.raise_for_status()
