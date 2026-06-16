import string
import math

STRENGTH_COLOURS = {
    "Not Generated": "#9491A7",
    "Weak": "#E05C5C",
    "Medium": "#E09A3A",
    "Strong": "#4CAF75",
    "Very Strong": "#00E676",
}


def calculate_strength(password: str) -> tuple[int, str]:
    """Returns the numeric score (0-7) and category of the password."""
    score = 0
    n = len(password)

    if n >= 16:
        score += 3
    elif n >= 12:
        score += 2
    elif n >= 8:
        score += 1

    if any(c in string.ascii_uppercase for c in password): score += 1
    if any(c in string.ascii_lowercase for c in password): score += 1
    if any(c in string.digits for c in password): score += 1
    if any(c not in string.ascii_letters + string.digits for c in password): score += 1

    if score <= 2:
        category = "Weak"
    elif score <= 4:
        category = "Medium"
    elif score <= 6:
        category = "Strong"
    else:
        category = "Very Strong"

    return score, category


def calculate_entropy(length: int, pool_size: int) -> float:
    """Calculates the information entropy in bits."""
    if pool_size == 0 or length == 0:
        return 0.0
    return length * math.log2(pool_size)