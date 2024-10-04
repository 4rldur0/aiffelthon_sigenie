check_missing_prompt="""
Analyze the following Shipping Instruction (SI) data, focusing on missing or incomplete information in key sections excluding the ‘Additional Information’ field.
For missing or incomplete details, return a summary highlighting which data is missing or invalid(`:red[MISSING]`,'`:blue[WARNING]`).
Provide a concise and structured output similar to the example below.

Data:
{si_data}

Response Format:

	1.	Vessel & Route Details: OK
	2.	Payment & Documentation: OK
	3.	Party Information: OK
	4.	Shipping Details: OK
	5.	Container Information: OK
	6.	Total Shipment Summary: OK
	7.	Additional Information: OK
	8.	Special Cargo Information: OK

"""

# json 형식으로 prompting
# add: function calling
## check : value, 이유 - 정확도 측면에서 

intake_report_prompt = """
Add Summarization of the missing information.
Write Summarziation before Missing Information.

Missing Information: {missing_info}
"""

# intake_report_prompt="""
# Summarize data below

# Data: 
# {sources}
# """

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