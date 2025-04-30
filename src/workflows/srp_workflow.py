from src.agent.srp_agent import create_srp_agent

def run_srp_analysis(class_code: str, class_name: str = "UnknownClass", callbacks=None) -> dict:
    agent = create_srp_agent()

    if not class_code.strip().startswith("public class") and "class " not in class_code:
        raise ValueError("The uploaded file does not seem to contain valid Java class code.")


    # Pass only raw prompt, and let the agent decide what tools to use
    prompt = f"""You are a static analysis agent. Your task is to determine whether the following Java class violates the Single Responsibility Principle (SRP).

You have the following tools available:
- CountLOCTool: gives you the number of lines of code in the class.
- ExtractMethodNamesTool: gives you a list of method names in the class.
- LLMSemanticTool: takes structured metadata (like LOC, methods, etc.) and returns a judgment on SRP compliance.

You may use any tools as needed. If you feel you have enough information, proceed directly to analysis.

Class Name: {class_name}

Java Code:
{class_code}

At the end, provide:
- SRP Violation: Yes/No
- Reason: <explanation>
- Tools Used: <comma-separated list or 'None'>
"""

    result = agent.run(prompt, callbacks=callbacks)

    steps = []
    if callbacks:
        for cb in callbacks:
            if hasattr(cb, "steps"):
                steps = cb.steps

    return {
        "class_name": class_name,
        "violation_analysis": result,
        "trace": steps
    }

