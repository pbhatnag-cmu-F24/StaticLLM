from langchain.tools import BaseTool
from langchain_community.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from typing import Type
from pydantic import BaseModel, Field, PrivateAttr
import json

class LLMSemanticInput(BaseModel):
    query: str = Field(..., description="A full description of the class to analyze including method names, LOC, and class name.")

class LLMSemanticTool(BaseTool):
    name: str = "LLMSemanticTool"
    description: str = (
        "Analyzes class design for SRP violations using LOC, method names, and class name. "
        "Input must be a JSON string with keys: class_name, loc, method_names."
    )

    args_schema: Type[BaseModel] = LLMSemanticInput
    _llm:ChatOpenAI = PrivateAttr()

    def __init__(self, llm=None, **kwargs):
        super().__init__(**kwargs)
        self._llm = llm or ChatOpenAI(temperature=0)

    def _run(self, query: str) -> str:
        import json
        import re
        from langchain.schema import SystemMessage, HumanMessage

        # Strip markdown ```json ... ``` block if present
        if query.strip().startswith("```json"):
            query = re.sub(r"```json\s*|\s*```", "", query.strip())

        try:
            data = json.loads(query)
        except json.JSONDecodeError:
            return "- SRP Violation: Unknown\n- Reason: Input was not valid JSON."

        class_name = data.get("class_name", "").strip()
        method_names = data.get("method_names", [])
        loc = data.get("loc", 0)

        if not class_name or not method_names or not loc:
            return "- SRP Violation: Unknown\n- Reason: Missing LOC, class name, or method names."

        method_str = ", ".join(method_names)

        prompt = [
            SystemMessage(content="You are a static code analysis expert specialized in object-oriented design."),
            HumanMessage(content=(
                f"Class Name: {class_name}\n"
                f"Method Names: {method_str}\n"
                f"Lines of Code: {loc}\n\n"
                "Does this class violate the Single Responsibility Principle (SRP)?\n"
                "Respond in this format:\n"
                "- SRP Violation: Yes/No\n"
                "- Reason: <brief explanation>"
            ))
        ]

        response = self._llm.invoke(prompt)
        return response.content

