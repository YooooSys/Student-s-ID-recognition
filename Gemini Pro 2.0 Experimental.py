from openai import OpenAI
import base64

import streamlit as st

API_KEY = st.secrets["general"]["API_KEY"]
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY,
)

st.title("Student's ID recognizer (Ultimate version)")

# File uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

# Encode an image to base64
def encode_image(image):
    file_bytes = image.read()
    
    # Encode the bytes to base64
    base64_image = base64.b64encode(file_bytes).decode("utf-8")

def Proccess(image) -> str:


    # Encode the image
    try:
        completion = client.chat.completions.create(
            model="google/gemini-2.5-pro-exp-03-25:free",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "what is the number after the Mã số sinh viên (which is Student's id) (only return result. Note: The number contains exactly 7 digit, no letter, no special character, always start with 2, return null if there's no result)"},
                        {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{encode_image(image)}"}}
                    ]
                }
            ]
        )
        if completion and hasattr(completion, 'choices') and completion.choices:
            return completion.choices[0].message.content
        else:
            print("No valid response from API")
            print(completion)  # Debug raw response
    
    except Exception as e:
        print(f"API call failed: {e}")



if st.button("Proccess"):

    if uploaded_file is not None:
        st.write(Proccess(uploaded_file))
        st.image(uploaded_file, caption='Result', use_container_width=True)
    else:
        st.write("Please provide an image.")
