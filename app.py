import streamlit as st
import json
from src.workflows.srp_workflow import run_srp_analysis
from src.callbacks.thought_callback_handler import ThoughtCallbackHandler

st.set_page_config(page_title="SRP Code Analyzer", layout="centered")
st.title("📏 SRP Code Violation Analyzer")

uploaded_file = st.file_uploader("Upload a Java class file", type=["java"])

if uploaded_file:
    class_code = uploaded_file.read().decode("utf-8")
    class_name = uploaded_file.name.replace(".java", "")

    st.subheader("Java Class Content")
    st.code(class_code, language="java")

    if st.button("🔍 Analyze for SRP Violation"):
        with st.spinner("Running agent analysis..."):
            callback = ThoughtCallbackHandler()
            result = run_srp_analysis(class_code, class_name, callbacks=[callback])
            st.success("Analysis Complete!")

            st.subheader("🧠 Agent's Verdict")
            st.markdown(result["violation_analysis"])

            st.subheader("🔍 Agent Trace")

            for i, step in enumerate(result["trace"]):
                if step["type"] == "action":
                    with st.expander(f"🛠 Tool Called: {step['tool']}"):
                        tool_input = step.get("tool_input", "[input not recorded]")

                        st.markdown("**📨 Tool Input:**")
                        # Try to pretty-print JSON
                        try:
                            parsed = json.loads(tool_input)
                            st.json(parsed)
                        except:
                            # Fallback for code or plain text
                            st.code(tool_input, language="java" if "class" in tool_input else "text")

                elif step["type"] == "observation":
                    with st.expander("📥 Tool Output"):
                        st.markdown(step["output"])
