import re

from parsers.regex_parser import RegexPolicyParser
from parsers.base import Insurers


class IciciLombardPolicyParser(RegexPolicyParser):
    # Ensure that PDFMINER regexs always come first, since they have to be more restrictive
    class RE(RegexPolicyParser.RE):
        CUST_NAME_PATTERNS = [
            re.compile(r"Insured\s*Name[\s :]*([\w\.\/\d \t]+?)Policy"),
            re.compile(r"Name\s*Of\s*the\s*Insured[\s :]*([\w\.\/\d \t]+?)Policy"),
            re.compile(r"Dear\s*([\w\.\/\d \t]+),"),
        ]

        ADDRESS_PATTERNS = [
            re.compile(r"Address\s*Partner\s*Code\s*(.+?)CB69117", flags=re.M | re.I | re.DOTALL),
            # re.compile(r"BEGINPDFMINER.*(?<!Branch )(?<!Email )Address\s*(?!:Telephone)?\s*(.+?)(?:Policy|Mobile)", flags=re.M | re.I | re.DOTALL),
            re.compile(r"(?<!Branch )(?<!Email )Address\s*:\s*(.+?)(?:Tenure|Period)", flags=re.M | re.I | re.DOTALL),
            re.compile(r"(?<!Branch )(?<!Email )Address\s*(.+?)(?:Policy)", flags=re.M | re.I | re.DOTALL),
        ]

        CITY_PATTERNS = [
            re.compile(r"RTO\s*Location[:\s]*[\w ]+-([\w ]+)", flags=re.M | re.I)
        ]

        STATE_PATTERNS = [
            re.compile(r"RTO\s*Location[:\s]*([\w ]+)-", flags=re.M | re.I)
        ]

        MOBILE_PATTERNS = [
            re.compile(r"Mobile\s*No[\s:]*([\d]+)", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Mobile\s*Number[\s:]*([\d]+)", flags=re.M | re.I | re.DOTALL),
        ]

        REG_NO_PATTERNS = [
            re.compile(
                r"Registration\s*(?:No|Number)[\.\s:]*(NEW|[A-Z]{2}[- ]?[0-9]{1,2}[- ]?[A-Z]+[- ]?[0-9]{1,4}|[A-Z]{2}[ -]?[A-Z0-9]{1,2}[- ]?[0-9]{1,4})",
                flags=re.M | re.I | re.DOTALL,
            ),
        ]

        MAKE_PATTERNS = [
            re.compile(r"Make\s*([ \w\&]+)\s*Trailer", flags=re.M | re.I | re.DOTALL),
        ]

        MODEL_PATTERNS = [
            re.compile(r"Model\s*([ \d\w\.\-\*\(\)/\+]+)\s*Non", flags=re.M | re.I | re.DOTALL),
        ]

        VARIANT_PATTERNS = [
        ]

        BODY_TYPE_PATTERNS = [
            re.compile(r"Type\s*of\s*Body\s*(\w+)\s*Mfg\s*Yr", flags=re.M | re.I),

        ]

        YOM_PATTERNS = [
            re.compile(r"(?:Open|Closed|Pillion|Hatchback|Saloon|Sedan)\s*\d+\s*(\d+)", flags=re.M | re.I),
        ]

        NCB_PATTERNS = [
            re.compile(r"No\s*Claims?\s*Bonus[:\s]*([\.\d]+)\s*\%", flags=re.M | re.I),
        ]

        POLICY_ISSUE_DATE_PATTERNS = [
            re.compile(r"Policy\s*Issued\s*On\s*: *([ ,\w\d]+)", flags=re.M | re.I),
        ]

        START_DATE_PATTERNS = [
            re.compile(r"(\w+ *\d+, *\d+)\s*[:\d]+\s*to\s*midnight\s*of", flags=re.M | re.I),
        ]

        END_DATE_PATTERNS = [
            re.compile(r"to\s*midnight\s*of\s*([ ,\w\d]+)", flags=re.M | re.I),
        ]

        POLICY_NUM_PATTERNS = [
            re.compile(r"Enclosed\s*Policy\s*No[\.:\s]*([\d\w/]+)", flags=re.M | re.I),
        ]

        SI_PATTERNS = [
            re.compile(r"Total\s*IDV *\(`\)\s*([\d\.,]+)", flags=re.M | re.I | re.DOTALL),
            re.compile(r"Total\s*IDV\s*.+?([\d\.,]+)\s*Premium\s*Details", flags=re.M | re.I | re.DOTALL),
        ]

        OD_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Own\s*Damage\s*Premium\s*\([\w\+]+\)[:\s]*([\d\.,]+)", flags=re.M | re.I),
        ]

        TP_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Liability\s*Premium\s*(?:\([\w\+]+\))?[:\s]*([\d\.,]+)", flags=re.M | re.I),
        ]

        NET_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Package\s*Premium\s*\([\w\+]+\)[:\s]*([\d\.,]+)", flags=re.M | re.I),
        ]

        TOTAL_PREMIUM_PATTERNS = [
            re.compile(r"Total\s*Premium\s*Payable(?:\s*in\s*`\s*)?[:\s]*([\d\.,]+)", flags=re.M | re.I),
        ]

        TAXES_PATTERNS = [
            re.compile(r"Total\s*Tax\s*Payable\s*in\s*`[:\s]*([\d\.,]+)", flags=re.M | re.I),
        ]

        INSURER_BRANCH_PATTERNS = [
            re.compile(r"Policy\s*Issuing\s*Office\s*:\s*(.+?)(Warranted|Product|Agent)", flags=re.DOTALL | re.I)
        ]

        POS_IDENTIFIER_PATTERNS = []

        RECEIPT_NUMBER_PATTERNS = [re.compile(r"Premium\s*Collection\s*No[\.\s:]+(\d+)", flags=re.M | re.I)]

        RECEIPT_DATE_PATTERNS = [
            re.compile(r"Receipt\s*Date *([- ,\w\d]+)", flags=re.M | re.I),
        ]

        PAYMENT_MODE_PATTERNS = []

        PAYMENT_AMOUNT_PATTERNS = [
            re.compile(r"Premium\s*Amount[`:\s]*([\d\.,]+)Receipt", flags=re.M | re.I),
        ]

    def get_insurer(self):
        return Insurers.ICICI_LOMBARD

    def get_policy_type(self):
        # Two Wheeler
        if re.search(r"Two\s*Wheeler\s*Vehicles[\w\s]*Policy", self.content, flags=re.I):
            return "Motor Two Wheeler Policy"
        elif re.search(r"Two\s*wheeler\s*Insurance\s*Policy", self.content, flags=re.I):
            return "Motor Two Wheeler Policy"

        # Private Car
        elif re.search(r"Private\s*Car\s*Package\s*Policy", self.content, flags=re.I):
            return "Motor Private Car Package Policy"
        elif re.search(r"Private\s*Car\s*Liability\s*Policy", self.content, flags=re.I):
            return "Motor Liability Policy"
        elif re.search(r"Stand-Alone\s*Own\s*Damage\s*Private\s*Car\s*Insurance\s*Policy", self.content):
            return "Motor Standalone OD Policy"

        # GCV
        elif re.search(r"Goods\s*Carrying\s*Vehicles[\w\s]*Policy", self.content, flags=re.I):
            return "Motor GCV Policy"
        elif re.search(r"Miscellaneous\s*Vehicles[\w\s]*Policy", self.content, flags=re.I):
            return "Motor Misc Policy"

        # PCV
        elif re.search(r"Passenger\s*Carrying\s*Vehicles[\w\s]*Policy", self.content, flags=re.I):
            return "Motor PCV Policy"

    def get_rto_location(self):
        rto_location_pattern = [re.compile(r"RTO\s*Location\s*:([\-\w ]+)", flags=re.M | re.I)]
        return self.extract_information(rto_location_pattern, "rto_location")

    def get_reg_no(self):
        value = super().get_reg_no()
        if value:
            return value

        rto_location = self.get_rto_location()
        if not rto_location:
            return ""

        reg_no_pattern = re.compile(
            rto_location
            + r"\s*(NEW|[A-Z]{2}[- ]?[0-9]{1,2}[- ]?[A-Z]+[- ]?[0-9]{1,4}|[A-Z]{2}[ -]?[A-Z0-9]{1,2}[- ]?[0-9]{1,4})",
            flags=re.M | re.I,
        )
        return self.extract_information([reg_no_pattern], "registration_number")

    def get_make(self):
        value = super().get_make()
        if value:
            return value

        rto_location = self.get_rto_location()
        if not rto_location:
            return ""

        secondary_pattern = re.compile(rf"^([\w\&\d\. ]+)/[\w\&\d\. \/]+\s*{rto_location}", flags=re.M | re.I)
        return self.extract_information([secondary_pattern], "make")

    def get_model(self):
        value = super().get_model()
        if value:
            return value

        rto_location = self.get_rto_location()
        if not rto_location:
            return ""

        secondary_pattern = re.compile(rf"/([\w\&\d\. \/]+)\s*{rto_location}", flags=re.M | re.I)
        return self.extract_information([secondary_pattern], "model")

    def get_net_premium(self):
        value = super().get_net_premium()
        if value:
            return value

        # Use Total Premium - Taxes as fallback for net premium calculation
        try:
            return str(int(self.get_total_premium()) - int(self.get_taxes()))
        except Exception:
            return ""

    def get_taxes(self):
        value = super().get_taxes()
        if value:
            return value

        # Assume 18% as tax rate to calculate from total premium
        # Cannot rely on net premium, because net premium's fallback depends on taxes,
        # so there is a chance of infinte recursive loop if we use net_premium here
        try:
            total_premium = float(self.get_total_premium())
            net_premium = total_premium * 100 / (100 + float(self.get_tax_rate()))
            return str(round(total_premium - net_premium))
        except Exception:
            return ""
