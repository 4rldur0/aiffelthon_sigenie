b_l_prompt = """
# BILL OF LADING (B/L)

## SHIPPER / EXPORTER
{shipper_name}
{shipper_address}
Tel: {shipper_phone}

## CONSIGNEE
{consignee_name}
{consignee_address}
Tel: {consignee_phone}

## NOTIFY PARTY
{notify_name}
{notify_address}
Tel: {notify_phone}

## PLACE OF RECEIPT
{place_of_receipt}

## PORT OF LOADING
{port_of_loading}

## PORT OF DISCHARGE
{port_of_discharge}

## PLACE OF DELIVERY
{place_of_delivery}

## VESSEL NAME
{vessel_name}

## VOYAGE NUMBER
{voyage_number}

## PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE

### Marks and Numbers: 
{marks_numbers}

### Number of Packages: 
{num_of_packages}

### Description of Goods: 
{goods_description}

### Gross Weight (kg): 
{gross_weight}

### Measurement (CBM): 
{measurement_cbm}

## CONTAINER INFORMATION
Container No. | Seal No. | Number of Packages | Gross Weight (kg) | Measurement (CBM)
{container_info}

## TOTAL NUMBER OF CONTAINERS/PACKAGES RECEIVED BY THE CARRIER
{total_containers_packages}
"""
