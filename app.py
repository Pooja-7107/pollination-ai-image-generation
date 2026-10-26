
import streamlit as st
import requests
from PIL import Image
from io import BytesIO
from urllib.parse import quote
import os
from dotenv import load_dotenv


# ============================================================
# LOAD ENVIRONMENT VARIABLES
# ============================================================

load_dotenv()

API_KEY = os.getenv("POLLINATIONS_API_KEY")


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="AI Image Generator",
    page_icon="🎨",
    layout="wide"
)


# ============================================================
# TITLE
# ============================================================

st.title("🎨 Pollinations AI Image Generator")

st.write(
    "Generate images using a text prompt."
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header("⚙️ Image Settings")

    width = st.selectbox(
        "Image Width",
        [512, 768, 1024],
        index=1
    )

    height = st.selectbox(
        "Image Height",
        [512, 768, 1024],
        index=1
    )

    model = st.selectbox(
        "Model",
        [
            "flux",
            "turbo"
        ]
    )

    seed = st.number_input(
        "Seed",
        min_value=0,
        value=42,
        step=1
    )

    st.info(
        "Change the seed to create a different variation."
    )


# ============================================================
# PROMPT
# ============================================================

prompt = st.text_area(
    "📝 Enter your image prompt",
    placeholder=(
        "Example: A futuristic Chennai city at night, "
        "neon lights, cyberpunk architecture, cinematic "
        "lighting, highly detailed"
    ),
    height=150
)


# ============================================================
# GENERATE BUTTON
# ============================================================

generate = st.button(
    "✨ Generate Image",
    type="primary",
    use_container_width=True
)


# ============================================================
# IMAGE GENERATION
# ============================================================

if generate:

    if not prompt.strip():

        st.warning(
            "Please enter an image prompt."
        )

        st.stop()


    with st.spinner(
        "🎨 Generating your image..."
    ):

        try:

            # Encode prompt safely for URL
            encoded_prompt = quote(
                prompt.strip()
            )

            # Pollinations image endpoint
            url = (
                f"https://image.pollinations.ai/prompt/"
                f"{encoded_prompt}"
                f"?width={width}"
                f"&height={height}"
                f"&seed={seed}"
                f"&model={model}"
            )


            # Headers
            headers = {}

            if API_KEY:
                headers["Authorization"] = (
                    f"Bearer {API_KEY}"
                )


            # Request image
            response = requests.get(
                url,
                headers=headers,
                timeout=120
            )


            # Check response
            if response.status_code != 200:

                st.error(
                    f"Image generation failed. "
                    f"HTTP Status: {response.status_code}"
                )

                st.stop()


            # Convert response to image
            image = Image.open(
                BytesIO(response.content)
            )


            # ====================================================
            # DISPLAY IMAGE
            # ====================================================

            st.success(
                "Image generated successfully!"
            )

            st.image(
                image,
                caption=prompt,
                use_container_width=True
            )


            # ====================================================
            # DOWNLOAD
            # ====================================================

            image_buffer = BytesIO()

            image.save(
                image_buffer,
                format="PNG"
            )

            st.download_button(
                label="⬇️ Download Image",
                data=image_buffer.getvalue(),
                file_name="pollinations_image.png",
                mime="image/png",
                use_container_width=True
            )


            # ====================================================
            # IMAGE INFORMATION
            # ====================================================

            with st.expander(
                "🔍 Image Information"
            ):

                st.write(
                    f"**Model:** {model}"
                )

                st.write(
                    f"**Width:** {width}px"
                )

                st.write(
                    f"**Height:** {height}px"
                )

                st.write(
                    f"**Seed:** {seed}"
                )

                st.write(
                    f"**Prompt:** {prompt}"
                )


        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. "
                "Please try again."
            )


        except Exception as e:

            st.error(
                f"Something went wrong: {e}"
            )

