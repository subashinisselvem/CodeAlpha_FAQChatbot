from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
from urllib.parse import urlparse

from dotenv import load_dotenv
from google import genai

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# ========================================
# LOAD ENVIRONMENT VARIABLES
# ========================================

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check your .env file."
    )


# ========================================
# GEMINI CLIENT
# ========================================

client = genai.Client(
    api_key=GEMINI_API_KEY
)


# ========================================
# FAQ DATA
# ========================================

faqs = [
    {
        "question": "what is codealpha",
        "answer": "CodeAlpha is an organization that provides internship opportunities and practical learning experiences for students."
    },
    {
        "question": "how can i apply for internship",
        "answer": "You can apply for an internship through the official CodeAlpha internship process."
    },
    {
        "question": "what technologies can i use",
        "answer": "You can use technologies such as HTML, CSS, JavaScript, Python, Java, Node.js, and other technologies depending on your project."
    },
    {
        "question": "how do i submit my project",
        "answer": "Complete your project, upload the source code to GitHub, create the required LinkedIn post or video, and submit the project through the required CodeAlpha submission form."
    },
    {
        "question": "what is an internship",
        "answer": "An internship is a practical learning experience where students work on real or simulated projects to improve their technical and professional skills."
    },
    {
        "question": "what is a chatbot",
        "answer": "A chatbot is a software application that communicates with users and provides responses to their questions."
    },
    {
        "question": "how long is the internship",
        "answer": "The internship duration depends on the program and the internship requirements."
    },
    {
        "question": "why should i use github",
        "answer": "GitHub is used to store, manage, and share your project source code."
    },
    {
        "question": "why should i post on linkedin",
        "answer": "LinkedIn helps you showcase your project, share your learning experience, and demonstrate your technical skills."
    },
    {
        "question": "will i get a certificate",
        "answer": "Certificate eligibility depends on completing the internship requirements and following the organization's guidelines."
    },
    {
        "question": "what are project requirements",
        "answer": "Project requirements depend on the assigned task. You should complete the required features, test your project, upload the source code to GitHub, and submit it according to the internship instructions."
    }
]


# ========================================
# PREPARE TF-IDF MODEL
# ========================================

questions = [
    faq["question"]
    for faq in faqs
]

vectorizer = TfidfVectorizer(
    lowercase=True,
    stop_words="english"
)

faq_vectors = vectorizer.fit_transform(
    questions
)


# ========================================
# GEMINI GENERAL AI
# ========================================

def ask_gemini(user_question):

    try:

        prompt = f"""
You are a helpful AI assistant inside an FAQ chatbot.

Answer the user's question clearly and accurately.

Keep the answer reasonably short and easy to understand.

User question:
{user_question}
"""

        chat = client.chats.create(
            model="gemini-3.8-flash"
        )

        response = chat.send_message(
            prompt
        )

        return response.text

    except Exception as error:

        print("Gemini error:", repr(error))
        raise


# ========================================
# FIND FAQ ANSWER
# ========================================

def find_answer(user_question):

    user_vector = vectorizer.transform(
        [user_question]
    )

    similarities = cosine_similarity(
        user_vector,
        faq_vectors
    )[0]

    best_index = similarities.argmax()

    best_score = similarities[best_index]

    print(
        "Similarity score:",
        round(float(best_score), 3)
    )


    # ========================================
    # FAQ MATCH
    # ========================================

    if best_score >= 0.25:

        return {
            "answer": faqs[best_index]["answer"],
            "source": "FAQ",
            "confidence": round(
                float(best_score),
                3
            )
        }


    # ========================================
    # GENERAL AI
    # ========================================

    print("No FAQ match. Sending to Gemini...")

    general_answer = ask_gemini(
        user_question
    )

    return {
        "answer": general_answer,
        "source": "Gemini AI",
        "confidence": round(
            float(best_score),
            3
        )
    }


# ========================================
# HTTP SERVER
# ========================================

class ChatbotHandler(BaseHTTPRequestHandler):


    # ========================================
    # SEND JSON RESPONSE
    # ========================================

    def send_json(
        self,
        status_code,
        data
    ):

        response = json.dumps(
            data,
            ensure_ascii=False
        )

        self.send_response(
            status_code
        )

        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )

        self.send_header(
            "Access-Control-Allow-Origin",
            "*"
        )

        self.send_header(
            "Access-Control-Allow-Headers",
            "Content-Type"
        )

        self.send_header(
            "Access-Control-Allow-Methods",
            "POST, OPTIONS"
        )

        self.end_headers()

        self.wfile.write(
            response.encode("utf-8")
        )


    # ========================================
    # OPTIONS
    # ========================================

    def do_OPTIONS(self):

        self.send_json(
            200,
            {
                "message": "OK"
            }
        )


    # ========================================
    # GET
    # ========================================

    def do_GET(self):

        if urlparse(self.path).path == "/":

            self.send_json(
                200,
                {
                    "message":
                    "AI FAQ Chatbot backend is running!"
                }
            )

        else:

            self.send_json(
                404,
                {
                    "error":
                    "Not found"
                }
            )


    # ========================================
    # POST
    # ========================================

    def do_POST(self):

        if urlparse(self.path).path != "/api/chat":

            self.send_json(
                404,
                {
                    "error":
                    "Endpoint not found"
                }
            )

            return


        try:

            content_length = int(
                self.headers.get(
                    "Content-Length",
                    0
                )
            )

            body = self.rfile.read(
                content_length
            )

            data = json.loads(
                body.decode("utf-8")
            )

            question = data.get(
                "question",
                ""
            ).strip()


            # ========================================
            # CHECK QUESTION
            # ========================================

            if not question:

                self.send_json(
                    400,
                    {
                        "error":
                        "Question is required"
                    }
                )

                return


            # ========================================
            # GET ANSWER
            # ========================================

            result = find_answer(
                question
            )


            self.send_json(
                200,
                result
            )


        except Exception as error:

            print(
                "Server error:",
                error
            )

            self.send_json(
                500,
                {
                    "error":
                    "Chatbot server error"
                }
            )


# ========================================
# START SERVER
# ========================================

server = HTTPServer(
    ("localhost", 5001),
    ChatbotHandler
)

print(
    "AI FAQ Chatbot backend running on "
    "http://localhost:5001"
)

server.serve_forever()