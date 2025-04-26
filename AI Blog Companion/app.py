import streamlit as st
from google import genai
from google.genai import types
import os

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r"Path-to-Json"


client = genai.Client(
    vertexai=True,
    project="Your-Project-id",
    location="us-central1",
    http_options=types.HttpOptions(api_version='v1')
)

model = "gemini-2.0-flash"

st.set_page_config(layout="wide")

st.title("Your Blog Writing Assistant")

st.subheader("Now create blogs with help of this assistant. Let the magic of AI help you in writing the blog.")

with st.sidebar:
    st.title("Input Blog Details")
    st.subheader("Enter details of the blog you want to generate")

    blog_title = st.text_input("Blog Title")

    keywords = st.text_area("Keywords (comma-seperated)")

    num_words = st.slider("Number of words", min_value=250, max_value=1000, step=250)

    submit_button = st.button("Generate Blog")

    blog = ""
    if submit_button:
        prompt = f"""Generate a comprehensive, engaging blog post relevant to the given title: '{blog_title}' and keywords: '{keywords}'. The blog should be approximately {num_words} words in length, suitable for an online audience. Ensure the content is original, informative, and maintains a consistent tone throughout."""
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_text(text=prompt),
                ],
            ),
        ]
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            blog += chunk.text


if submit_button:
    st.write(blog)
