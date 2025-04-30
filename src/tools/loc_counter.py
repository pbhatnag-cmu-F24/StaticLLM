# src/tools/loc_counter.py

from langchain.tools import BaseTool
from typing import Optional, Type
from pydantic import BaseModel, Field

class LOCCounterInput(BaseModel):
    code: str = Field(..., description="The Java source code for a class")

class CountLOCTool(BaseTool):
    name: str = "CountLOCTool"
    description: str = "Returns the number of lines of code in a Java class. Input must be full source code as a string."

    args_schema: Type[BaseModel] = LOCCounterInput

    def _run(self, code: str) -> int:
        if "class " not in code:
            raise ValueError("Invalid input: expected raw Java class code, not a description.")
        #TODO: Some comments starting with a <whitespace>* are creeing in, remove them
        lines = code.splitlines()
        meaningful_lines = [
            line for line in lines
            if line.strip() and not line.strip().startswith("//") and not line.strip().startswith("/*")
        ]
        return len(meaningful_lines)

    def _arun(self, code: str) -> int:
        raise NotImplementedError("Async not supported for CountLOCTool.")
