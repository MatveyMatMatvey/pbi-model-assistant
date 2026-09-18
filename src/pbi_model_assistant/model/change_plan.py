SUPPORTED_ACTIONS = {
    "create_measure",
}


def validate_change_plan(plan: dict) -> None:
    """
    Проверяет ChangePlan до изменения Power BI.
    """

    if not isinstance(plan, dict):
        raise ValueError(
            "ChangePlan должен быть JSON-объектом."
        )

    actions = plan.get("actions")

    if not isinstance(actions, list):
        raise ValueError(
            "ChangePlan должен содержать список 'actions'."
        )

    if not actions:
        raise ValueError(
            "ChangePlan не содержит действий."
        )

    for index, action in enumerate(actions, start=1):
        if not isinstance(action, dict):
            raise ValueError(
                f"Action #{index} должен быть объектом."
            )

        action_type = action.get("type")

        if action_type not in SUPPORTED_ACTIONS:
            raise ValueError(
                f"Action #{index}: "
                f"неподдерживаемый type '{action_type}'."
            )

        if action_type == "create_measure":
            _validate_create_measure(
                action,
                index,
            )


def _validate_create_measure(
    action: dict,
    index: int,
) -> None:
    required_fields = (
        "table",
        "name",
        "expression",
    )

    for field in required_fields:
        value = action.get(field)

        if not isinstance(value, str):
            raise ValueError(
                f"Action #{index}: "
                f"'{field}' должно быть строкой."
            )

        if not value.strip():
            raise ValueError(
                f"Action #{index}: "
                f"'{field}' не может быть пустым."
            )