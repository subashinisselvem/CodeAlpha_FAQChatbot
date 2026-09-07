# 🤖 CodeAlpha FAQ Chatbot

A simple AI-powered FAQ Chatbot developed as part of my CodeAlpha internship project.

## 🚀 Features

- 💬 Interactive chatbot interface
- 🔎 FAQ matching using TF-IDF and cosine similarity
- 🧠 Gemini AI for general questions
- ⚡ Real-time responses
- ⌨️ Enter key support
- 📱 Responsive design
- 🔐 API key protected using environment variables

## 🛠️ Technologies Used

- HTML
- CSS
- JavaScript
- Python
- Scikit-learn
- Google Gemini API

## 🧠 How It Works

The chatbot uses two methods to answer questions:

1. The user enters a question.
2. TF-IDF converts the question into a numerical representation.
3. Cosine similarity finds the closest FAQ.
4. If the similarity score is high enough, the FAQ answer is returned.
5. If there is no suitable FAQ match, the question is sent to Gemini AI.
6. Gemini generates a general AI response.

## 📁 Project Structure

```text
CodeAlpha_FAQChatbot/
├── backend/
│   └── app.py
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── .gitignore
└── README.md
```

## ▶️ How to Run

### 1. Install Python dependencies

```bash
python -m pip install scikit-learn google-genai python-dotenv
```

### 2. Create the `.env` file

Inside the `backend` folder, create a file named:

```text
.env
```

Add:

```text
GEMINI_API_KEY=your_gemini_api_key
```

### 3. Start the backend

Open the terminal in the `backend` folder and run:

```bash
python app.py
```

The backend will run at:

```text
http://localhost:5001
```

### 4. Open the chatbot

Open:

```text
frontend/index.html
```

in a web browser.

## 🔐 Security

The Gemini API key is stored in the `.env` file and is not uploaded to GitHub.

Never share your Gemini API key publicly.

## 👩‍💻 Internship Project

Developed as part of the **CodeAlpha Internship Program**.

## 📌 GitHub Repository

https://github.com/subashinisselvem/CodeAlpha_FAQChatbot