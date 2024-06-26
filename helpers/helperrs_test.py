from pymarc import MARCReader, record
from tkinter import Tk, filedialog

from .format import process_line
from .models import BookInfo

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

bookFields = {
    "245": {1: ["a", "book_name"]},
    "100": {2: ["a", "author"]},
    "---": {3: ["a", "other_authors"]},
    "---": {4: ["a", "author_company"]},
    "020": {5: ["a", "isbn"]},
    "082": {6: ["a", "ddc_classification"]},
    "300": {7: ["a", "page_count"], 8: ["c", "book_length"]},
    "---": {9: ["a", "material_type"]},
    "250": {10: ["a", "edition"]},
    "260": {11: ["c", "publication_year"], 12: ["a", "publication_country"], 13: ["b", "publishing_agency"]},
    "264": {11: ["c", "publication_year"], 12: ["a", "publication_country"], 13: ["b", "publishing_agency"]},
    "---": {14: ["a", "language_of_origin"]},
    "---": {15: ["a", "translation"]},
    "---": {16: ["a", "copy_numbers"]},
    "856": {17: ["a", "electronic_resources"]},
    "---": {18: ["a", "book_location"]},
    "---": {19: ["a", "book_status"]},
    "520": {20: ["a", "contents"]},
}


def getBookInfo(file_path: str) -> BookInfo:
    book_info = BookInfo()
    records = decode_marc(file_path)

    # Getting all the separate fields
    for field in records[0].get_fields():
        # Checking if tag is in bookFields
        if field.tag not in bookFields or field.is_control_field():
            continue

        # Getting all the keys of tag map
        for key in bookFields[field.tag]:
            # Iterating through every subfield
            for sub in field.subfields:
                # If we need that subfield, append
                if sub.code == bookFields[field.tag][key][0]:
                    setattr(book_info, bookFields[field.tag][key][1], sub.value)

    # Processing Lines
    for i in range(20):
        # Find the attribute name based on the current index (i+1)
        attr = next((bookFields[tag][i+1][1] for tag in bookFields if (i+1) in bookFields[tag]), None)
        if attr:
            current_value = getattr(book_info, attr)
            processed_value = process_line(i, current_value)
            setattr(book_info, attr, processed_value)

    return book_info

