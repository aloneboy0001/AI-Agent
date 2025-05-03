# AI Article Summarizer (Streamlit App)

This is an AI-powered Streamlit web app that summarizes articles from URLs using Google's Gemini model via the SimplerLLM library.

## Features
- Input a URL to an article
- Summarizes the article into bullet points using LLM
- Powered by Gemini via SimplerLLM
- Clean UI with Streamlit

## Setup Instructions

### 1. Clone the repo
```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Add your API key (do NOT commit it!)
Create a file: `.streamlit/secrets.toml`
```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

### 4. Run the app
```bash
streamlit run main.py
```

---

### Deployment on Streamlit Cloud
- Push your code to GitHub (without `.streamlit/secrets.toml`)
- Go to [Streamlit Cloud](https://streamlit.io/cloud)
- Deploy the app from your GitHub repo
- In the app **Settings > Secrets**, paste:

```toml
GEMINI_API_KEY = "your-gemini-api-key-here"
```

Enjoy summarizing!