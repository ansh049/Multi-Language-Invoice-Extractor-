# 🧾 Invoice Extractor

An AI-powered Streamlit app that reads invoice images and answers questions about them using Google's Gemini API — extract totals, line items, vendor details, due dates, and more from a photo or scan of an invoice.

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-app-red.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## ✨ Features

- 📤 Upload an invoice image (`jpg`, `jpeg`, `png`)
- 💬 Ask any natural-language question about it
- ⚡ Quick prompt buttons for common queries (summary, line items, totals check, vendor info, due date)
- 🎨 Clean, dark-themed UI with a two-column layout
- 🛡️ Friendly error handling for missing files, empty prompts, and API quota limits

## 🖼️ Preview

Upload an invoice on the left, ask a question on the right, and get a structured answer back — no manual data entry required.

## 🚀 Getting Started

### Prerequisites

- Python 3.9+
- A [Google AI Studio](https://ai.google.dev/) API key

### Installation

```bash
git clone https://github.com/<your-username>/invoice-extractor.git
cd invoice-extractor
pip install -r requirements.txt
```

### Configuration

Create a `.env` file in the project root:

```env
GOOGLE_API_KEY=your_google_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```

> **Note on models:** Google moved Gemini Pro models behind paid billing — the free tier now only covers Flash and Flash-Lite models. This app defaults to `gemini-2.5-flash`, which works well for invoice extraction and is free-tier eligible. If you have billing enabled and want higher-reasoning output, set `GEMINI_MODEL=gemini-2.5-pro` instead.

### Run the app

```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`.

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/) — UI framework
- [google-generativeai](https://pypi.org/project/google-generativeai/) — Gemini API SDK
- [Pillow](https://pypi.org/project/Pillow/) — image handling
- [python-dotenv](https://pypi.org/project/python-dotenv/) — environment variable management

## 📁 Project Structure

```
invoice-extractor/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── .env                # API keys (not committed)
└── README.md
```

## 🔑 Getting a Google API Key

1. Go to [Google AI Studio](https://ai.google.dev/)
2. Sign in and click **Get API Key**
3. Create a new key and paste it into your `.env` file

## ⚠️ Troubleshooting

**`429 Quota exceeded` error** — You're likely trying to use a Pro model on the free tier. Switch `GEMINI_MODEL` in `.env` to `gemini-2.5-flash`, or enable billing on your Google Cloud project for Pro access.

**`FileNotFoundError: No file uploaded`** — Make sure you've selected an image before clicking "Extract Details."

## 📄 License

This project is licensed under the MIT License — feel free to use and modify it.

## 🙏 Acknowledgements

Built with [Streamlit](https://streamlit.io/) and [Google Gemini](https://ai.google.dev/).