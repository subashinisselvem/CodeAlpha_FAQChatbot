const userInput = document.getElementById("userInput");
const sendBtn = document.getElementById("sendBtn");
const chatBox = document.getElementById("chatBox");

// ========================================
// ADD MESSAGE
// ========================================

function addMessage(message, type) {

    const messageElement = document.createElement("div");

    messageElement.classList.add(
        type === "user"
            ? "user-message"
            : "bot-message"
    );

    messageElement.textContent = message;

    chatBox.appendChild(messageElement);

    chatBox.scrollTop = chatBox.scrollHeight;
}


// ========================================
// SEND MESSAGE TO AI BACKEND
// ========================================

async function sendMessage() {

    const question = userInput.value.trim();

    if (question === "") {
        return;
    }

    // Show user message
    addMessage(question, "user");

    // Clear input
    userInput.value = "";

    // Focus input
    userInput.focus();

    // Show typing message
    const typingMessage = document.createElement("div");

    typingMessage.classList.add("bot-message");
    typingMessage.textContent = "🤖 AI is thinking...";

    chatBox.appendChild(typingMessage);

    chatBox.scrollTop = chatBox.scrollHeight;

    try {

        // Send question to Python AI backend
        const response = await fetch(
            "http://localhost:5001/api/chat",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify({
                    question: question
                })
            }
        );

        const data = await response.json();

        // Remove typing message
        typingMessage.remove();

        if (!response.ok) {

            addMessage(
                "Sorry, something went wrong with the AI chatbot.",
                "bot"
            );

            return;
        }

        // Show AI answer
        addMessage(
            data.answer,
            "bot"
        );

    } catch (error) {

        console.error("Error:", error);

        typingMessage.remove();

        addMessage(
            "❌ Cannot connect to the AI backend. Please make sure the Python server is running.",
            "bot"
        );
    }
}


// ========================================
// SEND BUTTON
// ========================================

sendBtn.addEventListener(
    "click",
    sendMessage
);


// ========================================
// ENTER KEY
// ========================================

userInput.addEventListener(
    "keydown",
    (event) => {

        if (event.key === "Enter") {
            sendMessage();
        }

    }
);