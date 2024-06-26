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

def process_line(i, line):
    actions = {
        1: format_text,
        2: format_name,
        5: find_isbn,
        6: find_ddc,
        7: find_integer,
        8: lambda x: find_integer(x, additional=" cm"),
        9: lambda _: "Book",
        11: find_integer,
        12: format_text,
        13: format_text,
        14: lambda _: "English",
        15: lambda _: "No translation",
        19: lambda _: "Available for circulation"
    }
    function = actions.get(i+1)
    return function(line) if function else line