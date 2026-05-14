OFFTOPIC = [
    "salary",
    "visa",
    "immigration",
    "politics",
    "medical",
    "religion"
]

INJECTION = [
    "ignore previous instructions",
    "reveal system prompt",
    "bypass"
]


def detect_offtopic(text):

    lower = text.lower()

    for word in OFFTOPIC:

        if word in lower:
            return True

    return False


def detect_injection(text):

    lower = text.lower()

    for word in INJECTION:

        if word in lower:
            return True

    return False
