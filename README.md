# 📦 Second Wind Resale: buyer feedback

A small Streamlit app for an online resale shop that sells used items on eBay.
Buyers leave a comment and a star rating. An LLM (Groq, `openai/gpt-oss-20b`) labels each comment, and the app saves the comment, rating and label. The owner tab turns it into numbers, charts and a list of comments to read carefully.

## Business question

What is the main reason buyers are unhappy, so the shop knows what to fix first?

## Labels

Each comment gets exactly one label.

| Label | Definition |
|---|---|
| shipping | The package was slow, damaged in transit, or lost. |
| condition | The item is worn, dirty, broken, or does not work well. |
| listing | The item is not what the listing or photos said (wrong size, color, model, or missing parts). |
| communication | The seller replied slowly, rudely, or not at all. |
| happy | The buyer has no complaint. |

Rules for hard cases: praise plus a complaint gets the complaint's label; two complaints get the bigger problem; sarcasm counts as a complaint. If the model answers with anything outside the list, the comment is labeled `unclear`.

## Files

- `app.py`: the app (customer tab and owner tab)
- `labeler.py`: the labeling guide and the call to Groq
- `requirements.txt`: libraries for Streamlit Cloud

The Groq API key is stored as a Streamlit secret named `GROQ-API-KEY`, not in this repository.
