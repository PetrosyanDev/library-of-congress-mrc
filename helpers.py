from pymarc import MARCReader, record
from tkinter import Tk, filedialog

from format import *

def select_file() -> str:
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(filetypes=[("MARC files", "*.mrc")])
    
    return file_path

def decode_marc(file_path) -> list[record.Record]:
    records = []
    with open(file_path, 'rb') as file:
        reader = MARCReader(file)
        for record in reader:
            records.append(record)
    return records

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

bookFields =  {
    "245": {1: ["a", "Name Of The Book"]},
    "100": {2: ["a", "Author"]},
    "1--": {3: ["a", "Other Authors"]},
    "12-": {4: ["a", "Other Authors (Company)"]},
    "020": {5: ["a", "ISBN"]},
    "082": {6: ["a", "DDC"]},
    "300": {7: ["a", "Pages"], 8: ["c", "Length"]},
    "sss": {9: ["a", "Material Type"]},
    "250": {10: ["a", "Edition"]},
    "260": {12: ["a", "Location"], 13: ["b", "Publishing Company"], 11: ["c", "Year"]},
    "264": {12: ["a", "Location"], 13: ["b", "Publishing Company"], 11: ["c", "Year"]},
    "---": {14: ["a", "Language"]},
    "12-": {15: ["a", "Translation"]},
    "---": {16: ["a", "Copy Numbers"]},
    "856": {17: ["a", "Resources"]},
    "---": {18: ["a", "Book Location"]},
    "---": {19: ["a", "Book Status"]},
    "520": {20: ["a", "Description"]},
}

def getBookInfo(file_path: str) -> list[str]:
    bookInfo = [""]*20

    records = decode_marc(file_path)

    # Getting All the Seperate Fields
    for field in records[0].get_fields():

        # Checking if tag is in bookFields
        if field.tag not in bookFields or field.is_control_field():
            continue

        # Getting all the keys of tag map
        for key in bookFields[field.tag]:

            # Iterating through every subfield
            for sub in field.subfields:

                # IF we need that subfield, append
                if sub.code == bookFields[field.tag][key][0]:
                    bookInfo[key-1] = sub.value
                    # print(bookFields[field.tag][key][1], "Found")

    # Processing Lines
    for i in range(len(bookInfo)):
        bookInfo[i] = process_line(i, bookInfo[i])

    return bookInfo