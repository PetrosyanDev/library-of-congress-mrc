import re

def format_text(string):
    return string.rstrip("/:, ").strip()


def format_name(name):
    parts = name.strip().split(",")
    return f'{parts[1].strip(". ")} {parts[0].strip(". ")}' if len(parts) >= 2 else name

def find_isbn(string):
    pattern10 = r"\d{10}"
    pattern13 = r"(?i)\d{13}|\d{13}-\d{1}"

    for pattern in [pattern10, pattern13]:
        match = re.search(pattern, string)

    return match.group() if match else ""

def find_ddc(string):
    if string == "[Fic]":
        return "FIC"
    match = re.search(r'^\d+', string)
    if not match:
        return ""
    
    num = int(match.group())
    if num >= 800 and num < 900:
        return "FIC"
    return str(num)

def find_integer(string, additional=""):
    match = re.search(r'\d+', string)
    return match.group()+additional if match else ""