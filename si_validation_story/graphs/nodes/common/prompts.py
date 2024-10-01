check_missing_prompt="""
    Are there any missing data with the following shipping instruction:
    Except for Additional Information is needed.
    Find from following data :\n{si_data}.
    Just say `OK` or `MISSING` per group.
"""
validation_report_prompt = """

"""
check_parties_prompt = """
Found following issues in shipper, consignee, and notify parties' data

## Example
Incorrect/Miswrite
Shipper:
    - The Postal/Zip code is not correct for the country.
    - PHONE & FAX NO shall be input.
Consignee:
    - The format and logic of the address are not suitable for the country.
    - The spelling mistakes on the parties & the description is incorrect.
Notify:OK. 
    - E-mail Mark is an option.
"""

validate_compliance_prompt = """
# Compliance Verification
You are an expert in sanctions and compliance regulations.
Verify whether the following Shipping Instruction (SI) complies with any relevant compliance regulations.

Shipping Instruction: {si_data}

Provide a detailed response, including any relevant regulations, compliance issues, or the absence of any violations.
"""

verify_company_policy_prompt = """

"""