from failures import FailureType

RETRY_POLICY = {
    FailureType.TIMEOUT: {
        "max_retries": 2,
        "backoff": True,
    },
    FailureType.CONNECTION: {
        "max_retries": 3,
        "backoff": True,
    },
    FailureType.SCHEMA_JSON: {
        "max_retries": 2,
        "backoff": False,
    },
    FailureType.SCHEMA_VALIDATION: {
        "max_retries": 2,
        "backoff": False,
    },
    FailureType.UNKNOWN: {
        "max_retries": 0,
        "backoff": False,
    },
}