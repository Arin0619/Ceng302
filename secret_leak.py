"""Module that demonstrates connecting with AWS credentials.

This file previously contained a hard-coded AWS secret. Storing secrets in
source code is a high-risk practice — use environment variables or a
secrets manager instead.
"""

from os import environ
from typing import Optional


AWS_SECRET_KEY: Optional[str] = environ.get("AWS_SECRET_KEY")


def connect() -> None:
    """Attempt to connect using AWS credentials taken from env vars.

    This function intentionally does not print the secret value.
    """
    key = AWS_SECRET_KEY
    if not key:
        print("No AWS_SECRET_KEY configured; aborting connection.")
        return
    # Do not print secrets to logs or stdout. Indicate connection attempt only.
    print("Connecting with AWS credentials (hidden).")
