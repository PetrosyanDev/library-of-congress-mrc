class BookInfo:
    def __init__(self):
        self.book_name = ""
        self.author = ""
        self.other_authors = ""
        self.author_company = ""
        self.isbn = ""
        self.ddc_classification = ""
        self.page_count = ""
        self.book_length = ""
        self.material_type = ""
        self.edition = ""
        self.publication_year = ""
        self.publication_country = ""
        self.publishing_agency = ""
        self.language_of_origin = ""
        self.translation = ""
        self.copy_numbers = ""
        self.electronic_resources = ""
        self.book_location = ""
        self.book_status = ""
        self.contents = ""

    def __repr__(self):
        return "BookInfo(" + ", ".join(f"{attr}='{getattr(self, attr)}'" for attr in ['book_name', 'author', 'other_authors', 'author_company', 'isbn', 'ddc_classification', 'page_count', 'book_length', 'material_type', 'edition', 'publication_year', 'publication_country', 'publishing_agency', 'language_of_origin', 'translation', 'copy_numbers', 'electronic_resources', 'book_location', 'book_status', 'contents']) + ")"

    def getList(self) -> list[str]:
        return [getattr(self, attr) for attr in [
            'book_name', 'author', 'other_authors', 'author_company', 'isbn', 'ddc_classification',
            'page_count', 'book_length', 'material_type', 'edition', 'publication_year', 'publication_country',
            'publishing_agency', 'language_of_origin', 'translation', 'copy_numbers', 'electronic_resources',
            'book_location', 'book_status', 'contents'
        ]]