import pyjokes

PLUGIN_NAME = "Joke"

TRIGGERS = [
    "tell me a joke",
    "make me laugh",
    "say something funny"
]

def execute(command):
    try:
        joke = pyjokes.get_joke()
        return joke
    except Exception as e:
        return "I tried to think of a joke, but my humor module experienced a runtime error."