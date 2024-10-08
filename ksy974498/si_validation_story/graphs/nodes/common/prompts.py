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