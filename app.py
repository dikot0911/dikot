from flask import Flask, request
import openai
import os
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Masukkan API Key OpenAI dan Twilio dari environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/bot", methods=["POST"])
def bot():
    incoming_msg = request.values.get("Body", "").strip()
    response = MessagingResponse()
    msg = response.message()

    if incoming_msg:
        # Kirim pertanyaan ke OpenAI GPT
        try:
            reply = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": incoming_msg}]
            )
            msg.body(reply["choices"][0]["message"]["content"])
        except Exception as e:
            msg.body("Maaf, terjadi kesalahan. Coba lagi nanti!")

    return str(response)

# Tambahkan endpoint /health
@app.route("/health", methods=["GET"])
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
