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