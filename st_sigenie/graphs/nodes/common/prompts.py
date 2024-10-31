check_missing_prompt= """
    Analyze the following Shipping Instruction (SI) data, focusing on missing or incomplete information in key sections excluding the ‘Additional Information’ field.
    \n{format_instructions}
    \n{si_data}\n
"""

intake_report_prompt = """
You are a report generator AI. Your task is to summarize any issues or missing data in key sections.

{format_instructions}

Here is the shipment data:
{si_data}

Missing or problematic information:
{missing_info}
"""

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