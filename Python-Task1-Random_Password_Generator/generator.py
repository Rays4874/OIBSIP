import secrets
import string


def generate_custom_password(length, use_upper, use_lower, use_digits, use_sym, excl_ambig, prev_rep):
    """Generates a password based on strict rules and returns (password, pool_size, types_count)."""
    pool_str = ""
    mandatory_groups = []

    if use_upper:
        pool_str += string.ascii_uppercase
        mandatory_groups.append(string.ascii_uppercase)
    if use_lower:
        pool_str += string.ascii_lowercase
        mandatory_groups.append(string.ascii_lowercase)
    if use_digits:
        pool_str += string.digits
        mandatory_groups.append(string.digits)
    if use_sym:
        symbols = "!@#$%^&*()-_=+[]{}|;:,.<>?/"
        pool_str += symbols
        mandatory_groups.append(symbols)

    if not pool_str:
        raise ValueError("Please select at least one character type.")

    if excl_ambig:
        ambiguous = "0OIl15S2Z"
        pool_str = "".join([c for c in pool_str if c not in ambiguous])
        cleaned_groups = []
        for group in mandatory_groups:
            clean_group = "".join([c for c in group if c not in ambiguous])
            if clean_group:
                cleaned_groups.append(clean_group)
        mandatory_groups = cleaned_groups

    if not pool_str:
        raise ValueError("Excluding ambiguous characters left the pool empty.")

    pool_size = len(set(pool_str))

    if prev_rep:
        if length > pool_size:
            raise ValueError(
                f"Cannot generate a {length}-character password without repeating characters. Only {pool_size} unique characters available.")

        available = set(pool_str)
        chars = []

        for group in mandatory_groups:
            valid_choices = list(set(group) & available)
            if valid_choices:
                choice = secrets.choice(valid_choices)
                chars.append(choice)
                available.remove(choice)

        if len(chars) < length:
            secure_sampler = secrets.SystemRandom()
            chars.extend(secure_sampler.sample(list(available), length - len(chars)))

    else:
        guaranteed = [secrets.choice(g) for g in mandatory_groups]
        filler = [secrets.choice(pool_str) for _ in range(length - len(guaranteed))]
        chars = guaranteed + filler
        
    for i in range(len(chars) - 1, 0, -1):
        j = secrets.randbelow(i + 1)
        chars[i], chars[j] = chars[j], chars[i]

    return "".join(chars), pool_size, len(mandatory_groups)
