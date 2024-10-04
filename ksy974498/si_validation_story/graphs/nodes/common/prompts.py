# json 형식으로 prompting
check_missing_prompt="""
    Analyze the following Shipping Instruction (SI) data, focusing on missing or incomplete information in key sections excluding the ‘Additional Information’ field.
    \n{format_instructions}
    \n{si_data}\n
"""

intake_report_prompt =  """
You are a report generator AI. Your task is to summarize any issues or missing data in key sections.

{format_instructions}

Here is the shipment data:
{si_data}

Missing or problematic information:
{missing_info}
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

verify_company_policy_prompt = """
# Compliance Verification
You are an expert in sanctions and compliance regulations.
Verify whether the following Shipping Instruction (SI) complies with any relevant compliance regulations.

Shipping Instruction: {si_data}

Provide a detailed response, including any relevant regulations, compliance issues, or the absence of any violations.
"""

validation_report_prompt = """
Summarize data below

Data: 
{sources}
"""