import re

from parsers.regex_parser import RegexPolicyParser
from parsers.base import Insurers


class SbiPolicyParser(RegexPolicyParser):
    class RE(RegexPolicyParser.RE):
        CUST_NAME_PATTERNS = [
            re.compile(r"Insured Name\s*:\s*([\w\.\d \t]+)"),  # Policy Details Table
            re.compile(r"Details of Policy Holder:\s*Name:\s*(\w[\w\.\d \t]+)"),
            re.compile(
                r"^[\w\d\w]*Insured Name\s*([\w\.\d \t]+?)NCB", flags=re.M | re.I
            ),  # From NCB Verification section
            re.compile(r"Policy\s*Holder\s*Name[\s:\.]*([\w\.\d \t]+)"),
        ]

        ADDRESS_PATTERNS = [
            re.compile(r"Address\s*:\s*(.+?)Customer Contact", flags=re.M | re.I | re.DOTALL),
            re.compile(
                r"Details\s*of\s*Policy\s*Holder.+Address\s*:\s*(.+?)Policy\s*Holder\s*State",
                flags=re.M | re.I | re.DOTALL,
            ),
            re.compile(r"Proposer\s*Address[:\s]*(.+?)Proposer Contact Number", flags=re.M | re.I | re.DOTALL),
        ]

        CITY_PATTERNS = [
            re.compile(r"RTO\s*Location\s*Name\s*(\w+)Insured", flags=re.I),
            re.compile(r"RTO\s*Location\s*Name\s*(\w+)"),
            re.compile(r"RTO\s*Location\s+(\w+)"),
        ]

        STATE_PATTERNS = [
            re.compile(r"Policy\s*Holder\s*State([\s\w]+)Place", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Policy\s*Holder\s*State([\s\w]+)GSTIN", flags=re.M | re.I | re.DOTALL),
        ]

        MOBILE_PATTERNS = [
            re.compile(r"Contact\s*Details\s*:?\s*(?:\+91)?(?:-)?(\d+)", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Proposer\s*Contact\s*Number\s*:?\s*(?:\+91)?(?:-)?(\d+)", flags=re.M | re.I | re.DOTALL)
        ]

        REG_NO_PATTERNS = [
            re.compile(
                r"Registration\s*Number[\s:]*(NEW)",
                flags=re.M | re.I | re.DOTALL,
            ),
            re.compile(
                r"Registration\s*Number[\s:]*([A-Z]{2}[- ]?[0-9]{1,2}[- ]?[A-Z]+[- ]?[0-9]{1,4})",
                flags=re.M | re.I | re.DOTALL,
            ),
            re.compile(
                r"Registration\s*Number[\s:]*([A-Z]{2}[ -]?[0-9]{1,2}[- ]?[0-9]{1,4})",
                flags=re.M | re.I | re.DOTALL,
            ),
            # Special state patterns
            # DL-9S-AB-1234
            re.compile(
                r"Registration\s*Number[\s:]*(DL[- ]?[A-Z0-9]{1,2}[- ]?[A-Z]+[- ]?[0-9]{1,4})",
                flags=re.M | re.I | re.DOTALL,
            ),
        ]

        MAKE_PATTERNS = [
            re.compile(r"^Make of vehicle([ \w\&]+)$", flags=re.M | re.I),
            re.compile(r"Make of vehicle([\s\w\&]+?)Model", flags=re.M | re.I),
            re.compile(r"^Make([\s\w\&]+)Vehicle", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Make ?\& ?Model\s*([ \w\&]+)[, ]+[ \d\w\.\-\*]+?\s*Trailer", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Make([\s\w\.\&]+?)Model", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Make([\s\w\&]+?)Trailer", flags=re.M | re.I | re.DOTALL),
            re.compile(r"^Make([\s\w\&]+)$", flags=re.M | re.I | re.DOTALL),
            re.compile(r"^Vehicle\s*Make\s*([\s\w\&]+?)$", flags=re.M | re.I),
        ]

        MODEL_PATTERNS = [
            re.compile(r"Model *\& *Variant\s*([ \d\w]+)\&+[ \d\w\.\-\*]+$", flags=re.M | re.I),
            re.compile(r"Model *\& *Variant\s*([ \d\w]+)-+[ \d\w\.\-\*]+\s*(Year|Trailer)", flags=re.M | re.I),
            re.compile(r"Model *\& *Variant\s*([ \d\w\.\-\*]+)\s*(Year|Trailer)", flags=re.M | re.I),
            re.compile(r"Make ?\& ?Model\s*[ \w\&]+[, ]+([\s\d\w\.\-\*]+?)\s*Trailer", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Model([\s\d\w]+)Vehicle\s*Variant", flags=re.M | re.I),
            re.compile(r"Model([\s\d\w]+)Variant", flags=re.M | re.I),
            re.compile(r"Model *([ \d\w]+)", flags=re.M | re.I),
        ]

        VARIANT_PATTERNS = [
            re.compile(r"^Vehicle\s*Variant\s*([ \d\w\.\-]+)$", flags=re.M | re.I),
            re.compile(r"Model *\& *Variant[ \d\w]+\&+([ \d\w\.\-\*]+)$", flags=re.M | re.I),
            re.compile(r"Model *\& *Variant\s*[ \d\w]+-+([ \d\w\.\-\*]+)\s*(Year|Trailer)", flags=re.M | re.I),
            re.compile(r"Model *\& *Variant\s*([ \d\w\.\-\*]+)\s*(Year|Trailer)", flags=re.M | re.I),
            re.compile(r"Variant([\s\d\w\.\-\*]+?)Year", flags=re.M | re.I),
            re.compile(r"Variant *([ \d\w\.\-]+)", flags=re.M | re.I),
        ]

        YOM_PATTERNS = [
            re.compile(r"Year\s*of\s*Manufacture\s*(\d+)", flags=re.M | re.I),
            re.compile(r"Year\s*of\s*Manufacturing\s*(\d+)", flags=re.M | re.I),
        ]

        NCB_PATTERNS = [
            re.compile(r"No\s*Claims?\s*Bonus[:\s%]*([\.\d]+)\s*\%", flags=re.M | re.I),
            re.compile(r"No\s*Claims?\s*Bonus\s*\(NCB\)[:\s]*([\.\d]+)\%", flags=re.M | re.I),
        ]

        START_DATE_PATTERNS = [
            re.compile(r"Period\s*of\s*Insurance[\s:]*From[:\s]+([\d\/]+)00:00\s*Hours\s*", flags=re.M | re.I),
            re.compile(r"Period\s*of\s*Insurance[\s:]*From[:\s]+([\d\/]+)\s*", flags=re.M | re.I),
            re.compile(r"Period\s*of\s*Insurance\s*for\s*Own\s*Damage\s*Cover[\s:]*From[:\s]*([\d\/]+)\s*", flags=re.M | re.I),
            re.compile(r"Period\s*of\s*Insurance\s*OD[\s:]*From[:\s]+([\d\/]+)\s*", flags=re.M | re.I),
            re.compile(r"(?<!Previous )(?<!Active )(?<!Active Liability Only )Policy\s*Start\s*Date[:\s]+([\d\/]+)\s*", flags=re.M | re.I),
        ]

        END_DATE_PATTERNS = [
            re.compile(
                r"Period\s*of\s*Insurance[\s:]*From[:\s]*[T\s\(\)\d\/:]+\s*(?:hrs)?\s*to[:\s]*([\d\/]+)",
                flags=re.M | re.I,
            ),
            re.compile(
                r"Period\s*of\s*Insurance\s*OD[\s:]*From[:\s]*[T\s\(\)\d\/:]+\s*(?:hrs)?\s*to[:\s]*([\d\/]+)",
                flags=re.M | re.I,
            ),
            re.compile(
                r"Period\s*of\s*Insurance\s*for\s*Own\s*Damage\s*Cover[\s:]*From[:\s]*[T\s\(\)\d\/:]+\s*(?:hrs)?\s*to[:\s]*([\d\/]+)",
                flags=re.M | re.I,
            ),
            re.compile(
                r"Period\s*of\s*Insurance[\s:]*From[:\s]*[T\s\(\)\d\/:]+\s*(?:hours)?\s*to\s*midnight\s*of[:\s]*([\d\/]+)",
                flags=re.M | re.I,
            ),
            re.compile(r"(?<!Previous )(?<!Active )(?<!Active Liability Only )Policy\s*End\s*Date[:\s]+([\d\/]+)\s*", flags=re.M | re.I),
        ]

        POLICY_NUM_PATTERNS = [
            re.compile(r"(?<!Previous )(?<!Active )(?<!Active Liability )Policy\s*Number[:\s]*([\d\w]+)", flags=re.M | re.I),
            re.compile(r"Policy\s*No[\.: ]*([\d\w]{1,18})", flags=re.M | re.I),
            re.compile(r"Policy\s*Number[:\s]*([\d\w]+)", flags=re.M | re.I),
        ]

        SI_PATTERNS = [
            re.compile(r"IDV[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Insured Declared Value[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(
                r"Total IDV[\s:]*[\d\.,]+ +[\d\.,]+ +[\d\.,]+ +[\d\.,]+ +[\d\.,]+ +([\d\.,]+)",
                flags=re.M | re.I,
            ),  # GCV
            re.compile(r"Total IDV[\s:]+[\d\.,]+ +[\d\.,]+ +[\d\.,]+ +[\d\.,]+ +([\d\.,]+)", flags=re.M | re.I),  # GCV
        ]

        OD_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Own\s*Damage\s*Premium\s*(?:\(\w\))?[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Total\s*Own\s*Damage\s*(?:\(\w\))?[\s:]+([\d\.,]+)", flags=re.M | re.I),
        ]

        TP_PREMIUM_PATTERNS = [
            re.compile(
                r"Total\s*Third\s*Party\s*Liability\s*Premium\s*(?:\(\w\))?[\s:]+([\d\.,]+)",
                flags=re.M | re.I,
            ),
            re.compile(r"Total\s*Liability\s*Premium\s*(?:\(\w\))?[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Total\s*Third\s*Party\s*(?:\(\w\))?[\s:]+([\d\.,]+)", flags=re.M | re.I),
        ]

        TOTAL_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Premium\s*Collected\s*[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Policy\s*premium\s*including\s*Tax[\s:]+([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Final\s*Premium[\s:]+([\d\.,]+)", flags=re.M | re.I),
        ]

        TAXES_PATTERNS = [
            re.compile(r"Taxes\s*as\s*applicable[\s:]*([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"GST\s*Taxes[\s:]*([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"^Tax[\s:]*([\d\.,]+)", flags=re.M | re.I),
            re.compile(r"Taxes\s*Applicable[\s:]*([\d\.,]+)", flags=re.M | re.I),
        ]

        POS_IDENTIFIER_PATTERNS = [re.compile(r"POSP\s*Agent\s*Pan/Aadhar\s*Card\s*:\s*([\d\w]+)", flags=re.M | re.I)]

        RECEIPT_NUMBER_PATTERNS = [
            re.compile(r"Receipt\s*No[\.\s:]+([\d\w]+)", flags=re.M | re.I),
            re.compile(r"Receipt\s*Number[\.\s:]+([\d\w]+)", flags=re.M | re.I)
        ]

        RECEIPT_DATE_PATTERNS = [re.compile(r"Receipt\s*Date[:\s]*([\d\/]+)", flags=re.M | re.I)]

        PAYMENT_MODE_PATTERNS = [
            re.compile(
                r"Received\s*with\s*thanks\s*from[\w\s]+an\s*amount\s*of\s*Rs\.?\s*\d+\s*(?:\([\w\s\-\.]+\))?\s*by\s*(EFT|ONLINE|INTERNETBANKING)",
                flags=re.M | re.I,
            )
        ]

        PAYMENT_AMOUNT_PATTERNS = [
            re.compile(r"Received\s*with\s*thanks\s*from[\w\s]+an\s*amount\s*of\s*Rs\.?\s*(\d+)", flags=re.M | re.I)
        ]

        INSURER_BRANCH_PATTERNS = [
            re.compile(r"Policy\s*Issuing\s*Office[\s:]*(.+?)Policy", flags=re.DOTALL | re.I),
            re.compile(r"Policy\s*Servicing\s*Branch[\s:]*(.+?)$", flags=re.M | re.I)
        ]

    def get_insurer(self):
        return Insurers.SBI

    def get_policy_type(self):
        # Two Wheeler
        if re.search(r"Two[\s\-]*Wheeler\s*Insurance\s*Policy\s*-\s*Package", self.content, flags=re.I | re.M):
            return "Motor Two Wheeler Policy"
        elif re.search(r"BUNDLED\s*TWO[- ]WHEELER\s*INSURANCE\s*POLICY", self.content, flags=re.I | re.M):
            return "Motor Two Wheeler Policy"
        elif re.search(r"Stand-Alone Motor\s*(own)?\s*Damage Cover for Two[\s\-]*Wheeler", self.content, flags=re.I | re.M):
            # return "Motor Two Wheeler Standalone OD Policy"
            return "Motor Two Wheeler Policy"
        elif re.search(r"TWO[\s\-]*WHEELER\s*LIABILITY\s*ONLY\s*POLICY", self.content, flags=re.I | re.M):
            # return "Motor Two Wheeler Liability Policy"
            return "Motor Two Wheeler Policy"
        elif re.search(r"Act\s*Only\s*Insurance\s*Policy", self.content, flags=re.M) and "POPM2W" in self.get_policy_number():
            # return "Motor Two Wheeler Liability Policy"
            return "Motor Two Wheeler Policy"

        # Private Car
        elif re.search(r"Private\s*Car\s*Insurance\s*Policy\s*-\s*Package", self.content, flags=re.I | re.M):
            return "Motor Private Car Package Policy"
        elif re.search(r"Act\s*Only\s*Insurance\s*Policy", self.content, flags=re.I | re.M) and "POPMCAR" in self.get_policy_number():
            return "Motor Liability Policy"
        elif re.search(r"Stand-Alone Motor own Damage Cover for Private Car", self.content, flags=re.I | re.M):
            # return "Motor Private Car Standalone OD Policy"
            return "Motor Standalone OD Policy"
        elif re.search(r"PRIVATE\s*CAR\s*PACKAGE\s*POLICY", self.content, flags=re.I | re.M):
            return "Motor Private Car Package Policy"
        elif re.search(r"Private\s*Motor\s*4\s*wheeler", self.content, flags=re.I | re.M):
            return "Motor Private Car Package Policy"

        # GCV
        elif re.search(r"COMMERCIAL GOODS CARRYING", self.content, flags=re.I | re.M):
            return "Motor GCV Policy"
        elif re.search(r"Commercial Motor Miscellaneous Vehicles", self.content, flags=re.I | re.M):
            return "Motor Misc Policy"

        # PCV
        elif re.search(r"Commercial Motor Passenger Carrying", self.content, flags=re.I | re.M):
            return "Motor PCV Policy"

    def get_net_premium(self):
        try:
            return str(int(self.get_total_premium()) - int(self.get_taxes()))
        except Exception:
            return ""

    def get_receipt_number(self):
        value = super().get_receipt_number()
        if value and value.strip().lower() in ("reference", "receipt"):
            return ""
        return value

    def get_policy_issue_date(self):
        return self.get_receipt_date()
