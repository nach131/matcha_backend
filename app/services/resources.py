"""Validation and orchestration for resource endpoints."""

from collections.abc import Mapping

from app.repositories.resources import find_resource, insert_resource
from app.resources import RESOURCE_SPECS, ResourceSpec


def _get_spec(resource_name: str) -> ResourceSpec:
    try:
        return RESOURCE_SPECS[resource_name]
    except KeyError as exc:
        raise ValueError(f"Unsupported resource: {resource_name}.") from exc


def get_resource(
    resource_name: str,
    key_values: tuple[int, ...],
) -> dict[str, object] | None:
    spec = _get_spec(resource_name)
    if len(key_values) != len(spec.primary_key):
        raise ValueError(f"Invalid key for resource: {resource_name}.")
    if any(type(value) is not int or value <= 0 for value in key_values):
        raise ValueError("Resource identifiers must be positive integers.")

    return find_resource(spec, dict(zip(spec.primary_key, key_values)))


def create_resource(
    resource_name: str,
    data: Mapping[str, object],
) -> dict[str, object]:
    spec = _get_spec(resource_name)
    required_fields = set(spec.fields)
    provided_fields = set(data)
    missing_fields = required_fields - provided_fields
    unexpected_fields = provided_fields - required_fields
    errors: list[str] = []

    if missing_fields:
        errors.append(f"Missing fields: {', '.join(sorted(missing_fields))}.")
    if unexpected_fields:
        errors.append(
            f"Unexpected fields: {', '.join(sorted(unexpected_fields))}."
        )

    values: dict[str, object] = {}
    for field, expected_type in spec.fields.items():
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

    return insert_resource(spec, values)
