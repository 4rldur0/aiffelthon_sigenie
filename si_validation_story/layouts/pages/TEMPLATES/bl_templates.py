bl_html = f"""
        <div class="bl-form">
            <div class="watermark">DRAFT</div>
            <div class="bl-header">
                <div class="bl-title">
                    <h2>BILL OF LADING (B/L)</h2>
                </div>
                <div>
                    <p class="bl-row"><strong>Booking Number:</strong> {doc.get('bookingReference', '')}</p>
                    <p class="bl-row"><strong>Service Type:</strong> {doc.get('service', '')}</p>
                    <p class="bl-row"><strong>B/L Number:</strong> {doc.get('bookingReference', '')}</p>
                </div>
                <div class="bl-logo">
                    <img src="data:image/jpeg;base64,{logo_base64}" alt="Company Logo">
                </div>
            </div>
            <div class="bl-section">
                <h3>SHIPPER / EXPORTER (Full Name and Address)</h3>
                <p class="bl-row">{doc.get('partyDetails', {}).get('shipper', {}).get('name', '')}</p>
                <p class="bl-row">{doc.get('partyDetails', {}).get('shipper', {}).get('address', '')}</p>
                <p class="bl-row">Tel: {doc.get('partyDetails', {}).get('shipper', {}).get('telephone', '')}</p>
            </div>
            <div class="bl-section">
                <h3>CONSIGNEE (Full Name and Address)</h3>
                <p class="bl-row">{doc.get('partyDetails', {}).get('consignee', {}).get('name', '')}</p>
                <p class="bl-row">{doc.get('partyDetails', {}).get('consignee', {}).get('address', '')}</p>
                <p class="bl-row">Tel: {doc.get('partyDetails', {}).get('consignee', {}).get('telephone', '')}</p>
            </div>
            <div class="bl-section">
                <h3>NOTIFY PARTY (Full Name and Address)</h3>
                <p class="bl-row">{doc.get('partyDetails', {}).get('notifyParty', {}).get('name', '')}</p>
                <p class="bl-row">{doc.get('partyDetails', {}).get('notifyParty', {}).get('address', '')}</p>
                <p class="bl-row">Tel: {doc.get('partyDetails', {}).get('notifyParty', {}).get('telephone', '')}</p>
            </div>
            <div class="bl-grid">
                <div class="bl-section">
                    <h3>PLACE OF RECEIPT</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('placeOfReceipt', '')}</p>
                </div>
                <div class="bl-section">
                    <h3>PORT OF LOADING</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('portOfLoading', '')}</p>
                </div>
            </div>
            <div class="bl-grid">
                <div class="bl-section">
                    <h3>PORT OF DISCHARGE</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('portOfDischarge', '')}</p>
                </div>
                <div class="bl-section">
                    <h3>PLACE OF DELIVERY</h3>
                    <p class="bl-row">{doc.get('routeDetails', {}).get('placeOfDelivery', '')}</p>
                </div>
            </div>
            <div class="bl-grid">
                <div class="bl-section">
                    <h3>VESSEL NAME</h3>
                    <p class="bl-row">{doc.get('voyageDetails', {}).get('vesselName', '')}</p>
                </div>
                <div class="bl-section">
                    <h3>VOYAGE NUMBER</h3>
                    <p class="bl-row">{doc.get('voyageDetails', {}).get('voyageNumber', '')}</p>
                </div>
            </div>

        <div class="bl-section">
            {particulars_html}
        </div>
        <div class="bl-section">
            {container_info_html}
        </div>
        <div class="bl-section">
            {footer_info_html}
        </div>
        <div class="bl-footer">
            <p class="small-text">The number of containers of packages shown in the 'TOTAL No. OF CONTAINERS OR PACKAGES RECEIVED BY THE CARRIER's box which are said by the shipper to hold or consolidate the goods described in the PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE box, have been received by CHERRY SHIPPING LINE from the shipper in apparent good order and condition except as otherwise indicated hereon - weight, measure, marks, numbers, quality, quantity, description, contents and value unknown - for Carriage from the Place of Receipt or the Port of loading (whichever is applicable) to the Port of Discharge or the Place of Delivery (whichever is applicable) on the terms and conditions hereof INCLUDING THE TERMS AND CONDITIONS ON THE REVERSE SIDE HEREOF, THE CARRIER'S APPLICABLE TARIFF AND THE TERMS AND CONDITIONS OF THE PRECARRIER AND ONCARRIER AS APPLICABLE IN ACCORDANCE WITH THE TERMS AND CONDITIONS ON THE REVERSE SIDE HEREOF.</p>
            <p class="small-text">IN WITNESS WHEREOF {doc['documentationDetails']['numberOfOriginalBLs']} ({doc['documentationDetails']['numberOfOriginalBLs']} in words) ORIGINAL BILLS OF LADING (unless otherwise stated above) HAVE BEEN SIGNED ALL OF THE SAME TENOR AND DATE, ONE OF WHICH BEING ACCOMPLISHED THE OTHER(S) TO STAND VOID.</p>
            <div class="bl-grid">
                <div>
                    <p class="bl-row"><strong>CHERRY SHIPPING LINE</strong></p>
                    <p class="bl-row"><strong>as Carrier</strong></p>
                    <p class="bl-row">By ContainerGenie.ai CO., LTD.</p>
                    <p>as Agents only for Carrier</p>
                </div>
                <div>
                    <p class="bl-row"><strong>Place Issued: {doc['paymentDetails']['freightPayableAt']}</strong></p>
                    <p class="bl-row"><strong>Date Issued: {doc['additionalInformation']['onboardDate']}</strong></p>
                </div>
            </div>
        </div>
        """