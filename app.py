"""CodeCoach AI - paste or upload code and get a simple explanation,
bug check, improvements, comments or complexity analysis from Gemini Flash."""

import streamlit as st
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemini-2.5-flash"
MAX_CHARS = 20000
CODE_EXTENSIONS = ["py", "js", "ts", "java", "c", "cpp", "cs", "go", "php", "rb", "html", "css", "sql", "txt"]

TASKS = {
    "Explain simply": "Explain what this code does step by step in simple language for a beginner. "
                      "End with a short summary of the overall purpose.",
    "Find bugs": "Find bugs, errors and risky parts. For each issue give: the line or snippet, "
                 "why it is a problem, and the fixed code. If there are no bugs, say so.",
    "Improve code": "Suggest improvements for readability, performance and best practices. "
                    "Then show the full improved version of the code.",
    "Add comments": "Return the same code with clear helpful comments added. Do not change the logic.",
    "Time complexity": "Explain the time and space complexity (Big-O) of the main parts, "
                       "with a short reason for each.",
}


# ---------- helpers (pure functions, easy to test) ----------
def prepare_code(raw: str):
    """Trim code and cut it if too long. Returns (code, was_trimmed)."""
    code = raw.strip()
    if len(code) > MAX_CHARS:
        return code[:MAX_CHARS], True
    return code, False


def build_prompt(code: str, task: str, language: str) -> str:
    lang = "Detect the programming language automatically." if language == "Auto-detect" else f"The language is {language}."
    return f"""You are a patient senior programmer and teacher. {lang}

TASK: {TASKS[task]}

Reply in Markdown. Put all code inside fenced code blocks.

CODE:
```
{code}
```"""


def ask_gemini(client, model: str, prompt: str) -> str:
    config = types.GenerateContentConfig(temperature=0.3)
    response = client.models.generate_content(model=model, contents=prompt, config=config)
    return response.text or ""


# ---------- UI ----------
def main():
    st.set_page_config(page_title="CodeCoach AI", page_icon="💻", layout="centered")
    st.title("💻 CodeCoach AI")
    st.caption("Paste or upload code and get help understanding and improving it.")

    with st.sidebar:
        st.header("Settings")
        try:
            api_key = st.secrets["GEMINI_API_KEY"]
        except Exception:
            api_key = ""
        if not api_key:
            api_key = st.text_input("Gemini API key", type="password")
        model = st.text_input("Model name", value=DEFAULT_MODEL)

    task = st.radio("What do you want?", list(TASKS), horizontal=True)
    language = st.selectbox(
        "Language", ["Auto-detect", "Python", "JavaScript", "Java", "C", "C++", "C#", "Go", "PHP", "SQL", "HTML/CSS"]
    )
    uploaded = st.file_uploader("Upload a code file (optional)", type=CODE_EXTENSIONS)
    pasted = st.text_area("Or paste your code here", height=250)

    if st.button("Analyze code", type="primary"):
        if not api_key:
            st.error("Please enter your Gemini API key in the sidebar.")
            st.stop()

        raw = uploaded.read().decode("utf-8", errors="ignore") if uploaded else pasted
        code, trimmed = prepare_code(raw)
        if not code:
            st.error("Please paste some code or upload a file.")
            st.stop()
        if trimmed:
            st.warning(f"Code is long, using only the first {MAX_CHARS} characters.")

        try:
            client = genai.Client(api_key=api_key)
            with st.spinner("Reading your code..."):
                st.session_state["result"] = ask_gemini(client, model, build_prompt(code, task, language))
        except Exception as e:
            st.error(f"Something went wrong: {e}")
            st.stop()

    if st.session_state.get("result"):
        st.divider()
        st.markdown(st.session_state["result"])
        st.download_button("Download result", st.session_state["result"], "codecoach_result.md")


if __name__ == "__main__":
    main()
