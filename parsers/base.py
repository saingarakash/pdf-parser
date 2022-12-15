
class Insurers:
    SBI = "SBI"
    NEW_INDIA = "New India"
    ICICI_LOMBARD = "ICICI Lombard"
    NOT_AVAILABLE = "NOT_AVAILABLE"


class BasePolicyParser(object):
    def __init__(self, content, *args, **kwargs):
        self.content = content

    def get_insurer(self):
        return Insurers.NOT_AVAILABLE

    def get_customer_name(self):
        pass

    def get_address(self):
        pass

    def get_city(self):
        pass

    def get_state(self):
        pass

    def get_mobile_no(self):
        pass

    def get_reg_no(self):
        pass

    def get_make(self):
        pass

    def get_model(self):
        pass

    def get_variant(self):
        pass

    def get_year_of_manufacture(self):
        pass

    def get_ncb(self):
        pass

    def get_start_date(self):
        pass

    def get_end_date(self):
        pass

    def get_policy_type(self):
        pass

    def get_policy_number(self):
        pass

    def get_sum_insured(self):
        pass

    def get_basic_od_premium(self):
        pass

    def get_od_premium(self):
        pass

    def get_tp_premium(self):
        pass

    def get_taxes(self):
        pass

    def get_tax_rate(self):
        pass

    def get_net_premium(self):
        pass

    def get_total_premium(self):
        pass

    def get_posp_identifier(self):
        pass

    def get_receipt_number(self):
        pass

    def get_receipt_date(self):
        pass

    def get_policy_issue_date(self):
        pass

    def get_payment_mode(self):
        pass

    def get_payment_amount(self):
        pass

    def get_insurer_branch(self):
        pass

    def get_customer_type(self):
        pass
    
    def get_body_type(self):
        pass