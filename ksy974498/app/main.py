from langgraph import LangGraph

# Defining function nodes
def import_json_si(data):
    # Function for importing JSON type SI
    # Implementation details here
    return parsed_data

def check_missing_data(data):
    # Function for checking missing data in shipping instructions
    # Implementation details here
    return missing_fields

# LLM agent prompt examples
def llm_agent_verify_parties(data):
    prompt = f"Please verify the party details in the following shipping instruction: {data}"
    response = chatgpt_4o_mini(prompt)
    return response

def llm_agent_check_company_policy(data, company_policy_db):
    prompt = f"Validate the shipping instruction with the company policy: {data} with {company_policy_db}"
    response = chatgpt_4o_mini(prompt)
    return response

# Define LangGraph structure
graph = LangGraph()

# Chapter 1 Nodes
graph.add_node("Import_JSON_SI", function=import_json_si)
graph.add_node("Check_Missing_Data", function=check_missing_data)
graph.add_node("Generate_Intake_Report", function=generate_intake_report)

# Chapter 2 Nodes
graph.add_node("Check_Parties", agent=llm_agent_verify_parties)
graph.add_node("Verify_Company_Policy", agent=llm_agent_check_company_policy)
graph.add_node("Generate_Validation_Report", function=generate_validation_report)

# Define the flow connections between nodes
graph.connect("Import_JSON_SI", "Check_Missing_Data")
graph.connect("Check_Missing_Data", "Generate_Intake_Report")
graph.connect("Generate_Intake_Report", "Check_Parties")
graph.connect("Check_Parties", "Verify_Company_Policy")
graph.connect("Verify_Company_Policy", "Generate_Validation_Report")

# Execute the graph
result = graph.run(input_data)