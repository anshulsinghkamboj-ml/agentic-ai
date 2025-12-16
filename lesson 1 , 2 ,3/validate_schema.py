def validate_schema(data: dict, schema: dict):
    if not isinstance(data, dict):
        raise TypeError("Top-level JSON must be an object")

    for key, expected_type in schema.items():
        if key not in data:
            raise KeyError(f"Missing required key: {key}")

        if not isinstance(data[key], expected_type):
            raise TypeError(
                f"Key '{key}' must be {expected_type.__name__}, "
                f"got {type(data[key]).__name__}"
            )
