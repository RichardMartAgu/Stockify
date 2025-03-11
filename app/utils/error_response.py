from typing import Dict

from starlette import status


def get_error_response(error: str, detail: str):
    return {
        "description": error,
        "content": {
            "application/json": {
                "example": {
                    "detail": detail
                }
            }
        }
    }

