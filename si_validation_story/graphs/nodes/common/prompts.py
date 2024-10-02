check_missing_prompt="""
Analyze the following Shipping Instruction (SI) data, focusing on missing or incomplete information in key sections excluding the ‘Additional Information’ field. Assess each section for completeness: ‘Voyage & Route Details,’ ‘Payment & Documentation,’ ‘Party Details,’ ‘Shipping Information,’ ‘Containers,’ and ‘Total Shipment.’ For missing or incomplete details, return a summary highlighting which data is missing or invalid. Provide a concise and structured output similar to the example below.

Data:
{si_data}

Example Output:

This is the summarized report on SI cherry202409072244:

	1. VESSEL VOYAGE BOUND: OK (APL TEMASEK, 2024581E)
	2. PARTIES
		- SHIPPER: OK
		- CONSIGNEE: OK
		- NOTIFY PARTY: OK
	3. PLACE OF RECEIPT: OK
		- PORT OF LOADING: OK
		- PORT OF DISCHARGING: OK
		- PLACE OF DELIVERY: OK
	4. DESCRIPTIONS OF GOODS
		- CONTAINER/SEAL NO: OK
		- CONTAINER UNIT: OK
		- MARKS AND NUMBERS: OK
		- NUMBER AND PACKAGE TYPE: OK
		- COMMODITY: OK (POWER TRANSFORMERS)
		- SHIPPING TERMS: OK (CIF)
		- FREIGHT TERMS: OK (COLLECT)
    5. ...
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