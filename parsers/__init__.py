import re

from parsers.reader import PdfReader
from parsers.base import BasePolicyParser
from parsers.sbi import SbiPolicyParser
from parsers.new_india import NewIndiaPolicyParser
from parsers.icici_lombard import IciciLombardPolicyParser


def get_policy_parser(input_file, generate_txt_file=None):
    pdf_reader = PdfReader(input_file)
    pdf_content = pdf_reader.read_file_pypdf()

    if re.search(r"Welcome\s*to\s*(the)?\s*SBI\s*General", pdf_content, flags=re.I):
        # print("SBI Policy")
        return SbiPolicyParser(pdf_content)
    elif re.search(
        r"THE\s*NEW\s*INDIA\s*ASSURANCE\s*CO.\s*LTD.\s*\(Government\s*of\s*India\s*Undertaking\)",
        pdf_content,
        flags=re.I,
    ):
        # print("New India Policy")
        return NewIndiaPolicyParser(pdf_content)
    elif re.search(r"Thank\s*you\s*for\s*choosing\s*ICICI\s*Lombard", pdf_content, flags=re.I) or re.search(
        r"We\s*value\s*your\s*relationship\s*with\s*ICICI\s*Lombard", pdf_content, flags=re.I
    ):
        # For icici policies, pdfminer works better in some scenarios, so re-read the file accordingly
        pdf_content += "\nBEGINPDFMINER\n" + pdf_reader.read_file_pdfminer()
        return IciciLombardPolicyParser(pdf_content)
    else:
        # print("Unidentified Policy")
        return BasePolicyParser(pdf_content)
