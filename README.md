# 💻 CodeCoach AI

Paste or upload code and choose what you want:
- **Explain simply** - step-by-step beginner explanation
- **Find bugs** - issues with fixed code
- **Improve code** - better version of your code
- **Add comments** - same code with helpful comments
- **Time complexity** - Big-O explanation

Built with **Streamlit** and **Google Gemini Flash**.

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```
Paste your Gemini API key in the sidebar (free key: https://aistudio.google.com/apikey).

## Deploy on Streamlit Community Cloud
1. Push `app.py`, `README.md` and `requirements.txt` to a public GitHub repo.
2. Go to https://share.streamlit.io and create a new app (main file: `app.py`).
3. In **Advanced settings → Secrets** add:
   ```
   GEMINI_API_KEY = "your-key-here"
   ```

## Notes
- Code longer than 20,000 characters is trimmed.
- The model name can be changed in the sidebar.
