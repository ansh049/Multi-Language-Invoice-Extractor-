from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

# gemini-2.5-pro requires a paid Google Cloud billing account (Pro models were
# removed from the free tier). gemini-2.5-flash is still free-tier eligible
# and works well for this kind of structured extraction task.
GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-3.1-flash-lite')
model = genai.GenerativeModel(GEMINI_MODEL)

# ---------------------------------------------------------------------------
# Core functions (unchanged logic, just cleaned up)
# ---------------------------------------------------------------------------

def get_gemini_response(input_text, image, prompt):
    response = model.generate_content([input_text, image[0], prompt])
    return response.text


def input_image_details(uploaded_file):
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data,
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")


DEFAULT_PROMPT = """You are an expert in extracting information from invoices.
Please extract the following information from the invoice image provided:"""

QUICK_PROMPTS = {
    "Summary": "Summarize the key details of this invoice: vendor, date, invoice number, and total amount.",
    "Line items": "List every line item on this invoice with quantity, unit price, and total price.",
    "Totals check": "Extract the subtotal, tax, discounts, and grand total, and verify that they add up correctly.",
    "Vendor & buyer info": "Extract the vendor's name/address and the buyer's name/address from this invoice.",
    "Due date": "What is the invoice due date and payment terms mentioned on this invoice?",
}

# ---------------------------------------------------------------------------
# Page config & styling
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Invoice Extractor",
    page_icon="🧾",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
        /* Overall background */
        .stApp {
            background: linear-gradient(180deg, #0f1117 0%, #161a23 100%);
        }

        /* Header */
        .app-title {
            font-size: 2.4rem;
            font-weight: 800;
            background: linear-gradient(90deg, #7dd3fc, #a78bfa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.1rem;
        }
        .app-subtitle {
            color: #9ca3af;
            font-size: 1.02rem;
            margin-bottom: 1.6rem;
        }

        /* Card containers */
        .card {
            background: #1a1e2a;
            border: 1px solid #2a2f3d;
            border-radius: 14px;
            padding: 1.4rem 1.5rem;
            margin-bottom: 1rem;
        }

        /* Buttons */
        div.stButton > button {
            background: linear-gradient(90deg, #6366f1, #8b5cf6);
            color: white;
            border: none;
            border-radius: 10px;
            padding: 0.6rem 1.4rem;
            font-weight: 600;
            font-size: 1rem;
            transition: transform 0.15s ease, box-shadow 0.15s ease;
            width: 100%;
        }
        div.stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 18px rgba(139, 92, 246, 0.35);
        }

        /* Text input */
        .stTextInput > div > div > input {
            background-color: #11141c;
            border: 1px solid #2a2f3d;
            border-radius: 10px;
            color: #e5e7eb;
        }

        /* File uploader */
        section[data-testid="stFileUploaderDropzone"] {
            background-color: #11141c;
            border: 1.5px dashed #3f3f52;
            border-radius: 12px;
        }

        /* Result box */
        .result-box {
            background: #11141c;
            border-left: 4px solid #8b5cf6;
            border-radius: 8px;
            padding: 1.2rem 1.4rem;
            color: #e5e7eb;
            line-height: 1.6;
        }

        /* Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #12141b;
            border-right: 1px solid #2a2f3d;
        }

        .pill {
            display: inline-block;
            background: #22263344;
            border: 1px solid #363b4a;
            border-radius: 999px;
            padding: 0.15rem 0.7rem;
            font-size: 0.8rem;
            color: #a5b4fc;
            margin-right: 0.3rem;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.markdown("### 🧾 Invoice Extractor")
    st.markdown(
        "Upload an invoice image and ask Gemini anything about it — "
        "totals, vendor details, line items, due dates, and more."
    )
    st.divider()

    st.markdown("**How to use**")
    st.markdown(
        "1. Upload a `jpg`, `jpeg`, or `png` invoice\n"
        "2. Pick a quick prompt or write your own\n"
        "3. Click **Extract Details**"
    )
    st.divider()

    st.markdown("**Quick prompts**")
    for label, text in QUICK_PROMPTS.items():
        if st.button(label, key=f"quick_{label}", use_container_width=True):
            st.session_state["input"] = text

    st.divider()
    st.caption("Powered by Google Gemini 2.5 Pro")

# ---------------------------------------------------------------------------
# Main layout
# ---------------------------------------------------------------------------

st.markdown('<div class="app-title">Invoice Extractor</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="app-subtitle">AI-powered invoice reading — upload an image, ask a question, get structured answers.</div>',
    unsafe_allow_html=True,
)

left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 📤 Upload invoice")
    uploaded_file = st.file_uploader(
        "Choose an image", type=["jpg", "png", "jpeg"], label_visibility="collapsed"
    )

    image = None
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded invoice", use_container_width=True)
    else:
        st.info("No image uploaded yet. Supported formats: JPG, JPEG, PNG.")
    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown("#### 💬 Ask a question")
    input_text = st.text_input(
        "Input Prompt",
        key="input",
        placeholder="e.g. What is the total amount and due date?",
        label_visibility="collapsed",
    )
    st.markdown(
        '<span class="pill">Tip: use a Quick prompt from the sidebar</span>',
        unsafe_allow_html=True,
    )
    st.write("")
    submit = st.button("🔍 Extract Details", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    result_placeholder = st.empty()

    if submit:
        if uploaded_file is None:
            st.warning("Please upload an invoice image before submitting.")
        elif not input_text.strip():
            st.warning("Please enter a question or select a quick prompt.")
        else:
            try:
                with st.spinner("Analyzing invoice with Gemini..."):
                    image_data = input_image_details(uploaded_file)
                    response = get_gemini_response(DEFAULT_PROMPT, image_data, input_text)

                st.markdown("#### ✅ Result")
                st.markdown(f'<div class="result-box">{response}</div>', unsafe_allow_html=True)
            except Exception as e:
                err_text = str(e)
                if "429" in err_text or "quota" in err_text.lower():
                    st.error(
                        "Gemini API quota exceeded. If you're using `gemini-2.5-pro`, "
                        "note that Pro models now require a paid Google Cloud billing "
                        "account — the free tier only covers Flash models. Try setting "
                        "`GEMINI_MODEL=gemini-2.5-flash` in your `.env`, or enable billing "
                        "at https://ai.dev/rate-limit."
                    )
                else:
                    st.error(f"Something went wrong while processing the invoice: {e}")
