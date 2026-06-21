import re

PLUGIN_NAME = "Calculator"

TRIGGERS = [
    "calculate",
    "math"
]

def execute(command):
    clean_cmd = command.replace("calculate", "").replace("math", "").strip()
    clean_cmd = clean_cmd.replace("times", "*").replace("x", "*").replace("plus", "+").replace("minus", "-").replace("divided by", "/")
    
    try:
        safe_expr = re.sub(r'[^0-9\+\-\*\/\.]', '', clean_cmd)
        if not safe_expr:
            return "I couldn't hear the numbers properly."
            
        result = eval(safe_expr)
        return f"The answer is {result}"
    except Exception:
        return "I ran into an error calculating that."