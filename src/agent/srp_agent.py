# src/agent/srp_agent.py

from langchain.agents import initialize_agent, AgentType
from langchain_community.chat_models import ChatOpenAI
from langchain.tools import Tool
from langchain.schema import SystemMessage
from dotenv import load_dotenv
from typing import List
import os

# Tools
from src.tools.loc_counter import CountLOCTool
from src.tools.method_extractor import ExtractMethodNamesTool
from src.tools.llm_semantic_tool import LLMSemanticTool

load_dotenv()

def create_srp_agent():
    # Validate required environment variables
    openai_key = os.getenv("OPENAI_API_KEY")
    if not openai_key:
        raise ValueError("OPENAI_API_KEY is missing.")

    prompt_path = os.getenv("FEW_SHOT_SRP_PROMPT_PATH")
    if not prompt_path or not os.path.exists(prompt_path):
        raise FileNotFoundError(f"Few-shot prompt file not found at: {prompt_path}")

    with open(prompt_path, "r", encoding="utf-8") as f:
        prompt_text = f.read()

    system_prompt = SystemMessage(content=prompt_text)

    # (OpenAI for now)
    llm = ChatOpenAI(
        temperature=0,
        model="gpt-4o",
        openai_api_key=openai_key
    )

    # from langchain.llms import LlamaCpp
    # llm = LlamaCpp(
    #     model_path="models/llama/Llama3.2-3B-Instruct-int4-qlora-eo8/Llama-3.2-3B-Instruct-f16.gguf",
    #     temperature=0,
    #     max_tokens=1024,
    #     n_ctx=2048,
    #     verbose=True
    # )

    tools: List[Tool] = [
        CountLOCTool(),
        ExtractMethodNamesTool(),
        LLMSemanticTool(llm=llm)
    ]

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        agent_kwargs={
            "system_message": system_prompt
        }
    )

    return agent
