import requests
import streamlit as st

# ---- Settings ----------------------------------------------------------
BUSINESS = "a small online resale shop that sells used items on eBay"
LABELS = ["shipping", "condition", "listing", "communication", "happy"]
GUIDE = """Label the comment with exactly one word from this list: shipping, condition, listing, communication, happy.
shipping: the package was slow, damaged in transit, or lost.
condition: the item is worn, dirty, broken or does not work well.
listing: the item is not what the listing or photos said (wrong size, color, model, or missing parts).
communication: the seller replied slowly, rudely, or not at all.
happy: the buyer has no complaint.
If the comment has praise and a complaint, label the complaint.
If it has more than one complaint, label the bigger problem.
Sarcasm counts as a complaint.
Reply with the one word only."""
MODEL = "openai/gpt-oss-20b"   # if you get a 404, the model was retired: see console.groq.com/docs/models
URL = "https://api.groq.com/openai/v1/chat/completions"
# ------------------------------------------------------------------------


def label_comment(text):
    key = st.secrets["GROQ-API-KEY"]
    prompt = f"You label customer comments for {BUSINESS}.\n{GUIDE}\n\nComment: {text}"
    response = requests.post(
        URL,
        headers={"Authorization": f"Bearer {key}"},
        json={"model": MODEL, "temperature": 0,
              "messages": [{"role": "user", "content": prompt}]},
        timeout=30,
    )
    response.raise_for_status()
    answer = response.json()["choices"][0]["message"]["content"]
    label = answer.strip().strip(".").lower()
    return label if label in LABELS else "unclear"
