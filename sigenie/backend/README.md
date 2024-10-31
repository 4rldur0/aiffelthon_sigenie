# 🚢 SiGenie.ai
- LangChain, RAG, and Intelligent Agent.

## Setup
1. docker-compose build
2. docker-compose up
3. 
    - 1. http://127.0.0.1:8000/streaming_sync/chat/ch1?query="bookingreference"
        - ex) http://127.0.0.1:8000/streaming_sync/chat/ch2?query=CHERRY202409072244
    - 2. http://127.0.0.1:8000/streaming_sync/chat/ch2?query="bookingreference"

## Result 

### Ch1
```
event: get_si
data: content='{\'_id\': ObjectId(\'66e1562f0abd52a6a79a2ff6\'), \'bookingReference\': \'CHERRY202409072244\', \'voyageDetails\': {\'vesselName\': \'APL TEMASEK\', \'voyageNumber\': \'2024581E\'}, \'routeDetails\': {\'placeOfReceipt\': \'NINGBO\', \'portOfLoading\': \'NINGBO\', \'portOfDischarge\': \'YANTIAN\', \'placeOfDelivery\': \'YANTIAN\'}, \'paymentDetails\': {\'freightPaymentTerms\': \'COLLECT\', \'freightPayableAt\': \'ROTTERDAM, NETHERLANDS\'}, \'documentationDetails\': {\'blType\': \'NEGOTIABLE\', \'numberOfOriginalBLs\': \'3\', \'numberOfCopies\': \'0\'}, \'partyDetails\': {\'shipper\': {\'name\': \'SHIPPER 5029\', \'address\': \'NO. 188, SHANXI ROAD, NINGBO, CHINA\', \'telephone\': \'+86 574 8765 4321\'}, \'consignee\': {\'name\': \'EUROTECH TRADING BV\', \'address\': \'WATERLOO PLAZA, 121-123 WATERLOOPLEIN, 1011 PG AMSTERDAM, NETHERLANDS\', \'telephone\': \'+31 20 624 3500\'}, \'notifyParty\': {\'name\': \'EUROTECH TRADING BV\', \'address\': \'WATERLOO PLAZA, 121-123 WATERLOOPLEIN, 1011 PG AMSTERDAM, NETHERLANDS\', \'telephone\': \'+31 20 624 3500\'}}, \'shippingTerm\': \'CIF\', \'hsCode\': \'8541400000\', \'commodityDescription\': \'POWER TRANSFORMERS\', \'containers\': [{\'containerNumber\': \'TCLU9876543\', \'sealNumber\': \'123456\', \'containerType\': \'모름\', \'packageType\': \'CRATES\', \'numberOfPackages\': 2, \'grossWeight\': 15000.0, \'measurement\': 30.0, \'cargoDescription\': "SHIPPER\'S LOAD, COUNT & WEIGHT, SOTW & SEAL SAID TO CONTAIN: CIF, ROTTERDAM, NETHERLANDS POWER TRANSFORMERS", \'marksAndNumbers\': \'AS PER ATTACHED RIDER\'}, {\'containerNumber\': \'TCLU7654321\', \'sealNumber\': \'654321\', \'containerType\': \'모름\', \'packageType\': \'CRATES\', \'numberOfPackages\': 2, \'grossWeight\': 15000.0, \'measurement\': 30.0, \'cargoDescription\': "SHIPPER\'S LOAD, COUNT & WEIGHT, SOTW & SEAL SAID TO CONTAIN: CIF, ROTTERDAM, NETHERLANDS POWER TRANSFORMERS", \'marksAndNumbers\': \'AS PER ATTACHED RIDER\'}], \'totalShipment\': {\'totalContainers\': \'TWO (20 O/T X2) CONTAINERS ONLY\', \'totalPackages\': \'4\', \'packageType\': \'CRATES\', \'containerType\': \'20 O/TX2\', \'totalGrossWeight\': \'30000.0\', \'totalMeasurement\': \'60.0\'}, \'outOfGaugeDimensions\': {\'length\': 0, \'width\': 0, \'height\': 0, \'overWidth\': 0, \'overHeight\': 0}, \'additionalInformation\': {\'lcDetails\': {\'lcNumber\': \'0123456789\'}, \'certificateDetails\': \'1234567890\', \'originalBLDistribution\': {\'name\': \'BANK OF CHINA NINGBO BRANCH\', \'address\': \'NO. 123 HAIYAN ROAD, NINGBO, CHINA\', \'telephone\': \'+86 574 8666 7890\', \'fax\': \'+86 574 8666 7891\'}, \'originalInvoiceDistribution\': {\'name\': \'BANK OF CHINA NINGBO BRANCH\', \'address\': \'NO. 123 HAIYAN ROAD, NINGBO, CHINA\', \'telephone\': \'+86 574 8666 7890\', \'fax\': \'+86 574 8666 7891\'}, \'onboardDate\': \'2024-09-14 21:26\', \'additionalRemarks\': \'No special instructions\'}}' additional_kwargs={} response_metadata={}

event: check_missing_data
data: content="{'vessel_route_details': {'vessel_name': {'status': 'OK'}, 'voyage_number': {'status': 'OK'}, 'place_of_receipt': {'status': 'OK'}, 'port_of_loading': {'status': 'OK'}, 'port_of_discharge': {'status': 'OK'}, 'place_of_delivery': {'status': 'OK'}, 'total_status': 'Missing'}, 'payment_documentation': {'freight_payment_terms': {'status': 'OK'}, 'bl_type': {'status': 'OK'}, 'number_of_original_bls': {'status': 'OK'}, 'total_status': 'Missing'}, 'party_information': {'status': {'status': 'Missing', 'reason': 'Party information status not provided'}, 'total_status': 'Missing'}, 'shipping_details': {'status': {'status': 'Missing', 'reason': 'Shipping details status not provided'}, 'total_status': 'Missing'}, 'container_information': {'status': {'status': 'Missing', 'reason': 'Container information status not provided'}, 'total_status': 'Missing'}, 'total_shipment_summary': {'status': {'status': 'Missing', 'reason': 'Total shipment summary status not provided'}, 'total_status': 'Missing'}, 'additional_information': {'status': {'status': 'Missing', 'reason': 'Additional information status not provided'}, 'total_status': 'Missing'}, 'special_cargo_information': {'out_of_gauge_dimensions_info': {'status': 'OK'}, 'hazardous_materials_info': {'status': 'Missing', 'reason': 'Hazardous materials information not provided'}, 'refrigerated_cargo_info': {'status': 'Missing', 'reason': 'Refrigerated cargo information not provided'}, 'total_status': 'Missing'}, 'total_status': 'Missing'}" additional_kwargs={} response_metadata={}

event: generate_intake_report
data: {'overall_status': 'Missing', 'issues_found': 'Party information status not provided; Shipping details status not provided; Container information status not provided; Total shipment summary status not provided; Additional information status not provided; Hazardous materials information not provided; Refrigerated cargo information not provided.', 'missing_summary': 'Overall shipment status is missing; multiple sections lack complete information.', 'conclusion': 'The shipment report is incomplete and requires additional information to assess the overall status.'}
```

 ### Ch2
```
event: get_si
data: {'_id': ObjectId('66e1562f0abd52a6a79a2ff6'), 'bookingReference': 'CHERRY202409072244', 'voyageDetails': {'vesselName': 'APL TEMASEK', 'voyageNumber': '2024581E'}, 'routeDetails': {'placeOfReceipt': 'NINGBO', 'portOfLoading': 'NINGBO', 'portOfDischarge': 'YANTIAN', 'placeOfDelivery': 'YANTIAN'}, 'paymentDetails': {'freightPaymentTerms': 'COLLECT', 'freightPayableAt': 'ROTTERDAM, NETHERLANDS'}, 'documentationDetails': {'blType': 'NEGOTIABLE', 'numberOfOriginalBLs': '3', 'numberOfCopies': '0'}, 'partyDetails': {'shipper': {'name': 'SHIPPER 5029', 'address': 'NO. 188, SHANXI ROAD, NINGBO, CHINA', 'telephone': '+86 574 8765 4321'}, 'consignee': {'name': 'EUROTECH TRADING BV', 'address': 'WATERLOO PLAZA, 121-123 WATERLOOPLEIN, 1011 PG AMSTERDAM, NETHERLANDS', 'telephone': '+31 20 624 3500'}, 'notifyParty': {'name': 'EUROTECH TRADING BV', 'address': 'WATERLOO PLAZA, 121-123 WATERLOOPLEIN, 1011 PG AMSTERDAM, NETHERLANDS', 'telephone': '+31 20 624 3500'}}, 'shippingTerm': 'CIF', 'hsCode': '8541400000', 'commodityDescription': 'POWER TRANSFORMERS', 'containers': [{'containerNumber': 'TCLU9876543', 'sealNumber': '123456', 'containerType': '모름', 'packageType': 'CRATES', 'numberOfPackages': 2, 'grossWeight': 15000.0, 'measurement': 30.0, 'cargoDescription': "SHIPPER'S LOAD, COUNT & WEIGHT, SOTW & SEAL SAID TO CONTAIN: CIF, ROTTERDAM, NETHERLANDS POWER TRANSFORMERS", 'marksAndNumbers': 'AS PER ATTACHED RIDER'}, {'containerNumber': 'TCLU7654321', 'sealNumber': '654321', 'containerType': '모름', 'packageType': 'CRATES', 'numberOfPackages': 2, 'grossWeight': 15000.0, 'measurement': 30.0, 'cargoDescription': "SHIPPER'S LOAD, COUNT & WEIGHT, SOTW & SEAL SAID TO CONTAIN: CIF, ROTTERDAM, NETHERLANDS POWER TRANSFORMERS", 'marksAndNumbers': 'AS PER ATTACHED RIDER'}], 'totalShipment': {'totalContainers': 'TWO (20 O/T X2) CONTAINERS ONLY', 'totalPackages': '4', 'packageType': 'CRATES', 'containerType': '20 O/TX2', 'totalGrossWeight': '30000.0', 'totalMeasurement': '60.0'}, 'outOfGaugeDimensions': {'length': 0, 'width': 0, 'height': 0, 'overWidth': 0, 'overHeight': 0}, 'additionalInformation': {'lcDetails': {'lcNumber': '0123456789'}, 'certificateDetails': '1234567890', 'originalBLDistribution': {'name': 'BANK OF CHINA NINGBO BRANCH', 'address': 'NO. 123 HAIYAN ROAD, NINGBO, CHINA', 'telephone': '+86 574 8666 7890', 'fax': '+86 574 8666 7891'}, 'originalInvoiceDistribution': {'name': 'BANK OF CHINA NINGBO BRANCH', 'address': 'NO. 123 HAIYAN ROAD, NINGBO, CHINA', 'telephone': '+86 574 8666 7890', 'fax': '+86 574 8666 7891'}, 'onboardDate': '2024-09-14 21:26', 'additionalRemarks': 'No special instructions'}}

event: check_parties
data: This is the summarized validation report for shipping instruction

1. Shipper
- Address: The address format is correct for China, but it lacks a postal code. A postal code is essential for proper delivery.
- Telephone: The phone number format is correct, including the country code.

2. Consignee
- Address: The address format is correct for the Netherlands, including the postal code (1011 PG). No issues found.
- Telephone: The phone number format is correct, including the country code.

3. Notify Party
- Address: The address format is correct for the Netherlands, including the postal code (1011 PG). No issues found.
- Telephone: The phone number format is correct, including the country code.
- Note: The Notify Party is the same as the Consignee, which is acceptable. 

Overall, the main issue is the missing postal code for the Shipper's address.

event: verify_company_policy
data: The Shipping Instruction (SI) provided has been summarized and evaluated for compliance with relevant regulations. Here’s a detailed analysis:

### 1. Shipper
- **Address**: The address format is correct for China, but it lacks a postal code. 
  - **Compliance Issue**: A postal code is essential for proper delivery and is often required for customs clearance. The absence of a postal code could lead to delays or issues with the shipment.
  - **Regulations**: According to international shipping regulations and local postal requirements, complete address information, including postal codes, is necessary for compliance.

- **Telephone**: The phone number format is correct, including the country code.
  - **Compliance Status**: No issues found.

### 2. Consignee
- **Address**: The address format is correct for the Netherlands, including the postal code (1011 PG).
  - **Compliance Status**: No issues found.

- **Telephone**: The phone number format is correct, including the country code.
  - **Compliance Status**: No issues found.

### 3. Notify Party
- **Address**: The address format is correct for the Netherlands, including the postal code (1011 PG).
  - **Compliance Status**: No issues found.

- **Telephone**: The phone number format is correct, including the country code.
  - **Compliance Status**: No issues found.

- **Note**: The Notify Party is the same as the Consignee, which is acceptable.
  - **Compliance Status**: No issues found.

### Overall Compliance Assessment
- **Main Issue**: The primary compliance issue identified is the missing postal code for the Shipper's address. This could potentially violate shipping regulations that require complete and accurate address information for customs and delivery purposes.
- **Recommendations**: It is recommended to obtain and include the postal code for the Shipper's address to ensure compliance with shipping regulations and to avoid any potential delays or issues with the shipment.

### Conclusion
The Shipping Instruction is mostly compliant, with the exception of the missing postal code for the Shipper. Addressing this issue will enhance compliance with relevant regulations and facilitate smoother shipping processes.

event: verify_vessel_port_situation
data: {'query': '"NINGBO port APL TEMASEK news"', 'follow_up_questions': None, 'answer': "The port of Ningbo-Zhoushan experienced an explosion, leading to its closure and exacerbating bottlenecks in Asian shipping. The incident occurred on a container ship berthed at the port, raising serious safety concerns in ocean container shipping. The explosion resulted in the shutdown of Ningbo Beilun's Phase III Terminal indefinitely. Additionally, the APL TEMASEK, the largest vessel in APL's fleet, made its maiden call at YICT on March 20th.", 'images': [], 'results': [{'url': 'https://www.joc.com/article/ningbo-explosion-closes-port-adds-to-worsening-asian-bottlenecks-5703235', 'title': 'Ningbo explosion closes port, adds to worsening Asian bottlenecks', 'content': 'Aug 9, 2024 · Ningbo explosion closes port, adds to worsening Asian bottlenecks. The port of Ningbo-Zhoushan is the second largest in China and handled 35.3\xa0...Missing:  APL TEMASEK', 'score': 0.99392605, 'raw_content': None}, {'url': 'https://www.ajot.com/news/explosion-at-ningbo-zhoushan-port-in-china-raises-serious-safety-concerns-in-ocean-container-shipping', 'title': 'Explosion at Ningbo-Zhoushan port in China raises serious safety ...', 'content': 'Aug 9, 2024 · A major explosion has occurred on a container ship while berthed at the port of Ningbo-Zhoushan in China in another incident that raises serious safety\xa0...Missing:  APL TEMASEK', 'score': 0.9933846, 'raw_content': None}, {'url': 'https://industrialautomationco.com/blogs/news/the-ningbo-port-explosion-unraveling-the-impact-on-global-trade-and-exploring-alternatives?srsltid=AfmBOooqBNyDE-8KvkkNOSrOpUQp62Nk-ywTNEFPPB5ByI4Dwh7b9wct', 'title': 'The Ningbo Port Explosion: Unraveling the Impact on Global Trade ...', 'content': "Aug 15, 2024 · The Ningbo Beilun's Phase III Terminal, one of the world's busiest intermodal hubs, was forced to shut down indefinitely following a hazardous materials\xa0...Missing:  APL TEMASEK", 'score': 0.9923638, 'raw_content': None}, {'url': 'https://yict.com.cn/article/detail/3461.html?locale=en_US', 'title': 'YICT Welcomes the Maiden Call of the 14000-TEU APL TEMASEK', 'content': "On 20 March, the APL TEMASEK, the largest vessel in APL's fleet, made her maiden call at YICT. Measuring 368 metres long, 51 metres wide, the vessel has a\xa0...", 'score': 0.97599226, 'raw_content': None}, {'url': 'https://www.cnbc.com/2024/08/09/chinas-ningbo-port-reports-explosion-on-container-ship-state-news-agency-says.html', 'title': "Container explodes on cargo ship at China's key Ningbo port - CNBC", 'content': "Aug 9, 2024 · A hazardous goods container exploded Friday on a ship operating in China's Ningbo Port, vessel owner Yang Ming told CNBC in a statement.Missing:  APL TEMASEK", 'score': 0.9621787, 'raw_content': None}], 'response_time': 4.76}

event: generate_validation_report
data: ### Summary of Validation Report for Shipping Instruction

1. **Shipper**
   - **Address**: Correct format for China, but missing postal code (essential for delivery).
   - **Telephone**: Correct format, including country code.

2. **Consignee**
   - **Address**: Correct format for the Netherlands, including postal code (1011 PG).
   - **Telephone**: Correct format, including country code.

3. **Notify Party**
   - **Address**: Correct format for the Netherlands, including postal code (1011 PG).
   - **Telephone**: Correct format, including country code.
   - **Note**: Notify Party is the same as Consignee, which is acceptable.

### Overall Compliance Assessment
- **Main Issue**: Missing postal code for the Shipper's address, which could lead to delivery issues and non-compliance with shipping regulations.
- **Recommendations**: Include the postal code for the Shipper's address to ensure compliance and avoid shipment delays.

### Conclusion
The Shipping Instruction is mostly compliant, with the primary issue being the missing postal code for the Shipper. Addressing this will enhance compliance and facilitate smoother shipping processes.

---

### Incident Report: Ningbo Port Explosion

- An explosion occurred on a container ship at Ningbo-Zhoushan port, leading to its indefinite closure and worsening shipping bottlenecks in Asia.
- The incident raised serious safety concerns in ocean container shipping.
- The APL TEMASEK, the largest vessel in APL's fleet, made its maiden call at YICT on March 20, 2024.
- The closure of Ningbo Beilun's Phase III Terminal is expected to impact global trade significantly.

### Relevant Articles
1. [Ningbo explosion closes port, adds to worsening Asian bottlenecks](https://www.joc.com/article/ningbo-explosion-closes-port-adds-to-worsening-asian-bottlenecks-5703235)
2. [Explosion at Ningbo-Zhoushan port raises serious safety concerns](https://www.ajot.com/news/explosion-at-ningbo-zhoushan-port-in-china-raises-serious-safety)
3. [Impact of the Ningbo Port explosion on global trade](https://industrialautomationco.com/blogs/news/the-ningbo-port-explosion-unraveling-the-impact-on-global-trade-and-exploring-alternatives?srsltid=AfmBOooqBNyDE-8KvkkNOSrOpUQp62Nk-ywTNEFPPB5ByI4Dwh7b9wct)
4. [YICT Welcomes the Maiden Call of the APL TEMASEK](https://yict.com.cn/article/detail/3461.html?locale=en_US)
5. [Container explodes on cargo ship at Ningbo port](https://www.cnbc.com/2024/08/09/chinas-ningbo-port-reports-explosion-on-container-ship-state-news-agency-says.html)
```