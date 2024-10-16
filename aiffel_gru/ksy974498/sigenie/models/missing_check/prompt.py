## Example:
# PREFIX = """Answer the following questions as best you can. You have access to the following tools:"""
# FORMAT_INSTRUCTIONS = """Use the following format:

# Question: the input question you must answer
# Thought: you should always think about what to do
# Action: the action to take, should be one of [{tool_names}]
# Action Input: the input to the action
# Observation: the result of the action
# ... (this Thought/Action/Action Input/Observation can repeat N times)
# Thought: I now know the final answer
# Final Answer: the final answer to the original input question"""
# SUFFIX = """Begin!

# Question: {input}
# Thought:{agent_scratchpad}"""

missing_check_prompt = """
Are there any missing data with the following shipping instruction:
Except for Additional Information is needed.
Find from following data :\n{si_data}.
Just say `OK` or `MISSING` per group.
"""