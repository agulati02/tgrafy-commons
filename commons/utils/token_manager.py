from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
import requests

from ..interfaces import SecretsManagerInterface


class TokenManager:
    def __init__(self, secrets_manager: SecretsManagerInterface) -> None:
        self.secrets_manager = secrets_manager

    def get_jwt_token(
        self, private_key: str, iss: str, algo: str = "RS256", exp: int = 10
    ) -> str:
        payload: dict[str, Any] = {
            "iat": int(datetime.now(timezone.utc).timestamp()),
            "exp": int(
                (datetime.now(timezone.utc) + timedelta(minutes=exp)).timestamp()
            ),
            "iss": iss,
            "alg": algo,
        }

        jwt_token = jwt.encode(payload, private_key, algorithm=algo)
        return jwt_token

    def get_installation_access_token(
        self, jwt_token: str, installation_id: int
    ) -> str:
        url = (
            f"https://api.github.com/app/installations/{installation_id}/access_tokens"
        )
        headers = {
            "Authorization": f"Bearer {jwt_token}",
            "Accept": "application/vnd.github+json",
        }

        response = requests.post(url, headers=headers)
        response.raise_for_status()
        return response.json().get("token", None)
