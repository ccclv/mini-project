import random
from flask import Flask

app = Flask(__name__)

VERSION = "Version 1"
secret_number = random.randint(1, 100)


def check_guess(guess, secret):
    if guess < secret:
        return "Too LOW"
    if guess > secret:
        return "Too HIGH"
    return "Correct!"


@app.route("/")
def home():
    return """
    <style>
      body {
        font-family: Arial, sans-serif;
        background: #f0f4f8;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 100vh;
        margin: 0;
        text-align: center;
      }
      input {
        padding: 10px;
        font-size: 16px;
        width: 120px;
        text-align: center;
        border: 1px solid #aaa;
        border-radius: 6px;
      }
      button {
        padding: 10px 18px;
        font-size: 16px;
        border: none;
        border-radius: 6px;
        background: #3b82f6;
        color: white;
        cursor: pointer;
      }
      button:hover { background: #2563eb; }
      #result { font-size: 24px; font-weight: bold; margin-top: 20px; }
      .low { color: #dc2626; }
      .high { color: #ca8a04; }
      .correct { color: #16a34a; }
    </style>
    <h1>Guess the Number</h1>
    <p>I'm thinking of a number between 1 and 100.</p>
    <div>
      <input id="guess" type="number" min="1" max="100" placeholder="Your guess">
      <button onclick="sendGuess()">Guess</button>
      <button onclick="newGame()">New game</button>
    </div>
    <p id="result"></p>
    <script>
      async function sendGuess() {
        const n = document.getElementById("guess").value;
        if (n === "") return;
        const res = await fetch("/guess/" + n);
        const text = await res.text();
        const result = document.getElementById("result");
        result.innerText = text;
        if (text === "Too LOW") result.className = "low";
        else if (text === "Too HIGH") result.className = "high";
        else result.className = "correct";
      }
      async function newGame() {
        const res = await fetch("/reset");
        const result = document.getElementById("result");
        result.innerText = await res.text();
        result.className = "";
      }
    </script>
    """


@app.route("/guess/<int:guess>")
def guess_number(guess):
    return check_guess(guess, secret_number)


@app.route("/reset")
def reset_game():
    global secret_number
    secret_number = random.randint(1, 100)
    return "New game started"


@app.route("/health")
def health():
    return "ok"


@app.route("/version")
def version():
    return VERSION


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)