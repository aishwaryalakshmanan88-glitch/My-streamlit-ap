import os
from pathlib import Path

import openai
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

FAQ_PATH = Path(__file__).parent / "docs" / "faq.txt"


def load_faq_text() -> str:
    if FAQ_PATH.exists():
        return FAQ_PATH.read_text(encoding="utf-8")
    return ""


def query(user_prompt: str) -> dict:
    api_key = st.secrets.get("openai_api_key") or os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OpenAI API key not found. Set st.secrets['openai_api_key'] or OPENAI_API_KEY."
        )

    openai.api_key = api_key

    faq_text = load_faq_text()
    system_message = (
        "You are a helpful assistant. Answer the user's question using the FAQ below. "
        "If the answer is not contained in the FAQ, say that you don't know."
    )
    messages = [
        {"role": "system", "content": system_message},
        {"role": "system", "content": f"FAQ:\n{faq_text}"},
        {"role": "user", "content": user_prompt},
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.2,
        max_tokens=600,
    )

    return {"answer": response.choices[0].message.content.strip()}
