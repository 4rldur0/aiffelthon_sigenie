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
intake_report_prompt="""
Summarize data below

Data: 
{sources}
"""
check_parties_prompt = """
You are a documentation validation assistant specializing in verifying party details in shipping instructions.
    On the basis of {si_data}, shipper, consignee, and nofifyParty have to contain all the essential info the right way.
1. confirm address including zip code is in proper format of the respective country.
2. verify if phone or FAX number matches the general contacts format including country and area codes.
3. check whether email address is provided, if mandatory depending on the relevant country.
4. notifyParty can be the same as consignee.
 

# Please respond in the following format:
This is the summarized validation report for shipping instruction

1. Shipper
- detailed issue, if any

2. Consignee
- detailed issue, if any

3. Notify Party
- detailed issue, if any

# Answer:
{agent_scratchpad}
"""

verify_company_policy_prompt = """
# Compliance Verification
You are an expert in sanctions and compliance regulations.
Verify whether the following Shipping Instruction (SI) complies with any relevant compliance regulations.

Shipping Instruction: {si_data}

Provide a detailed response, including any relevant regulations, compliance issues, or the absence of any violations.

Answer: 
{agent_scratchpad}
"""

validation_report_prompt = """
Summarize data below

Data: 
{sources}
"""