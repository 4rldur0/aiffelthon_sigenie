from prompt_templates import b_l_prompt

def generate_bill_of_lading(si_data):
    """
    Generate a bill of lading based on the provided SI data.
    """
    # Extract details from the shipping instruction data
    shipper_name = si_data.get('partyDetails', {}).get('shipper', {}).get('name', 'N/A')
    shipper_address = si_data.get('partyDetails', {}).get('shipper', {}).get('address', 'N/A')
    shipper_phone = si_data.get('partyDetails', {}).get('shipper', {}).get('telephone', 'N/A')

    consignee_name = si_data.get('partyDetails', {}).get('consignee', {}).get('name', 'N/A')
    consignee_address = si_data.get('partyDetails', {}).get('consignee', {}).get('address', 'N/A')
    consignee_phone = si_data.get('partyDetails', {}).get('consignee', {}).get('telephone', 'N/A')

    notify_name = si_data.get('partyDetails', {}).get('notifyParty', {}).get('name', 'N/A')
    notify_address = si_data.get('partyDetails', {}).get('notifyParty', {}).get('address', 'N/A')
    notify_phone = si_data.get('partyDetails', {}).get('notifyParty', {}).get('telephone', 'N/A')

    place_of_receipt = si_data.get('routeDetails', {}).get('placeOfReceipt', 'N/A')
    port_of_loading = si_data.get('routeDetails', {}).get('portOfLoading', 'N/A')
    port_of_discharge = si_data.get('routeDetails', {}).get('portOfDischarge', 'N/A')
    place_of_delivery = si_data.get('routeDetails', {}).get('placeOfDelivery', 'N/A')

    vessel_name = si_data.get('voyageDetails', {}).get('vesselName', 'N/A')
    voyage_number = si_data.get('voyageDetails', {}).get('voyageNumber', 'N/A')

    marks_numbers = si_data.get('containers', [{}])[0].get('marksAndNumbers', 'N/A')
    num_of_packages = si_data.get('totalShipment', {}).get('totalPackages', 'N/A')
    goods_description = si_data.get('commodityDescription', 'N/A')
    gross_weight = si_data.get('totalShipment', {}).get('totalGrossWeight', 'N/A')
    measurement_cbm = si_data.get('totalShipment', {}).get('totalMeasurement', 'N/A')

    container_info = ""
    containers = si_data.get('containers', [])
    for container in containers:
        container_info += f"{container.get('containerNumber', 'N/A')} | {container.get('sealNumber', 'N/A')} | {container.get('numberOfPackages', 'N/A')} | {container.get('grossWeight', 'N/A')} | {container.get('measurement', 'N/A')}\n"

    total_containers_packages = f"{si_data.get('totalShipment', {}).get('totalContainers', 'N/A')} / {num_of_packages} packages"

    # Format the Bill of Lading report
    report = b_l_prompt.format(
        shipper_name=shipper_name,
        shipper_address=shipper_address,
        shipper_phone=shipper_phone,
        consignee_name=consignee_name,
        consignee_address=consignee_address,
        consignee_phone=consignee_phone,
        notify_name=notify_name,
        notify_address=notify_address,
        notify_phone=notify_phone,
        place_of_receipt=place_of_receipt,
        port_of_loading=port_of_loading,
        port_of_discharge=port_of_discharge,
        place_of_delivery=place_of_delivery,
        vessel_name=vessel_name,
        voyage_number=voyage_number,
        marks_numbers=marks_numbers,
        num_of_packages=num_of_packages,
        goods_description=goods_description,
        gross_weight=gross_weight,
        measurement_cbm=measurement_cbm,
        container_info=container_info,
        total_containers_packages=total_containers_packages
    )

    return report