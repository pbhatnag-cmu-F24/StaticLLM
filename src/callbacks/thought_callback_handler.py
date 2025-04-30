# src/callbacks/thought_callback_handler.py

from langchain.callbacks.base import BaseCallbackHandler

class ThoughtCallbackHandler(BaseCallbackHandler):
    def __init__(self):
        self.steps = []  # Stores trace

    def on_agent_action(self, action, **kwargs):
        print(f"\n🧠 Agent Thought:\nUsing Tool: {action.tool}\nInput: {action.tool_input}")
        self.steps.append({
            "type": "action",
            "tool": action.tool,
            "tool_input": action.tool_input
        })

    def on_tool_end(self, output, **kwargs):
        print(f"📥 Tool Output:\n{output}")
        self.steps.append({
            "type": "observation",
            "output": output
        })
