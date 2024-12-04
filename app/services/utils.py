def validate_input(data, required_fields):
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
