import re

from parsers.regex_parser import RegexPolicyParser
from parsers.base import Insurers


class NewIndiaPolicyParser(RegexPolicyParser):
    class RE(RegexPolicyParser.RE):
        CUST_NAME_PATTERNS = [
            re.compile(r"Insured(?:'s)?\s*Name[\s:]+([\w\.\/\d \t]+)\s+Customer"),  # Policy Details Table
        ]

        ADDRESS_PATTERNS = [
            re.compile(r"Insured(?:'s)?\s*Address[:\s]*(.+?)Contact Number", flags=re.M | re.I | re.DOTALL),
        ]

        CITY_PATTERNS = [
            re.compile(r"Name\s*of\s*registration\s*authority[:\s]*([ \w]+)", flags=re.M | re.I)
        ]

        STATE_PATTERNS = [
        ]

        MOBILE_PATTERNS = [re.compile(r"Contact\s*Number[\s:\/]*([X\d]+)", flags=re.M | re.I | re.DOTALL)]

        REG_NO_PATTERNS = [
            re.compile(
                r"Registration\s*(?:No|Number)[\.\s:]*(NEW)",
                flags=re.M | re.I | re.DOTALL,
            ),
            re.compile(
                r"Registration\s*(?:No|Number)[\.\s:]*([A-Z]{2}[- ]?[0-9]{1,2}[- ]?[A-Z]+[- ]?[0-9]{1,4})",
                flags=re.M | re.I | re.DOTALL,
            ),
            re.compile(
                r"Registration\s*(?:No|Number)[\.\s:]*([A-Z]{2}[ -]?[A-Z0-9]{1,2}[- ]?[0-9]{1,4})",
                flags=re.M | re.I | re.DOTALL,
            ),
        ]

        MAKE_PATTERNS = [
            re.compile(r"Make\s*/\s*Model[\s:]*([ \w\&]+)", flags=re.M | re.I | re.DOTALL),
        ]

        MODEL_PATTERNS = [
            re.compile(r"Make\s*/\s*Model[\s:]*[\s\w\&]+/\s*([ \d\w\.\-\*\(\)/\+]+)Variant", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Make\s*/\s*Model[\s:]*[\s\w\&]+/\s*([ \d\w\.\-\*\(\)/\+]+)Registration", flags=re.M | re.I | re.DOTALL),
        ]

        VARIANT_PATTERNS = [
            re.compile(r"Variant[\s:]*([ \d\w\.\-\+\(\)/]+)", flags=re.M | re.I),
        ]

        YOM_PATTERNS = [
            re.compile(r"Year of Manufacture[:\s]*(\d+)", flags=re.M | re.I),
        ]

        NCB_PATTERNS = [
        ]

        POLICY_ISSUE_DATE_PATTERNS = [
            re.compile(r"Date\s*of\s*Issue[\s:]*([\d\/]+)", flags=re.M | re.I),
        ]

        START_DATE_PATTERNS = [
            re.compile(r"Period\s+of\s+cover[\s:]*([\d\/]+)", flags=re.M | re.I),
        ]

        END_DATE_PATTERNS = [
            re.compile(
                r"Period\s*of\s*cover[\s:]*[\s\(\)\d\/:]*(?:PM|AM)?\s*to\s*([\d\/]+)",
                flags=re.M | re.I,
            ),
        ]

        POLICY_NUM_PATTERNS = [
            re.compile(r"Policy\s*Number[:\s]*([\d\w]+)", flags=re.M | re.I),
            re.compile(r"Policy\s*No[\.: ]*([\d\w]+)", flags=re.M | re.I),
        ]

        SI_PATTERNS = [
            re.compile(r"INSURED DECLARED VALUE[^0-9]+(?:[\d\.,]+\s+){5}([\d\.,]+)", flags=re.M | re.I | re.DOTALL),
            re.compile(r"For\s*individual\s*covers\s*\(OD\)\s*in\s*RS[:\s]*([\d\.\,]+)", flags=re.M | re.I),
        ]

        OD_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*OD\s*Premium[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Total\s*OD\s*Premium\s*\(Rs\)[\s:]+([\d\.,]+)", flags=re.M | re.I),
        ]

        TP_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*TP\s*Premium[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Total\s*TP\s*Premium\s*\(Rs\)[\s:]+([\d\.,]+)", flags=re.M | re.I),
        ]

        NET_PREMIUM_PATTERNS = [
            re.compile(r"Net\s*Premium\s*in\s*Rs[\s:]*([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Net\s*Premium\s*\(Rs\)[\s:]*([\d\.,]+)", flags=re.M | re.I),
        ]

        TOTAL_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Payable\s*in\s*Rs[\s:]*([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Total\s*Payable\s*\(Rs\)[\s:]*([\d\.,]+)", flags=re.M | re.I),
        ]

        TAXES_PATTERNS = [
            re.compile(r"GST\s*in\s*Rs[\s:]*([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"GST\s*\(Rs\)[\s:]*([\d\.,]+)", flags=re.M | re.I),
        ]

        INSURER_BRANCH_PATTERNS = [
            re.compile(r"POLICY\s*ISSUING\s*OFFICE\s*:\s*(.+?)Phone", flags=re.DOTALL | re.I),
        ]

        POS_IDENTIFIER_PATTERNS = []

        RECEIPT_NUMBER_PATTERNS = [
            re.compile(r"Receipt\s*Number[\.\s:]+([\s\d\w\-\/]+)Previous\s*Insurer", flags=re.M | re.I)
        ]

        RECEIPT_DATE_PATTERNS = []

        PAYMENT_MODE_PATTERNS = [

        ]

        PAYMENT_AMOUNT_PATTERNS = [
        ]

    def get_insurer(self):
        return Insurers.NEW_INDIA

    def get_policy_type(self):
        # Two Wheeler
        if re.search(r"Two\s*Wheeler\s*Package\s*Policy", self.content, flags=re.I):
            return "Motor Two Wheeler Policy"
        elif re.search(r"Two\s*Wheeler\s*Liability\s*Policy", self.content, flags=re.I):
            return "Motor Two Wheeler Policy"
        elif re.search(r"Two\s*Wheeler\s*Liability\s*Only\s*Policy", self.content, flags=re.I):
            return "Motor Two Wheeler Policy"

        # Private Car
        elif re.search(r"Private\s*Car\s*Package\s*Policy", self.content, flags=re.I):
            return "Motor Private Car Package Policy"
        elif re.search(r"Private\s*Car\s*Liability\s*Policy", self.content, flags=re.I):
            return "Motor Liability Policy"
        elif re.search(r"Private\s*Car\s*Liability\s*Only\s*Policy", self.content, flags=re.I):
            return "Motor Liability Policy"

        # GCV
        elif re.search(r"A\s*-\s*Goods\s*Carrying", self.content, flags=re.I):
            return "Motor GCV Policy"
        elif re.search(r"D\s*-\s*Misc\s*-\s*Special\s*Type", self.content, flags=re.I):
            return "Motor Misc Policy"

        # PCV
        elif re.search(r"C\s*-\s*Passenger\s*Carrying", self.content, flags=re.I):
            return "Motor PCV Policy"

    def get_receipt_number(self):
        value = super().get_receipt_number()
        if value and value.strip().lower() in ("reference", "receipt"):
            return ""
        return value
