"""Common request-payload validation helpers."""

from collections.abc import Mapping


def validate_payload(
    data: Mapping[str, object],
    field_types: Mapping[str, type],
) -> dict[str, object]:
    required_fields = set(field_types)
    missing_fields = required_fields - set(data)
    unexpected_fields = set(data) - required_fields
    errors: list[str] = []

    if missing_fields:
        errors.append(f"Missing fields: {', '.join(sorted(missing_fields))}.")
    if unexpected_fields:
        errors.append(
            f"Unexpected fields: {', '.join(sorted(unexpected_fields))}."
        )

    values: dict[str, object] = {}
    for field, expected_type in field_types.items():
        value = data.get(field)

        if expected_type is int:
            if type(value) is not int or value <= 0:
                errors.append(f"'{field}' must be a positive integer.")
            else:
                values[field] = value
        elif expected_type is bool:
            if type(value) is not bool:
                errors.append(f"'{field}' must be a boolean.")
            else:
                values[field] = value
        elif expected_type is str:
            if not isinstance(value, str) or not value.strip():
                errors.append(f"'{field}' must be a non-empty string.")
            else:
                values[field] = value.strip()

    if errors:
        raise ValueError(" ".join(errors))

    return values


def validated_int(values: Mapping[str, object], field: str) -> int:
    value = values[field]
    if type(value) is not int:
        raise RuntimeError(f"Validated field '{field}' is not an integer.")
    return value


def validated_bool(values: Mapping[str, object], field: str) -> bool:
    value = values[field]
    if type(value) is not bool:
        raise RuntimeError(f"Validated field '{field}' is not a boolean.")
    return value


def validated_str(values: Mapping[str, object], field: str) -> str:
    value = values[field]
    if not isinstance(value, str):
        raise RuntimeError(f"Validated field '{field}' is not a string.")
    return value
