from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, END
from backend.agents.classifier import classifier_agent
from backend.agents.tariff import tariff_agent
from backend.agents.compliance import compliance_agent
from backend.agents.sanctions import sanctions_agent
from backend.agents.document import document_agent


class DutyBreakState(TypedDict):
    product_description: str
    origin_country: str
    destination_country: str
    supplier_name: str | None
    hs_code: str
    tariff_data: dict
    compliance_data: dict
    sanctions_data: dict
    compliance_brief: dict
    errors: list[str]


def build_graph() -> StateGraph:
    graph = StateGraph(DutyBreakState)

    graph.add_node("classifier", classifier_agent)
    graph.add_node("tariff", tariff_agent)
    graph.add_node("compliance", compliance_agent)
    graph.add_node("sanctions", sanctions_agent)
    graph.add_node("document", document_agent)

    graph.set_entry_point("classifier")
    graph.add_edge("classifier", "tariff")
    graph.add_edge("tariff", "compliance")
    graph.add_edge("compliance", "sanctions")
    graph.add_edge("sanctions", "document")
    graph.add_edge("document", END)

    return graph.compile()


duty_break_graph = build_graph()


async def run_compliance_check(
    product_description: str,
    origin_country: str,
    destination_country: str,
    supplier_name: str | None = None,
) -> dict:
    initial_state: DutyBreakState = {
        "product_description": product_description,
        "origin_country": origin_country,
        "destination_country": destination_country,
        "supplier_name": supplier_name,
        "hs_code": "",
        "tariff_data": {},
        "compliance_data": {},
        "sanctions_data": {},
        "compliance_brief": {},
        "errors": [],
    }
    result = await duty_break_graph.ainvoke(initial_state)
    return result
