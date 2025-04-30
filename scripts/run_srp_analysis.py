import argparse
from src.workflows.srp_workflow import run_srp_analysis
from src.callbacks.thought_callback_handler import ThoughtCallbackHandler
from dotenv import load_dotenv
load_dotenv()

def load_file_as_string(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run SRP analysis on a Java class.")
    parser.add_argument("file", type=str, help="Path to the Java file to analyze")
    args = parser.parse_args()

    code = load_file_as_string(args.file)
    class_name = args.file.split("/")[-1].replace(".java", "")

    callbacks = [ThoughtCallbackHandler()]

    result = run_srp_analysis(code, class_name, callbacks=callbacks)

    print("\nSRP Analysis Result:\n")
    print(result["violation_analysis"])
