import os

import pandas as pd
import plotly.express as px
import streamlit as st

from labeler import label_comment

# ---- Settings ----------------------------------------------------------
TITLE = "Second Wind Resale"
ICON = "📦"
LOW_RATING, HIGH_RATING = 2, 4      # 2 stars or fewer is low, 4 stars or more is high
CSV_FILE = "feedback.csv"
COLORS = {"happy": "#2BB38A", "shipping": "#3B82F6", "condition": "#B34700",
          "listing": "#E0A800", "communication": "#8B5CF6", "unclear": "#D0D0D0"}
# ------------------------------------------------------------------------

st.set_page_config(page_title=TITLE, page_icon=ICON, layout="wide")
st.title(f"{ICON} {TITLE}")
st.caption("Customers leave feedback. The app labels it and saves it. The owner analyzes it later.")

# Load the saved feedback, or start with an empty table
if os.path.exists(CSV_FILE):
    df = pd.read_csv(CSV_FILE)
else:
    df = pd.DataFrame(columns=["comment", "rating", "label"])

tab_customer, tab_owner = st.tabs(["Customer: leave feedback", "Owner: analyze the feedback"])

# ---- Customer tab: type feedback, pick stars, get a label, save --------------
with tab_customer:
    st.subheader("How was your order?")
    with st.form("feedback_form", clear_on_submit=True):
        comment = st.text_area("Your comment")
        stars = st.feedback("stars")          # nothing until clicked, then 0 to 4
        submitted = st.form_submit_button("Send feedback")

    if submitted:
        if not comment.strip() or stars is None:
            st.error("Please type a comment and choose a star rating.")
        else:
            label = label_comment(comment.strip())
            new_row = pd.DataFrame([{"comment": comment.strip(), "rating": stars + 1, "label": label}])
            pd.concat([df, new_row], ignore_index=True).to_csv(CSV_FILE, index=False)
            df = pd.read_csv(CSV_FILE)
            st.success("Thank you for your feedback!")
            st.caption(f"Behind the scenes, the app labeled it: {label}")

# ---- Owner tab: analyze the feedback ----------------------------------------
with tab_owner:
    if df.empty:
        st.info("No feedback yet. Switch to the customer tab and add the first comment.")
    else:
        # Comments to read carefully: the label and the rating disagree, or the label is unclear
        complaint = ~df["label"].isin(["happy", "unclear"])
        flag = ((df["label"] == "happy") & (df["rating"] <= LOW_RATING)) \
             | (complaint & (df["rating"] >= HIGH_RATING)) \
             | (df["label"] == "unclear")

        st.subheader("What are customers saying?")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Comments", len(df))
        m2.metric("Happy", f"{(df['label'] == 'happy').mean():.0%}")
        m3.metric("Average stars", f"{df['rating'].mean():.1f}")
        m4.metric("Read carefully", int(flag.sum()))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.caption("Number of comments by label")
            counts = df["label"].value_counts().rename_axis("label").reset_index(name="count")
            fig = px.bar(counts, x="label", y="count", color="label", text="count",
                         color_discrete_map=COLORS)
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Comments")
            st.plotly_chart(fig, width="stretch")

        with col2:
            st.caption("Average stars by label")
            avg = df.groupby("label")["rating"].mean().round(1).reset_index()
            fig = px.bar(avg, x="label", y="rating", color="label", text="rating",
                         color_discrete_map=COLORS, range_y=[0, 5])
            fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Average stars")
            st.plotly_chart(fig, width="stretch")

        with col3:
            st.caption("Stars given, colored by label")
            by_stars = df.groupby(["rating", "label"]).size().reset_index(name="count")
            fig = px.bar(by_stars, x="rating", y="count", color="label", color_discrete_map=COLORS)
            fig.update_layout(xaxis_title="Stars", yaxis_title="Comments", legend_title_text=None)
            st.plotly_chart(fig, width="stretch")

        st.subheader("Read these carefully")
        st.caption("The label and the rating disagree (happy with a low rating, a complaint with a high "
                   "rating), or the label is unclear.")
        st.dataframe(df[flag], hide_index=True, width="stretch")

        with st.expander("All feedback"):
            st.dataframe(df, hide_index=True, width="stretch")
        st.download_button("Download CSV", df.to_csv(index=False), file_name="feedback.csv")
        st.caption("On the free Streamlit Cloud, the saved file can disappear when the app restarts. "
                   "Download your CSV to keep it.")
