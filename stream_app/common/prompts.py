# json 형식으로 prompting
check_missing_prompt="""
    Analyze the following Shipping Instruction (SI) data, focusing on missing or incomplete information in key sections.
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

##### CH2

check_parties_prompt = """
You are a documentation validation assistant specializing in verifying party details in shipping instructions.
Make sure shipper, consignee, and nofifyParty in the data contain all the essential info as guided below:

# data:
{si_data}


# Instructions:
1. walk through each step carefully, explaining the thought process in detail.             
2. It is the rule that you have to mention address, phone or fax number, and email address, which are fundamentally mandatory items.              
3. Use PDF_retriever_tool to tell whether email address is not required.
4. Confirm address is in proper format of the respective country with explicit numeric postal code.
5. Do not attempt to infer or provide any missing elements such as a postal code in the address.
6. Verify if phone or FAX number definitely matches the general contacts format with area code.
7. Check whether email address is in proper format.
8. NotifyParty can be the same as consignee, the point that does't matter at all.
9. Any closing remarks at the bottom of the report are not preferred.
10. After reaching the final answer, review the solution once more to ensure it is correct.


# Respond in the example as below:
This is the summarized validation report for shipping instruction.

1. Shipper
- Address: The address part is valid containing a postal code(12345) for the related country.
- Phone: The phone number format is right with a conventional area code(99) for the related country included.
- Email: An email address is omitted, the item which is required.

2. Consignee
- Address: The address part is invalid as a postal code(99999) for the related country is not shown.
- Phone: A phone number is not detected.
- Email: The email address is in the correct format.

3. Notify Party
- Address: The address input is void.
- Phone: The phone number format is provided without a conventional area code(11) for the related country.
- Email: The email address is left empty, the item which is not mandatory.

# Answer:
{agent_scratchpad}
"""

verify_company_policy_prompt = """
You are tasked with verifying Company Compliance based on the provided SI information and matching the regulations specific to the involved countries. The compliance must be validated according to both the international and local country policies listed in the provided sources.

Make sure to consider the countries involved in the shipment (e.g., the place of receipt, port of loading, port of discharge, and final destination) and match the relevant policies accordingly. Your goal is to identify any compliance violations or discrepancies based on these country-specific policies and output them in the following format:

- Company Policy -
1. [Compliance Issue] (Source [x] page [y]) [Country: [Country Name]]
2. [Compliance Issue] (Source [x] page [y]) [Country: [Country Name]]
3. [Compliance Issue] (Source [x] page [y]) [Country: [Country Name]]
...
[Source]
Source [x]: [Source Title] Page [y], Chapter [z] [Additional details if necessary, e.g., URL]

**SI Information**:
{si_data}

Answer: 
{agent_scratchpad}
"""

query_prompt = """
Based on the following shipment data, generate a concise web search query to find recent news about the port and vessel. 
The search query should include the port of loading and the vessel name.

Shipment Data:
{si_data}

Generate a search query that might return recent news about the status of the port and the vessel's voyage.
"""

validation_report_prompt = """
Summarize data below

Data: 
{si_data}

Parties Check:
{parties_check}

Verify company policy:
{verify_company_policy}

Response Format:
- Summary -
1. Party: ....
2. Company policy: .... 3. Vessel: ....
4. Port: ....

- Recommandation -
1. Contact shipper to secure LEI data and correct address format. 
2. Contact notify party to secure missing data for USCI data.
3. .... 
4. .....

- Alert -
1. The commodity is under sanction. Therefore need cancel booking.
2. As the vessel will by pass the POD, need to reroute via other vessel

Party, Company Policy, Vessel, Port, Summary, Recommendation, Alert 표시

Sanction, Prohibited 해당하는 정보에 대해서는 Alert를 통해 특별히 강조
"""