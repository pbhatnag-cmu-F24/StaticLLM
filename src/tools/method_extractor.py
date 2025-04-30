# src/tools/method_extractor.py

from langchain.tools import BaseTool
from typing import Type, List
from pydantic import BaseModel, Field
import re

class MethodExtractorInput(BaseModel):
    code: str = Field(..., description="Java class source code as string")

class ExtractMethodNamesTool(BaseTool):
    name: str = "ExtractMethodNamesTool"
    description: str = "Returns a list of method names from a Java class. Input must be full source code as a string."

    args_schema: Type[BaseModel] = MethodExtractorInput

    def _run(self, code: str) -> List[str]:
        if "class " not in code:
            raise ValueError("Invalid input: expected raw Java class code, not a description.")
        method_pattern = r'(public|private|protected)?\s+[\w<>\[\]]+\s+(\w+)\s*\('
        matches = re.findall(method_pattern, code)
        method_names = [match[1] for match in matches]
        return list(set(method_names))
