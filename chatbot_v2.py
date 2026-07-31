"""
Retrieval-based Chatbot - Version 2
------------------------------------
What's new vs v1:

1. Data is now organized as "INTENTS" instead of flat question/answer pairs.
   An intent = a topic (like "greeting" or "joke"), with:
     - several PATTERNS (different ways a user might phrase it)
     - several RESPONSES (different replies, chosen at random)

   This is a big step toward how real chatbots (and even early versions
   of virtual assistants like Siri) were built: you don't need to predict
   every possible sentence, just enough patterns per topic to catch the
   most common phrasings.

2. Responses are randomized per intent, so the bot feels less robotic.

3. Matching now compares the user input against EVERY pattern of EVERY
   intent, and picks whichever intent had the single best-matching pattern.
"""

import random

# -----------------------------
# 1. The knowledge base (intents)
# -----------------------------
intents = [
    {
        "tag": "greeting",
        "patterns": ["hello", "hi", "hi there", "hey", "good morning", "good afternoon", "yo"],
        "responses": [
            "Hi there! How can I help you?",
            "Hello! What can I do for you?",
            "Hey! Good to see you.",
        ],
    },
    {
        "tag": "goodbye",
        "patterns": ["bye", "goodbye", "see you later", "see you", "farewell", "i am leaving", "have to go"],
        "responses": [
            "Goodbye! Have a great day!",
            "See you! Take care.",
            "Bye! Come back anytime.",
        ],
    },
    {
        "tag": "thanks",
        "patterns": ["thank you", "thanks", "thanks a lot", "appreciate it", "thank you so much"],
        "responses": [
            "You're welcome!",
            "No problem, happy to help!",
            "Anytime!",
        ],
    },
    {
        "tag": "name",
        "patterns": ["what is your name", "who are you", "what should i call you", "your name"],
        "responses": [
            "I'm ChatBot, nice to meet you!",
            "You can call me ChatBot.",
            "I'm a simple retrieval-based chatbot, built by you!",
        ],
    },
    {
        "tag": "mood",
        "patterns": ["how are you", "how are you doing", "how do you feel", "whats up", "how is it going"],
        "responses": [
            "I'm doing great, thanks for asking!",
            "Feeling good, ready to chat!",
            "All good on my end. How about you?",
        ],
    },
    {
        "tag": "capabilities",
        "patterns": ["what can you do", "help me", "what are your features", "how do you work"],
        "responses": [
            "I can chat with you using pattern matching, tell jokes, and learn new topics as you add them!",
            "Right now I match your message against known patterns and reply. Try asking me for a joke!",
        ],
    },
    {
        "tag": "joke",
        "patterns": ["tell me a joke", "make me laugh", "say something funny", "know any jokes", "joke please"],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "I told my computer I needed a break, and now it won't stop sending me KitKats.",
            "Why do Java developers wear glasses? Because they don't C sharp.",
            "There are 10 types of people in the world: those who understand binary and those who don't.",
            "I would tell you a UDP joke, but you might not get it.",
        ],
    },
    {
        "tag": "identity_check",
        "patterns": ["are you a robot", "are you human", "are you real", "are you a bot"],
        "responses": [
            "I'm a chatbot! Software all the way down.",
            "Yep, 100% code, no humans hiding in here.",
        ],
    },
    {
        "tag": "compliment",
        "patterns": ["you are smart", "you are cool", "good bot", "nice job", "you are awesome"],
        "responses": [
            "Thank you! I'm still learning though.",
            "Aw, thanks! You're pretty great yourself.",
        ],
    },
    {
        "tag": "insult",
        "patterns": ["you are dumb", "you are stupid", "you are bad", "bad bot"],
        "responses": [
            "That's fair, I'm still a work in progress!",
            "Ouch. I'll try to do better.",
        ],
    },
    {
        "tag": "age",
        "patterns": ["how old are you", "when were you created", "your age"],
        "responses": [
            "I don't have an age, I was just written into existence today!",
            "Age is just a variable I don't track.",
        ],
    },
    {
        "tag": "creator",
        "patterns": ["who made you", "who created you", "who built you", "who is your creator"],
        "responses": [
            "I was built by a systems engineering student, learning chatbot development step by step!",
        ],
    },
]

CONFIDENCE_THRESHOLD = 1


# -----------------------------
# 2. Text preprocessing
# -----------------------------
def preprocess(text):
    text = text.lower()
    for punct in [",", ".", "!", "?", "'", '"', ";", ":"]:
        text = text.replace(punct, "")
    return text.split()


# -----------------------------
# 3. Similarity scoring
# -----------------------------
def word_overlap_score(tokens_a, tokens_b):
    set_a, set_b = set(tokens_a), set(tokens_b)
    return len(set_a.intersection(set_b))


# -----------------------------
# 4. Finding the best matching intent
# -----------------------------
def get_response(user_input):
    user_tokens = preprocess(user_input)

    best_score = 0
    best_intent = None

    for intent in intents:
        for pattern in intent["patterns"]:
            pattern_tokens = preprocess(pattern)
            score = word_overlap_score(user_tokens, pattern_tokens)

            if score > best_score:
                best_score = score
                best_intent = intent

    if best_score >= CONFIDENCE_THRESHOLD and best_intent is not None:
        return random.choice(best_intent["responses"])
    else:
        return "Sorry, I don't understand. Could you rephrase that?"


# -----------------------------
# 5. Chat loop
# -----------------------------
def main():
    print("ChatBot: Hi! Type 'quit' to exit. Try asking for a joke!\n")

    while True:
        user_input = input("You: ")

        if user_input.lower() in ["quit", "exit"]:
            print("ChatBot: Goodbye!")
            break

        response = get_response(user_input)
        print(f"ChatBot: {response}\n")


if __name__ == "__main__":
    main()
