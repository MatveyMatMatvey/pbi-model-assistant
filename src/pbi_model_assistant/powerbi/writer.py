from pbi_model_assistant.model.change_plan import (
    validate_change_plan,
)

from pbi_model_assistant.powerbi.tom import (
    create_measure,
)


def apply_change_plan(
    server_address: str,
    database_name: str,
    plan: dict,
) -> None:
    """
    Проверяет и применяет ChangePlan к Power BI.
    """

    validate_change_plan(plan)

    for action in plan["actions"]:
        action_type = action["type"]

        if action_type == "create_measure":
            create_measure(
                server_address=server_address,
                database_name=database_name,
                table_name=action["table"],
                measure_name=action["name"],
                expression=action["expression"],
                format_string=action.get(
                    "format_string",
                    "",
                ),
            )