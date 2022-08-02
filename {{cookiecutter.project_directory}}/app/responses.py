"""
#######################################
Singel response example
#######################################
{
    "model": ""
    "description": "",
    "content": {
        "application/json": {
            "example": {"id": "bar", "value": "The bar tenders"}
        }
    },
}
########################################
Multi responses example
########################################
"normal": {
    "summary": "A normal example",
    "description": "A **normal** item works correctly.",
    "value": {
        "name": "Foo",
        "description": "A very nice Item",
        "price": 35.4,
        "tax": 3.2,
    },
}
"""
from typing import Dict, Any, Type
from pydantic import BaseModel

###
from app.schemas import GenericSchema


def _single_response_schema(
    *,
    model: Any,
    description: str,
    content_example: Dict,
    content_type: str = "application/json"
) -> Dict:
    return {
        "model": model,
        "description": description,
        "content": {content_type: content_example},
    }


def _multi_responses_schema(*, summary: str, description: str, value: Dict) -> Dict:
    return {"summary": summary, "description": description, "value": value}


def INCORRECT_USERNAME_OR_PASSWORD_EXAMPLE(
    model: Type[BaseModel] = GenericSchema.DetailResponse,
    description: str = "Incorrect username or password",
    content_type: str = "application/json",
    content_example: Dict = {},
) -> Dict:
    example = model.schema().get("example", {}) or content_example
    return _single_response_schema(
        model=model,
        description=description,
        content_type=content_type,
        content_example=example,
    )
