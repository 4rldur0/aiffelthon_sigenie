summary_template = """
# Mandatory information required in Shipping Instructions
Irrespective of the format shipping instructions are presented in, certain details are mandatory. 


## Container number
Container numbers are unique sequences used to identify and track containers as they move between ports. This number is displayed on the container door towards the top right. A container number typically has 4 letters followed by 7 numbers. It has 4 parts. 
The first three letters reflect the owner’s prefix. For example, all Maersk containers start with MAE while Hapag Lloyd containers have container numbers starting with HAM. 
The fourth letter is an equipment category identifier. The 7 numbers following the letters can also be broken into two parts. The first part has 6 digits. This refers to the serial number and is allocated by the container owner. The last digit is known as a check digit. This is used to validate the complete identification sequence with the Bureau of International Containers (BIC).
 

## Total number of packages
Your shipping instructions should include the total number of packages in each container as well as the overall total number of packages in all the containers being sent as one shipment. This helps ensure that nothing goes missing while in transit. 


## Type of package being shipped
The type of package will determine where the container is loaded on a ship as well as where it is held at port. For example, let’s say you are shipping fresh produce in refrigerated containers. These containers will need to be loaded and unloaded quickly since the container will be unable to maintain its internal temperature and pressure for more than a few hours when it is unplugged. 

 
## The gross weight of the cargo
This refers to the total weight of the shipment. Your shipper will need to know the total weight of the product and the weight of the packaging material being used for transportation. 
There are two reasons why this is important. Firstly, the weight of the cargo and the container will determine where it is loaded on the ship. To keep cargo from toppling over, the heaviest containers are loaded at the bottom and the lightest ones are loaded on the top. Further, they face import/export fees based on the cargo weight. Secondly, knowing the gross weight of the cargo helps freight forwarders choose the right truck transportation to deliver the cargo from the port to the delivery point. 

 
## Terms of payment
Shipping products over the oceans involves considerable risk.  Hence, choosing the appropriate payment terms is important. This must then be listed in the shipping instructions to avoid any misunderstanding. 
When you’re negotiating terms of payment, there are several factors to be included; loading charges, insurance, import and export duty, taxes, origin and destination terminal charges, carriage charges, etc. 
Payment may be made in advance, through a letter of credit from the bank, an open account or a telegraphic transfer.

 
## Cargo description
When it comes to customs clearance, cargo must be described in detail or it may be held up. It isn’t enough for the shipper to know that the container is transporting agricultural products. An acceptable cargo description would be the type of agricultural products being transported, i.e. apples, rice, bananas, etc. Similarly, if you’re shipping wires, the cargo description should specify whether the container has copper wires or steel wires. 

 
## Shipper’s name & address
The shipper refers to the exporter. They are responsible for packing and prepping the cargo as well as handling all documentation and paperwork. 
The shipping instructions must clearly state the shipper’s registered name and main office address. 

 

## Consignee’s name & address
The consignee is usually the owner of the goods and the person receiving the cargo. The consignee may be a company or an individual. Unless otherwise negotiated, the consignee must receive the cargo in person. 
Hence, it is important to have the consignee’s full name and address listed in the shipping instructions. 

 
## Other details
Depending on the country the products are being shipped from and the final port or receipt, many other local customs or regulations details may also need to be listed in the shipping instructions. 
For example, food products being exported from India will need certificates issued by the Export Inspection Council (EIC) that vouch for the safety and quality of the goods. 
"""

rag_prompt_template = """
# Compliance Verification
You are an expert in sanctions and compliance regulations.
Verify whether the following Shipping Instruction (SI) complies with any relevant compliance regulations.

Shipping Instruction: {si_data}

Provide a detailed response, including any relevant regulations, compliance issues, or the absence of any violations.
"""