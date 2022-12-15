from PyPDF2 import PdfReader as pyPdfReader
from pdfminer.high_level import extract_text
from pdfminer.layout import LAParams
import curses.ascii

SPECIAL_CHARS_MAPPING = {
    curses.ascii.DC1: " ",
    curses.ascii.DC2: " ",
    curses.ascii.DC3: " ",
    curses.ascii.DC4: " ",
    curses.ascii.SI: " ",
    curses.ascii.SYN: " ",
    curses.ascii.ETX: " ",
    curses.ascii.ETB: " ",
    curses.ascii.NAK: " ",
    curses.ascii.EM: " ",
    curses.ascii.FS: " ",
    curses.ascii.GS: " ",
    curses.ascii.TAB: " ",
    curses.ascii.CR: "\n",
    curses.ascii.LF: "\n",
    curses.ascii.FF: "\n"
}


class PdfReader(object):
    def __init__(self, file, *args, **kwargs):
        self._input_file = file
        self.pages = []
        self._content = ""

    @property
    def content(self):
        if not self._content:
            self.read_file_pypdf()
        return self._content

    def read_file_pypdf(self):
        reader = pyPdfReader(self._input_file)
        for page in reader.pages:
            clean_content = self.clean_content(page.extract_text())
            self.pages.append(clean_content)
            self._content += "\n" + clean_content
        return self._content

    def read_file_pdfminer(self):
        laparams = LAParams()
        return self.clean_content(extract_text(self._input_file, laparams=laparams))

    def remove_non_ascii_2(self, content):
        # encode using ASCII encoding and drop all non-ASCII characters
        return content.encode('ascii', errors='ignore').decode().translate(SPECIAL_CHARS_MAPPING)

    def clean_content(self, content):
        return self.remove_non_ascii_2(content).replace("&amp;", "&").replace("\xa0", " ").replace("\x18", " ").replace("\x08", " ")
