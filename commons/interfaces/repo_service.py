from abc import ABC, abstractmethod


class RepositoryServiceInterface(ABC):
    @abstractmethod
    def get_diff(
        self,
        pull_request_url: str,
        installation_id: int,
        app_client_id: str,
    ) -> str:
        """Retrieve the diff for the given pull request URL."""
        pass

    @abstractmethod
    def post_issue_comment(
        self, comments_url: str, installation_id: int, content: str, app_client_id: str
    ) -> None:
        """Post review comments to the given pull request URL."""
        pass
