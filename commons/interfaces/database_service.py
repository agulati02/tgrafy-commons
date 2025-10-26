from abc import ABC, abstractmethod
from typing import Any, Optional


class DatabaseServiceInterface(ABC):

    @abstractmethod
    def __enter__(self) -> 'DatabaseServiceInterface':
        pass

    @abstractmethod
    def __exit__(self, exc_type, exc_value, traceback) -> None: # type: ignore
        pass

    @abstractmethod
    def query(self, collection: str, filter: dict[str, Any], select: Optional[dict[str, Any]] = None) -> list[dict[str, Any]]:
        """Execute a query against the database and return the results."""
        pass

    @abstractmethod
    def save(self, collection: str, data: dict[str, Any]) -> None:
        """Save data to the database."""
        pass

    @abstractmethod
    def update(self, collection: str, filter: dict[str, Any], diff: dict[str, Any]) -> None:
        """Update existing data in the database."""
        pass
