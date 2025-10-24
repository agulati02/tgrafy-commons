from abc import ABC, abstractmethod
from typing import Union


class SecretsManagerInterface(ABC):
    @abstractmethod
    def get_secret(self, secret_name: str) -> Union[str, None]:
        """Retrieve the secret value for the given secret name."""
        pass
