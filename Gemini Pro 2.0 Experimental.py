from openai import OpenAI
import base64

import streamlit as st


st.title("Digit Recognizer")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Encode an image to base64
def encode_image(image):
    return base64.b64encode(image.getvalue()).decode("utf-8")

def Proccess(image) -> str:
    API_KEY = st.secrets["general"]["API_KEY"]
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=API_KEY,
    )

    # Encode the image
    base64_image = encode_image(image)

    # Send a request to the OpenRouter API with the image
    completion = client.chat.completions.create(
        extra_headers={
            "HTTP-Referer": "your_site_url_here",
            "X-Title": "your_site_name_here"
        },
        model="google/gemini-2.0-pro-exp-02-05:free",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "what is the number after the Mã số sinh viên (which is Student's id) (only return result. Note: The number contains exactly 7 digit, no letter, no special character, always start with 2, return null if there's no result)"},

                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}}
                ]
            }
        ]
    )

    return completion.choices[0].message.content


if st.button("Student's ID recognition (Ultimate version)"):

    if uploaded_file is not None:
        st.write(Proccess(uploaded_file))
    else:
        st.write("Please provide an image.")
