class BLHTML:
    def __init__(self, doc, logo_img):
        self.doc = doc
        self.logo_img = logo_img
        self.particulars_html = self._init_particulars_table()
        self.container_info_html = self._init_container_info_table()
        self.footer_info_html = self._init_footer_info()

        # Create the full BL HTML
        self.bl_html = self._create_bl_html()

    def _init_particulars_table(self):
        return """
        <h3>PARTICULARS FURNISHED BY SHIPPER - CARRIER NOT RESPONSIBLE</h3>
        <table class="bl-table">
            <tr>
                <th>MARKS AND NUMBERS</th>
                <th>NO. OF CONTAINERS OR PACKAGES</th>
                <th>DESCRIPTION OF GOODS</th>
                <th>GROSS WEIGHT</th>
                <th>MEASUREMENT</th>
            </tr>
        """

    def _init_container_info_table(self):
        return """
        <h3>TOTAL No. OF CONTAINERS OR PACKAGES RECEIVED BY THE CARRIER</h3>
        <table class="bl-table">
            <tr>
                <th>CONTAINER NUMBERS</th>
                <th>SEAL NUMBERS</th>
                <th>SIZE</th>
                <th>TYPE</th>
            </tr>
        """

    def _init_footer_info(self):
        return f"""
        <p><strong>Freight Payable at:</strong> {self.doc['paymentDetails']['freightPayableAt']}</p>
        <p><strong>Number of Original B/Ls:</strong> {self.doc['documentationDetails']['numberOfOriginalBLs']}</p>
        <p><strong>Place of Issue:</strong> {self.doc['paymentDetails']['freightPayableAt']}</p>
        <p><strong>Date of Issue:</strong> {self.doc['additionalInformation']['onboardDate']}</p>
        """

    def _generate_container_rows(self):
        """Generates rows for the containers and particulars table."""
        def style_empty_cell(value):
            if value == '':  # If the value is empty or None
                return '<td style="background-color: #ffcccc;"></td>'  # Apply red background
            else:
                return f'<td>{value}</td>'

        for container in self.doc['containers']:
            self.particulars_html += f"""
            <tr>
                {style_empty_cell(container.get('marksAndNumbers', ''))}
                {style_empty_cell(container.get('numberOfPackages', ''))}
                {style_empty_cell(container.get('descriptionOfGoods', ''))}
                {style_empty_cell(container.get('grossWeight', ''))}
                {style_empty_cell(container.get('measurement', ''))}
            </tr>
            """
            self.container_info_html += f"""
            <tr>
                {style_empty_cell(container.get('containerNumber', ''))}
                {style_empty_cell(container.get('sealNumber', ''))}
                {style_empty_cell(container.get('containerSize', ''))}
                {style_empty_cell(container.get('containerType', ''))}
            </tr>
            """

        self.particulars_html += "</table>"
        self.container_info_html += "</table>"

    def _create_bl_html(self):
        self._generate_container_rows()  # Populating container and particulars tables before generating the full HTML

        return f"""
        <div class="bl-form">
            <div class="watermark">DRAFT</div>
            {self._create_header()}
            {self._create_shipper_consignee_info()}
            <div class="bl-section">
                {self.particulars_html}
            </div>
            <div class="bl-section">
                {self.container_info_html}
            </div>
            <div class="bl-section">
                {self.footer_info_html}
            </div>
            {self._create_footer()}
        </div>
        """

    def _create_header(self):
        return f"""
        <div class="bl-header">
            <div class="bl-title">
                <h2>BILL OF LADING (B/L)(Draft)</h2>
            </div>
            <div>
                <p class="bl-row"><strong>Booking Number:</strong> {self.doc.get('bookingReference', '')}</p>
                <p class="bl-row"><strong>Service Type:</strong> {self.doc.get('service', '')}</p>
                <p class="bl-row"><strong>B/L Number:</strong> {self.doc.get('bookingReference', '')}</p>
            </div>
            <div class="bl-logo">
                <img src="data:image/jpeg;base64,{self.logo_img}" alt="Company Logo">
            </div>
        </div>
        """

    def _create_shipper_consignee_info(self):
        shipper_info = self.doc.get('partyDetails', {}).get('shipper', {})
        consignee_info = self.doc.get('partyDetails', {}).get('consignee', {})
        notify_party_info = self.doc.get('partyDetails', {}).get('notifyParty', {})

        return f"""
        <div class="bl-section">
            <h3>SHIPPER / EXPORTER (Full Name and Address)</h3>
            <p class="bl-row">{shipper_info.get('name', '')}</p>
            <p class="bl-row">{shipper_info.get('address', '')}</p>
            <p class="bl-row">Tel: {shipper_info.get('telephone', '')}</p>
        </div>
        <div class="bl-section">
            <h3>CONSIGNEE (Full Name and Address)</h3>
            <p class="bl-row">{consignee_info.get('name', '')}</p>
            <p class="bl-row">{consignee_info.get('address', '')}</p>
            <p class="bl-row">Tel: {consignee_info.get('telephone', '')}</p>
        </div>
        <div class="bl-section">
            <h3>NOTIFY PARTY (Full Name and Address)</h3>
            <p class="bl-row">{notify_party_info.get('name', '')}</p>
            <p class="bl-row">{notify_party_info.get('address', '')}</p>
            <p class="bl-row">Tel: {notify_party_info.get('telephone', '')}</p>
        </div>
        """

    def _create_footer(self):
        return f"""
        <div class="bl-footer">
            <p class="small-text">IN WITNESS WHEREOF {self.doc['documentationDetails']['numberOfOriginalBLs']} ORIGINAL BILLS OF LADING...</p>
            <div class="bl-grid">
                <div>
                    <p class="bl-row"><strong>CHERRY SHIPPING LINE</strong></p>
                    <p class="bl-row"><strong>as Carrier</strong></p>
                    <p class="bl-row">By ContainerGenie.ai CO., LTD.</p>
                    <p>as Agents only for Carrier</p>
                </div>
                <div>
                    <p class="bl-row"><strong>Place Issued: {self.doc['paymentDetails']['freightPayableAt']}</strong></p>
                    <p class="bl-row"><strong>Date Issued: {self.doc['additionalInformation']['onboardDate']}</strong></p>
                </div>
            </div>
        </div>
        """


class BLCSS:
    def __init__(self):
        self.bl_css = """
            <style>
                @font-face {{
                    font-family: 'Freesentation';
                    src: url(data:font/ttf;base64,{font_base64}) format('truetype');
                }}

                * {{
                    font-family: 'Freesentation', sans-serif !important;
                }}

                /* 모든 선(border)에 대한 스타일 */
                * {
                    border-color: #808080 !important; /* 중간 회색 */
                }

                /* 특정 Streamlit 컴포넌트의 테두리 스타일 */
                .stTextInput, .stSelectbox, .stMultiselect, .stDateInput, .stTimeInput,
                .stNumber, .stText, .stDataFrame, .stTable {
                    border: 1px solid #808080 !important;
                }

                /* 구분선 스타일 */
                hr {
                    border-top: 1px solid #808080 !important;
                }

                /* 테이블 테두리 스타일 */
                table {
                    border-collapse: collapse;
                }
                th, td {
                    border: 1px solid #808080 !important;
                }

                /* 사이드바 구분선 스타일 */
                .stSidebar .stSidebarNav {
                    border-right-color: #808080 !important;
                }

                .bl-form {
                    border: 2px solid black;
                    padding: 5px;
                    margin-bottom: 10px;
                    width: 100%;
                    position: relative;
                }
                .bl-header {
                    display: flex;
                    justify-content: space-between;
                    align-items: flex-start;
                    border-bottom: 1px solid black;
                    padding-bottom: 5px;
                    margin-bottom: 5px;
                }
                .bl-title {
                    margin-right: 15px;
                }
                .bl-section {
                    margin-bottom: 5px;
                    border: 1px solid black;
                    padding: 2px;
                }
                .bl-grid {
                    display: grid;
                    grid-template-columns: 1fr 1fr;
                    gap: 5px;
                }
                .bl-footer {
                    border-top: 1px solid black;
                    padding-top: 5px;
                    margin-top: 5px;
                }
                .bl-logo {
                    text-align: right;
                    margin-left: auto;
                }
                .bl-logo img {
                    max-width: 150px;
                    height: auto;
                }
                .bl-table {
                    width: 100%;
                    border-collapse: collapse;
                }
                .bl-table th, .bl-table td {
                    border: 1px solid black;
                    padding: 2px;
                    text-align: left;
                }
                .small-text {
                    font-size: 10px;
                }
                .bl-row {
                    line-height: 1.0;
                    margin: 0;
                    padding: 0;
                }    
                .watermark {
                    position: absolute;
                    top: 20%;
                    left: 75%;
                    transform: translate(-50%, -50%) rotate(45deg);
                    font-size: 180px;  /* 크기를 180px로 증가 */
                    color: rgba(255, 0, 0, 0.11);  /* 투명도를 0.15로 낮춤 */
                    pointer-events: none;
                    z-index: 1000;
                    user-select: none;
                    font-weight: bold;
                    white-space: nowrap;  /* 텍스트가 줄바꿈되지 않도록 설정 */
                }
            </style>
            """
