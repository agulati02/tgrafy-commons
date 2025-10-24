from abc import ABC, abstractmethod
from typing import Any


class DatabaseServiceInterface(ABC):
    @abstractmethod
    def connect(self, connection_string: str) -> None:
        """Establish a connection to the database."""
        pass

    @abstractmethod
    def query(self, query: str) -> list[dict[str, Any]]:
        """Execute a query against the database and return the results."""
        pass

    @abstractmethod
    def save(self, data: dict[str, Any]) -> None:
        """Save data to the database."""
        pass

    @abstractmethod
    def update(self, identifier: str, data: dict[str, Any]) -> None:
        """Update existing data in the database."""
        pass
