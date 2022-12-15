from parsers.base import BasePolicyParser

STATE_MAPPING = {
    "AN": "Andaman and Nicobar",
    "AP": "Andhra Pradesh",
    "AR": "Arunachal Pradesh",
    "AS": "Assam",
    "BR": "Bihar",
    "CH": "Chandigarh",
    "DN": "Dadra and Nagar Haveli",
    "DD": "Daman and Diu",
    "DL": "Delhi",
    "GA": "Goa",
    "GJ": "Gujarat",
    "HR": "Haryana",
    "HP": "Himachal Pradesh",
    "JK": "Jammu and Kashmir",
    "JH": "Jharkhand",
    "KA": "Karnataka",
    "KL": "Kerala",
    "LD": "Lakshadweep",
    "MP": "Madhya Pradesh",
    "MH": "Maharashtra",
    "MN": "Manipur",
    "ML": "Meghalaya",
    "MZ": "Mizoram",
    "NL": "Nagaland",
    "OR": "Orissa",
    "OD": "Odisha",
    "PY": "Pondicherry",
    "PN": "Punjab",
    "RJ": "Rajasthan",
    "SK": "Sikkim",
    "TN": "Tamil Nadu",
    "TR": "Tripura",
    "UP": "Uttar Pradesh",
    "WB": "West Bengal",
}


class RegexPolicyParser(BasePolicyParser):
    class RE:
        CUST_NAME_PATTERNS = []

        ADDRESS_PATTERNS = []

        CITY_PATTERNS = []

        STATE_PATTERNS = []

        MOBILE_PATTERNS = []

        REG_NO_PATTERNS = []

        MAKE_PATTERNS = []

        MODEL_PATTERNS = []

        VARIANT_PATTERNS = []

        YOM_PATTERNS = []

        NCB_PATTERNS = []

        START_DATE_PATTERNS = []

        END_DATE_PATTERNS = []

        POLICY_NUM_PATTERNS = []

        POLICY_TYPE_PATTERNS = []

        SI_PATTERNS = []

        BASIC_OD_PREMIUM_PATTERNS = []

        OD_PREMIUM_PATTERNS = []

        TP_PREMIUM_PATTERNS = []

        NET_PREMIUM_PATTERNS = []

        TOTAL_PREMIUM_PATTERNS = []

        TAXES_PATTERNS = []

        TAX_RATE_PATTERNS = []

        POS_IDENTIFIER_PATTERNS = []

        RECEIPT_NUMBER_PATTERNS = []

        RECEIPT_DATE_PATTERNS = []

        POLICY_ISSUE_DATE_PATTERNS = []

        PAYMENT_MODE_PATTERNS = []

        PAYMENT_AMOUNT_PATTERNS = []

        INSURER_BRANCH_PATTERNS = []

        CUSTOMER_TYPE_PATTERNS = []

        BODY_TYPE_PATTERNS = []

    def __init__(self, *args, **kwargs):
        # Define internal cache
        self._cache = {}
        return super().__init__(*args, **kwargs)

    def extract_information(self, pattern_list, cache_key=None, debug=False):
        if cache_key and self._cache.setdefault(cache_key):
            return self._cache[cache_key]

        value = ""
        match = None
        for pattern in pattern_list:
            match = pattern.search(self.content)
            if match:
                found_match = match.group(1).strip()
                if found_match:
                    value = found_match
                    if debug:
                        print(f"Value: {value}")
                        print(f"Matched {match.groups()} against pattern: {pattern.pattern}")
                    break
            else:
                if debug:
                    print(f"No Match. {pattern.pattern}")

        if cache_key:
            self._cache[cache_key] = value
        return value

    def get_customer_name(self):
        return self.extract_information(self.RE.CUST_NAME_PATTERNS)

    def get_address(self):
        return self.extract_information(self.RE.ADDRESS_PATTERNS)

    def get_city(self):
        return self.extract_information(self.RE.CITY_PATTERNS)

    def get_state(self):
        if not self._cache.setdefault("state", ""):
            # Extract from policy content
            self._cache["state"] = self.extract_information(self.RE.STATE_PATTERNS)

        if not self._cache["state"]:
            # Extract from registration number
            reg_state_chars = self.get_reg_no()[0:2]
            self._cache["state"] = STATE_MAPPING.get(reg_state_chars, "")
        return self._cache["state"]

    def get_mobile_no(self):
        return self.extract_information(self.RE.MOBILE_PATTERNS, "mobile_number")

    def get_reg_no(self):
        return self.extract_information(self.RE.REG_NO_PATTERNS, "registration_number")

    def get_make(self):
        return self.extract_information(self.RE.MAKE_PATTERNS, "make")

    def get_model(self):
        return self.extract_information(self.RE.MODEL_PATTERNS)

    def get_variant(self):
        return self.extract_information(self.RE.VARIANT_PATTERNS)

    def get_year_of_manufacture(self):
        return self.extract_information(self.RE.YOM_PATTERNS, "year_of_manufacture")

    def get_ncb(self):
        ncb = self.extract_information(self.RE.NCB_PATTERNS)
        if ncb:
            return str(int(float(ncb)))

    def get_start_date(self):
        return self.extract_information(self.RE.START_DATE_PATTERNS)

    def get_end_date(self):
        return self.extract_information(self.RE.END_DATE_PATTERNS)

    def get_policy_type(self):
        return self.extract_information(self.RE.POLICY_TYPE_PATTERNS)

    def get_policy_number(self):
        return self.extract_information(self.RE.POLICY_NUM_PATTERNS, "policy_number")

    def get_sum_insured(self):
        sum_insured = self.extract_information(self.RE.SI_PATTERNS)
        if sum_insured:
            sum_insured = sum_insured.replace(",", "")
            return str(int(float(sum_insured)))

    def get_basic_od_premium(self):
        value = self.extract_information(self.RE.BASIC_OD_PREMIUM_PATTERNS)
        if value:
            value = value.replace(",", "")
            return str(int(float(value)))

    def get_od_premium(self):
        value = self.extract_information(self.RE.OD_PREMIUM_PATTERNS)
        if value:
            value = value.replace(",", "")
            return str(int(float(value)))

    def get_tp_premium(self):
        value = self.extract_information(self.RE.TP_PREMIUM_PATTERNS)
        if value:
            value = value.replace(",", "")
            return str(int(float(value)))

    def get_taxes(self):
        if not self._cache.setdefault("taxes", ""):
            value = self.extract_information(self.RE.TAXES_PATTERNS)
            if value:
                value = value.replace(",", "")
                self._cache["taxes"] = str(int(float(value)))
        return self._cache["taxes"]

    def get_tax_rate(self):
        value = self.extract_information(self.RE.TAX_RATE_PATTERNS)
        return value or "18"

    def get_net_premium(self):
        if not self._cache.setdefault("net_premium", ""):
            value = self.extract_information(self.RE.NET_PREMIUM_PATTERNS)
            if value:
                value = value.replace(",", "")
                self._cache["net_premium"] = str(int(float(value)))
        return self._cache["net_premium"]

    def get_total_premium(self):
        if not self._cache.setdefault("total_premium", ""):
            value = self.extract_information(self.RE.TOTAL_PREMIUM_PATTERNS)
            if value:
                value = value.replace(",", "")
                self._cache["total_premium"] = str(int(float(value)))
        return self._cache["total_premium"]

    def get_posp_identifier(self):
        return self.extract_information(self.RE.POS_IDENTIFIER_PATTERNS, "pos_identifier")

    def get_receipt_number(self):
        return self.extract_information(self.RE.RECEIPT_NUMBER_PATTERNS)

    def get_receipt_date(self):
        return self.extract_information(self.RE.RECEIPT_DATE_PATTERNS, "receipt_date")

    def get_policy_issue_date(self):
        return self.extract_information(self.RE.POLICY_ISSUE_DATE_PATTERNS)

    def get_payment_mode(self):
        return self.extract_information(self.RE.PAYMENT_MODE_PATTERNS)

    def get_payment_amount(self):
        return self.extract_information(self.RE.PAYMENT_AMOUNT_PATTERNS)

    def get_insurer_branch(self):
        return self.extract_information(self.RE.INSURER_BRANCH_PATTERNS)

    def get_customer_type(self):
        if self._cache.get("customer_type", None):
            return self._cache["customer_type"]

        value = self.extract_information(self.RE.CUSTOMER_TYPE_PATTERNS, "customer_type")
        if value:
            return value

        self._cache["customer_type"] = "individual"
        customer_name = self.get_customer_name().lower()
        if "m/s" in customer_name or "llp" in customer_name or "ltd" in customer_name:
            self._cache["customer_type"] = "corporate"
        return self._cache["customer_type"]

    def get_body_type(self):
        return self.extract_information(self.RE.BODY_TYPE_PATTERNS)
