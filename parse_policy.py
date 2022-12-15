#!/bin/env python3
import argparse
import csv
import glob
import os
import sys
from datetime import datetime
from pathlib import Path

from dateparser import parse as dt_parse
from thefuzz import fuzz, process
from writers.excel import ExcelDictWriter

from parsers import get_policy_parser
from parsers.base import BasePolicyParser, Insurers

SAIBA_INSURERS = {
    Insurers.SBI: "SBI General Insurance Company Limited",
    Insurers.NEW_INDIA: "The New India Assurance Company Limited",
    Insurers.ICICI_LOMBARD: "ICICI Lombard General Insurance Company Limited",
    Insurers.HDFC_ERGO: "HDFC ERGO General Insurance Company Limited",
    Insurers.DIGIT: "Go Digit General Insurance Limited",
    Insurers.ORIENTAL: "The Oriental Insurance Company Limited",
    Insurers.UNITED: "United India Insurance Company Limited",
    Insurers.NATIONAL: "National Insurance Company Limited",
    Insurers.RELIANCE: "Reliance General Insurance Company Limited",
    Insurers.ROYAL_SUNDARAM: "Royal Sundaram General Insurance Company Limited",
    Insurers.IFFCO_TOKIO: "IFFCO Tokio General Insurance Company Limited",
    Insurers.LIBERTY: "Liberty Videocon General Insurance Company Limited",
    Insurers.UNIVERSAL_SOMPO: "Universal Sompo General Insurance Company Limited",
    Insurers.NOT_AVAILABLE: "Not Available",
}

SAIBA_HEADERS = [
    "Sno",
    "BrokerBranchCode",
    "BrokerBranch",
    "AreaCode",
    "CustCode",
    "CustName",
    "ClientCode(ShortName)",
    "Address",
    "City",
    "State",
    "Country",
    "Pin",
    "PhoneNo",
    "MobileNo",
    "DOB",
    "Fax",
    "Email",
    "PANNo",
    "CustGroupSAIBA",
    "VerticalType",
    "OrgType",
    "BusinessType",
    "RMCodeSAIBA",
    "SolicitCode",
    "CSCCodeSAIBA",
    "TCCodeSAIBA",
    "Ref/POS/MISP",
    "Ref/POS/MISPCodeSAIBA",
    "InsurerSAIBA",
    "InsurerBranchAutoCodeSAIBA",
    "PolicyTypeSAIBA",
    "ProductName",
    "VehicleRegnStatus",
    "VehicleNo",
    "Make",
    "Model",
    "Variant",
    "DateRegistration",
    "InvoiceDate",
    "YearofMan",
    "ChasisNo",
    "EngineNo",
    "CC",
    "Fuel",
    "RTO",
    "NCB",
    "ODD",
    "PCV/GCV/Misc",
    "Passenger/GVW",
    "BusPropDate",
    "StartDate",
    "ExpiryDate",
    "CoverNoteNo",
    "CovernoteProposalDate",
    "ProposalSubmissionDate",
    "PolicyNo",
    "PolicyIssueDate",
    "PolicyReceiveDate",
    "PolRecvdFormat",
    "BrokerBizType",
    "InsurerBizType",
    "SumInsured",
    "ODNetPremium",
    "Tp/Terroisem Prem",
    "OwnerDriver(LPD)",
    "RoadsideAssistance(WithoutBrokerage)",
    "GST/TaxAmount",
    "StampDuty",
    "GrossPrem",
    "Mode",
    "TranAmt",
    "TranNo",
    "TranDated",
    "BankName",
    "CessRate",
    "BrokRate",
    "GST/TaxRate",
    "TPBrokRate",
    "OwnerDriver%",
    "RewardRate",
    "RewardTPRate",
    "RewardRateOn",
    "ExpRate",
    "TPExpRate",
    "RefRate",
    "RefTPRate",
    "POS/MISPRate",
    "TPPOS/MISPRate",
    "PayAt",
    "CSCRate",
    "PolicyStatus",
    "Remarks",
    "OldControlNo",
    "ReceiptNo",
    "RefNo",
    "CampaignName",
    "Source",
    "PolicyVertical",
    "IsRenewable",
    "TPABranch",
    "TPAPer",
    "PremiumReceiptDate",
    "PremiumReceiptNo",
    "PremiumRemittingDate",
    "PrevPolicy_no",
    "Insured/ProposerName",
    "NomineeDetails",
    "file",
]

ENABLED_INSURERS = [Insurers.SBI, Insurers.NEW_INDIA, Insurers.ICICI_LOMBARD, Insurers.HDFC_ERGO]

# ENABLED_INSURERS = [Insurers.DIGIT]

APPLICABLE_DATE_FORMATS = ["%d/%m/%Y", "%d-%m-%Y", "%d-%b-%Y", "%b %d, %Y", "%d %b, %Y"]


class Masters:
    _branch_master = {}

    @classmethod
    def read_branch_master(cls, master_file):
        with open(master_file) as csvfile:
            for row in csv.DictReader(csvfile):
                insurer_branches = cls._branch_master.setdefault(row["Insurer"].lower(), {})
                insurer_branches[row["Address"]] = row["BranchAutoCode"]
        return cls._branch_master

    @classmethod
    def get_branch_code(cls, insurer, branch):
        if not branch:
            return ""

        branches = cls._branch_master[insurer.lower()]

        # Find branch using fuzzy match
        found_branch, score = process.extractOne(
            branch, branches.keys(), scorer=fuzz.token_sort_ratio
        )

        # print(f"{score}, {branch}, {found_branch}")

        if score <= 15:
            return ""

        # Return branch code
        return branches[found_branch]


class PolicyParser(object):
    def __init__(self, date, files, txt_file_directory=None) -> None:
        self.processing_date = date
        self.input_files = files
        self.txt_file_directory = txt_file_directory

    def clean_text(self, text):
        if not text:
            return ""
        cleaned_text = " ".join(text.split()).replace("\n", " ").strip().upper()

        return f"{cleaned_text}"

    def format_date(self, datetime_str):
        cleaned_datetime_str = self.clean_text(datetime_str)
        if not cleaned_datetime_str:
            return cleaned_datetime_str

        try:
            return dt_parse(cleaned_datetime_str, date_formats=APPLICABLE_DATE_FORMATS).strftime(
                "%m/%d/%Y"
            )
        except Exception as e:
            print(f"Unable to parse date {cleaned_datetime_str}. {e}")
            return cleaned_datetime_str

    def format_mobile_no(self, number):
        cleaned_mobile_str = self.clean_text(number)

        if not cleaned_mobile_str or "X" in cleaned_mobile_str:
            return "8826294213"
        return cleaned_mobile_str

    def transform_to_saibaa(self, input: BasePolicyParser):
        return {
            # Extracted Values
            "CustName": self.clean_text(input.get_customer_name()).replace(".", " ").strip(),
            "Address": self.clean_text(input.get_address()),
            "MobileNo": self.format_mobile_no(input.get_mobile_no()),
            "City": self.clean_text(input.get_city()),
            "State": self.clean_text(input.get_state()),
            "Ref/POS/MISP": "POS" if input.get_posp_identifier() else "Ref",
            "InsurerSAIBA": SAIBA_INSURERS[input.get_insurer()],
            "PolicyTypeSAIBA": input.get_policy_type(),
            "VehicleNo": input.get_reg_no(),
            "Make": self.clean_text(input.get_make()),
            "Model": self.clean_text(input.get_model()),
            "Variant": self.clean_text(input.get_variant()),
            "YearofMan": self.clean_text(input.get_year_of_manufacture()),
            "NCB": self.clean_text(input.get_ncb()) or "0",
            "ODD": input.get_od_premium() or "0",
            "StartDate": self.format_date(input.get_start_date()),
            "ExpiryDate": self.format_date(input.get_end_date()),
            "PolicyNo": self.clean_text(input.get_policy_number()),
            "PolicyIssueDate": self.format_date(
                input.get_policy_issue_date() or input.get_receipt_date()
            ),
            "SumInsured": input.get_sum_insured() or "0",
            "ODNetPremium": input.get_od_premium() or "0",
            "Tp/Terroisem Prem": input.get_tp_premium() or "0",
            "GST/TaxAmount": input.get_taxes() or "0",
            "GrossPrem": input.get_total_premium(),
            "TranAmt": self.clean_text(input.get_net_premium()),
            "TranDated": self.format_date(
                input.get_receipt_date() or input.get_policy_issue_date()
            ),
            "GST/TaxRate": self.clean_text(input.get_tax_rate()),
            "ReceiptNo": self.clean_text(input.get_receipt_number()),
            "PremiumReceiptNo": self.clean_text(input.get_receipt_number()),
            "PremiumReceiptDate": self.format_date(
                input.get_receipt_date() or input.get_policy_issue_date()
            ),
            "InsurerBranchAutoCodeSAIBA": Masters.get_branch_code(
                SAIBA_INSURERS[input.get_insurer()], input.get_insurer_branch()
            ),
            "VerticalType": "Corporate" if input.get_customer_type() == "corporate" else "Retail",
            "BusinessType": "Business" if input.get_customer_type() == "corporate" else "Service",
            "OrgType": input.get_customer_type(),
            "PolicyReceiveDate": self.format_date(self.processing_date),
            "BusPropDate": self.format_date(self.processing_date),
            # Default Values
            # "Mode": self.clean_text(input.get_payment_mode()) or "Cash",
            "Mode": "Cash",
            "Country": "India",
            "BrokerBranchCode": "0",
            "BrokerBranch": "Head Office",
            "CustGroupSAIBA": "Other",
            "RMCodeSAIBA": "",  # To be entered manually
            "SolicitCode": "14",
            "CSCCodeSAIBA": "",  # User upload id, To be entered manually
            "TCCodeSAIBA": "0",
            "Ref/POS/MISPCodeSAIBA": "0",
            "VehicleRegnStatus": "N",
            "CoverNoteNo": "0",
            "PolRecvdFormat": "Recd. in Soft Copy",
            "BrokerBizType": "New",
            "InsurerBizType": "New",
            "OwnerDriver(LPD)": "0",
            "RoadsideAssistance(WithoutBrokerage)": "0",
            "StampDuty": "0",
            "TranNo": "0",
            "CessRate": "0",
            "BrokRate": "",  # To be entered manually
            "TPBrokRate": "0",
            "OwnerDriver%": "0",
            "RewardRate": "0",
            "RewardTPRate": "0",
            "RewardRateOn": "PREMIUM",  # To be entered manually
            "ExpRate": "0",
            "TPExpRate": "0",
            "RefRate": "0",
            "RefTPRate": "0",
            "POS/MISPRate": "0",
            "TPPOS/MISPRate": "0",
            "PayAt": "",  # To be entered manually
            "CSCRate": "0",
            "PolicyStatus": "LoggedIn",
            "Remarks": "Fresh",
            "CampaignName": "No Campaign",
        }

    def write_txt_file(self, filename, policy):
        # Write txt files for PDF, if requested (for debugging)
        if self.txt_file_directory:
            os.makedirs(self.txt_file_directory, exist_ok=True)

            with open(f"{self.txt_file_directory}/{filename}.txt", "w") as txt_file:
                txt_file.write(policy.content)

    def extract_data_from_pdf(self):
        extracted_data = []
        error_data = []
        for input_file in self.input_files:
            row = {}

            if isinstance(input_file, str):
                file = input_file
            else:
                file = input_file.file

            file_prefix = os.path.basename(file).strip()

            try:
                # print(f"Parsing {file}")
                policy = get_policy_parser(file)
                self.write_txt_file(file_prefix, policy)

                if policy.__class__ == BasePolicyParser:
                    row["file"] = file_prefix
                    row["reason"] = "Unable to identify Insurer"
                    error_data.append(row)
                elif policy.get_insurer() not in ENABLED_INSURERS:
                    row["file"] = file_prefix
                    row["remarks"] = SAIBA_INSURERS[policy.get_insurer()]
                    row["reason"] = "Insurer Disabled"
                    error_data.append(row)
                else:
                    row.update(self.transform_to_saibaa(policy))
                    # Add filename to excel for debugging purposes
                    row["file"] = file_prefix
                    extracted_data.append(row)
            except Exception as e:
                print(f"Unable to read file: '{file}'. {e}.")
                row["file"] = file
                row["reason"] = f"Unable to read PDF. {e}."
                error_data.append(row)
                continue

        return (extracted_data, error_data)


def pdf_to_csv(args):
    input_count = 0
    success_count = 0
    error_count = 0
    error_data = []

    # Validation checks for input arguments
    if args.input_files and args.input_dir:
        sys.stderr.write("Only one of either input_files or input_directory can be given\n")
        return 1

    if args.input_dir:
        input_files = glob.glob(glob.escape(args.input_dir) + "/**/*.[pP][dD][fF]", recursive=True)
    elif args.input_files:
        input_files = args.input_files
    else:
        sys.stderr.write("Either input_files or input_directory must be given\n")
        return 1

    # Read master files
    print("Reading Branch Master...")
    Masters.read_branch_master(args.branch_master)

    output_file = Path(args.output_file)
    # Create output directories if they don't exist
    output_file.parent.mkdir(parents=True, exist_ok=True)

    # Unless successful, consider all as errors, hence error count = input count
    input_count = error_count = len(input_files)

    parser = PolicyParser(
        date=args.processing_date, files=input_files, txt_file_directory=args.generate_txt_file
    )
    with ExcelDictWriter(output_file) as writer:
        print(f"Processing {input_count} PDF Files...")
        writer.add_headers(SAIBA_HEADERS)
        extracted_data, error_data = parser.extract_data_from_pdf()
        error_count = len(error_data)
        success_count = len(extracted_data)

        serial_number = 1
        for row in extracted_data:
            row["Sno"] = serial_number
            try:
                writer.add_row(row)
            except Exception as e:
                print(e)
                print(row)
                raise
            serial_number += 1
    print("Processing complete.")

    error_file = Path(args.error_file)
    # Create output directories if they don't exist
    error_file.parent.mkdir(parents=True, exist_ok=True)
    with ExcelDictWriter(error_file) as writer:
        writer.add_headers(["file", "reason", "remarks"])
        for row in error_data:
            writer.add_row(row)

    return {"input": input_count, "success": success_count, "error": error_count}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process PDF File")
    parser.add_argument(
        "--files", "-f", dest="input_files", type=str, nargs="*", help="File path to process"
    )
    parser.add_argument(
        "--dir",
        "-d",
        metavar="input directory",
        dest="input_dir",
        type=str,
        help="Directory to process",
    )
    parser.add_argument(
        "--error", "-e", dest="error_file", type=str, help="Error Report File", default="errors.csv"
    )
    parser.add_argument(
        "--output", "-o", dest="output_file", type=str, help="Output File", required=True
    )
    parser.add_argument(
        "--branches", "-b", dest="branch_master", type=str, help="Branch Master", required=True
    )
    parser.add_argument(
        "--gentxt",
        "-g",
        dest="generate_txt_file",
        type=str,
        help="Directory to generate txt files of pdfs",
    )
    parser.add_argument(
        "--processing-date",
        "-p",
        dest="processing_date",
        type=str,
        help="Processing Date (mm/dd/yyyy)",
        required=True,
    )

    parser.add_argument("--remote", "-r", dest="remote_string", type=str, help="Remote String")

    args = parser.parse_args()

    result = pdf_to_csv(args)
    print(f"\nExecution Timestamp: {datetime.now().isoformat()}")
    print(f"Processing Date: {args.processing_date}")
    print(f"Total Files Processed: {result['input']}")
    print(f"Successful Files: {result['success']}")
    print(f"Files with error: {result['error']}")
