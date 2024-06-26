import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

import os
import clipboard
import helpers
import openai_text

ctk.set_default_color_theme("green")

# Sample app dimensions
appWidth = 600
appHeight = 700

column_titles = [
    'Book Name', 'Author', 'Other Authors',
    'Author Company', 'ISBN', 'DDC classification',
    'Page Count', 'Book length', 'Material Type',
    'Edition', 'Publication year', 'Publication country',
    'Publishing agency', 'Language of origin',
    'Translation', 'Copy Numbers', 'Electr. Resources', 'Book location',
    'Book status', 'Contents'
]

class App(ctk.CTk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.bookInfos = []

        self.title(" Book Data Helper")
        self.geometry(f"{appWidth}x{appHeight}")
        self.minsize(width=500, height=600)

        # Configure grid weights for the window
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create a scrollable frame for the main content
        self.scrollable_frame = ctk.CTkScrollableFrame(self, width=appWidth)
        self.scrollable_frame.grid(row=0, column=0, columnspan=4, rowspan=1, sticky="nsew")
        for i in range(6):
            self.scrollable_frame.grid_columnconfigure(i, weight=1)

        # Browse Files Button
        self.browseFilesButton = ctk.CTkButton(self.scrollable_frame, text="Browse Files", command=self.fileBrowse, height=120, font=ctk.CTkFont(size=14, weight="normal"), fg_color="#03A6A6", hover_color="#04BFBF")
        self.browseFilesButton.grid(row=0, column=0, columnspan=6, padx=20, pady=20, sticky="ew")

        # Text Label
        self.nameLabel = ctk.CTkLabel(self.scrollable_frame, text="Book Information:", font=ctk.CTkFont(size=20, weight="bold"))
        self.nameLabel.grid(row=1, column=0, padx=20, sticky="w")

        # Books Frame
        self.books_frame = ctk.CTkFrame(self.scrollable_frame, width=appWidth, height=0)
        self.books_frame.grid(row=2, column=0, padx=20, columnspan=6, pady=(0, 20), rowspan=1, sticky="nsew")
        self.books_frame.grid_columnconfigure(1, weight=4)

        self.copyAllBtn = ctk.CTkButton(self)

        # Detailed Info Frame
        self.detail_frame = ctk.CTkFrame(self, width=appWidth)
        self.detail_frame.grid(row=0, column=0, columnspan=4, rowspan=1, sticky="nsew")
        self.detail_frame.grid_columnconfigure(0, weight=1)
        self.detail_frame.grid_rowconfigure(1, weight=1)
        self.detail_frame.grid_remove()  # Hide initially

        self.back_button = ctk.CTkButton(self.detail_frame, text="Back", command=self.show_main_frame)
        self.back_button.grid(row=0, column=0, padx=20, pady=20, sticky="nw")

        self.detail_content_frame = ctk.CTkScrollableFrame(self.detail_frame)
        self.detail_content_frame.grid(row=1, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="nsew")
        self.detail_content_frame.grid_columnconfigure(0, weight=1)

        self.updateDisplay()

    def fileBrowse(self):
        file_path = helpers.select_file()
        if not file_path and not os.path.exists(file_path):
            CTkMessagebox(title="Error", message="Wrong File Path!!!", icon="cancel", justify="center")
            return

        bookInfo = helpers.getBookInfo(file_path)
        self.bookInfos.append(bookInfo)

        self.updateDisplay()

    def updateDisplay(self):
        self.clear_book_frame(self.books_frame)

        if not self.bookInfos:
            index_label = ctk.CTkLabel(self.books_frame, text="No books loaded yet.")
            index_label.grid(row=0, column=0, pady=(10, 0), sticky="e")  # Specify row
            return

        for index, bookInfo in enumerate(self.bookInfos):
            # Create index label
            index_label = ctk.CTkLabel(self.books_frame, text=f"{index+1}:")
            index_label.grid(row=index, column=0, pady=(10, 0), sticky="w")  # Specify row

            # Create title label
            title_label = ctk.CTkLabel(self.books_frame, text=bookInfo[0])
            title_label.grid(row=index, column=1, padx=(10, 0), pady=(10, 0), sticky="w")  # Specify row

            # Create button
            button = ctk.CTkButton(self.books_frame, text="View", command=lambda bookInfo=bookInfo: self.show_detail_frame(bookInfo))
            button.grid(row=index, column=2, pady=(10, 0), sticky="e")  # Specify row

            # Create delete button
            del_button = ctk.CTkButton(self.books_frame, text="X", command=lambda index=index: self.del_book_info(index), fg_color="red", hover_color="darkred", width=25)
            del_button.grid(row=index, column=3, padx=(10, 0), pady=(10, 0), sticky="e")  # Specify row

        # Copy Full button
        self.copyAllBtn = ctk.CTkButton(self, text="Copy All", height=40, command=lambda text=self.convertListToGSText(): self.copy_to_clipboard(text), font=ctk.CTkFont(size=14, weight="bold"), fg_color="#007bff", hover_color="#0062cc")
        self.copyAllBtn.grid(row=3, column=0, columnspan=4, padx=20, pady=20, sticky="nsew")

    def show_detail_frame(self, bookInfo):
        try:
            self.scrollable_frame.grid_remove()
            self.clear_book_frame(self.detail_content_frame)
        except:
            pass

        self.copy_book_detailed_button = ctk.CTkButton(self.detail_frame, text="Copy All", command=lambda text="\t".join(bookInfo): self.copy_to_clipboard(text))
        self.copy_book_detailed_button.grid(row=0, column=1, padx=20, pady=20, sticky="nw")

        for idx, info in enumerate(bookInfo):
            title = column_titles[idx]
            row_frame = ctk.CTkFrame(self.detail_content_frame)
            row_frame.grid(row=idx, column=0, pady=4, sticky="ew")
            row_frame.grid_columnconfigure(1, weight=1)

            title_label = ctk.CTkLabel(row_frame, text=f"{title}:")
            title_label.grid(row=0, column=0, padx=(10, 0), sticky="w")

            info_label = ctk.CTkLabel(row_frame, text=info if info else "N/A")
            info_label.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="w")

            if info:
                copy_button = ctk.CTkButton(row_frame, width=60, text="Copy", command=lambda text=info: self.copy_to_clipboard(text), fg_color="#007bff", hover_color="#0062cc")
                copy_button.grid(row=0, column=2, padx=(10, 15), sticky="e")
            elif title == "Contents":
                generateBtn = ctk.CTkButton(row_frame, width=100, text="Generate", command=lambda bookInfo=bookInfo: self.generateDescription(bookInfo))
                generateBtn.grid(row=0, column=2, padx=(10, 15), sticky="e")

        self.detail_frame.grid()
    
    def generateDescription(self, bookInfo):
        index = self.bookInfos.index(bookInfo)
        
        if bookInfo[0] and bookInfo[1]:
            prompt = f"Give me a description for {bookInfo[0]} by {bookInfo[1]}"
        elif bookInfo[0]:
            prompt = f"Give me a description for {bookInfo[0]}"
        else:
            prompt = f"Give me a description for"
        if bookInfo[4]:
            prompt += f" {bookInfo[4]}"

        bookInfo[-1] = openai_text.GenerateText(prompt)
        self.bookInfos[index] = bookInfo

        self.show_detail_frame(bookInfo)

    def show_main_frame(self):
        self.detail_frame.grid_remove()
        self.scrollable_frame.grid()
        self.updateDisplay()

    def copy_to_clipboard(self, text):
        clipboard.copy(text)

    def del_book_info(self, index):
        self.bookInfos.pop(index)
        self.updateDisplay()

    def convertListToGSText(self):
        return "\n".join(["\t".join(row) for row in self.bookInfos])

    def fullBook(self, index):
        self.bookInfos.pop(index)
        self.updateDisplay()

    def clear_book_frame(self, frame):
        for widgets in frame.winfo_children():
            widgets.destroy()
        self.copyAllBtn.destroy()

    def on_closing(self):
        self.destroy()