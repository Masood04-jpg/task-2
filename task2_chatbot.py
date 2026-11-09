"""
Task 2: Rule-based chatbot using regex pattern matching.
Topics: Greetings, Internship, Programming, AI/ML, Fun (jokes + time/date). Plus fallbacks + typo correction.
Run: python task2_chatbot.py      (type 'bye' to exit)
"""
import re
import random
import datetime
import difflib

# Order matters: the first matching intent wins, so specific intents go above general ones.
INTENTS = {
    "greeting": {
        "patterns": [r"\b(hi|hello|hey|hola|namaste)\b", r"good (morning|afternoon|evening)"],
        "responses": ["Hello! How can I help you today?", "Hi there! Ask me about internships, coding, or a joke."],
    },
    "how_are_you": {
        "patterns": [r"how are you", r"how('s| is) it going", r"what'?s up"],
        "responses": ["I'm just code, but running great! How about you?", "Doing well, thanks for asking!"],
    },
    "name": {
        "patterns": [r"\bname\b", r"who are you", r"what are you"],
        "responses": ["I'm PyBot, a rule-based chatbot built with Python and regex."],
    },
    "internship": {
        "patterns": [r"\b(internship|intern|task|tasks|week ?1|certificate|submission)\b"],
        "responses": [
            "For Week 1 you need to complete any 1 task: Neural Network, Chatbot, or Tic-Tac-Toe.",
            "Tip: push your code to GitHub with a clear README and share the link for submission.",
        ],
    },
    "define_coding": {
        "patterns": [r"what is (coding|programming)", r"what does (coding|programming) mean"],
        "responses": [
            "Coding is writing instructions in a language like Python that a computer can follow to solve a problem.",
        ],
    },
    "programming": {
        "patterns": [r"\b(python|code|coding|programming|bug|error|numpy|matplotlib|regex)\b"],
        "responses": [
            "Python tip: read the error message from the bottom up - the last line usually tells you the cause.",
            "NumPy tip: use vectorised operations instead of Python loops - they're much faster.",
            "Regex tip: test your patterns on regex101.com before putting them in code.",
        ],
    },
    "ai": {
        "patterns": [r"\b(ai|artificial intelligence|machine learning|neural network|minimax)\b"],
        "responses": [
            "AI is about building systems that perform tasks needing human-like intelligence - learning, reasoning, decision-making.",
            "A neural network learns by adjusting weights to reduce a loss using backpropagation.",
            "Minimax picks the move that maximises your minimum guaranteed outcome, assuming the opponent plays perfectly.",
        ],
    },
    "joke": {
        "patterns": [r"\b(joke|funny|laugh)\b"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "There are 10 kinds of people: those who understand binary and those who don't.",
            "A SQL query walks into a bar, walks up to two tables and asks: 'Can I join you?'",
        ],
    },
    "time": {
        "patterns": [r"\b(time|date|day|today)\b"],
        "responses": ["__TIME__"],
    },
    "thanks": {
        "patterns": [r"\b(thanks|thank you|thx)\b"],
        "responses": ["You're welcome!", "Happy to help!"],
    },
    "ok": {
        "patterns": [r"^(ok|okay|cool|nice|great|fine)\W*$"],
        "responses": ["Great! Anything else I can help with?", "Cool! Ask me about internships, coding, AI or a joke."],
    },
    "bye": {
        "patterns": [r"\b(bye|goodbye|exit|quit|see you)\b"],
        "responses": ["Goodbye! Happy coding!", "See you later!"],
    },
}

FALLBACKS = [
    "Sorry, I didn't get that. Try asking about internships, Python, AI, or ask for a joke.",
    "Hmm, I'm not sure how to respond. Could you rephrase?",
    "I'm still learning! Type 'help' to see what I can talk about.",
]
HELP = "I can chat about: greetings, the internship tasks, programming, AI/ML, jokes, and the time/date."

# Words used for typo correction
KEYWORDS = ["hello", "name", "joke", "internship", "python", "coding", "programming",
            "time", "date", "help", "bye", "goodbye", "thanks", "minimax", "numpy"]
# Normal words that must never be "corrected" into a keyword
SAFE_WORDS = {"what", "that", "this", "tell", "with", "your", "about", "have", "does", "mean",
              "give", "show", "take", "make", "more", "some", "when", "where", "which"}


def correct_typos(text):
    """Fix small spelling mistakes in words of 4+ letters, e.g. 'nmae' -> 'name'."""
    fixed = []
    for word in text.split():
        if len(word) >= 4 and word not in KEYWORDS and word not in SAFE_WORDS:
            match = difflib.get_close_matches(word, KEYWORDS, n=1, cutoff=0.75)
            fixed.append(match[0] if match else word)
        else:
            fixed.append(word)
    return " ".join(fixed)


def get_response(text):
    text = text.lower().strip()
    if re.search(r"\bhelp\b", text):
        return "help", HELP
    text = correct_typos(text)
    for name, intent in INTENTS.items():
        for pat in intent["patterns"]:
            if re.search(pat, text):
                reply = random.choice(intent["responses"])
                if reply == "__TIME__":
                    reply = "It's " + datetime.datetime.now().strftime("%A, %d %B %Y, %I:%M %p")
                return name, reply
    return "fallback", random.choice(FALLBACKS)


def main():
    print("PyBot: Hi! I'm PyBot. Type 'help' for topics or 'bye' to exit.")
    while True:
        try:
            user = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print("\nPyBot: Goodbye!")
            break
        if not user.strip():
            continue
        intent, reply = get_response(user)
        print(f"PyBot: {reply}")
        if intent == "bye":
            break


if __name__ == "__main__":
    main()