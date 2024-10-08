import streamlit as st
import base64
import pandas as pd

# 현재 SI를 기반으로 draft B/L을 보여주는 페이지

class BLDraftPage:
    def __init__(self, si_data):
        self.si_data = si_data
        self.logo_img = "./layouts/imgs/containergenie.png"

    # 로고 이미지 가져오기 및 출력 형식 지정
    def _get_base64_encoded_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    def _generate_container_rows(self, containers, doc):
            
        particulars_html = f"""
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

        container_info_html = f"""
        <h3>TOTAL No. OF CONTAINERS OR PACKAGES RECEIVED BY THE CARRIER</h3>
        <table class="bl-table">
            <tr>
                <th>CONTAINER NUMBERS</th>
                <th>SEAL NUMBERS</th>
                <th>SIZE</th>
                <th>TYPE</th>
            </tr>
        """

        footer_info_html = f"""
        <p><strong>Freight Payable at:</strong> {doc['paymentDetails']['freightPayableAt']}</p>
        <p><strong>Number of Original B/Ls:</strong> {doc['documentationDetails']['numberOfOriginalBLs']}</p>
        <p><strong>Place of Issue:</strong> {doc['paymentDetails']['freightPayableAt']}</p>
        <p><strong>Date of Issue:</strong> {doc['additionalInformation']['onboardDate']}</p>
        """
        def style_empty_cell(value):
            if value == '':  # If the value is empty or None
                return '<td style="background-color: #ffcccc;"></td>'  # Apply red background
            else:
                return f'<td>{value}</td>'
            
        for container in containers:
            particulars_html += f"""
            <tr>
                {style_empty_cell(container.get('marksAndNumbers', ''))}
                {style_empty_cell(container.get('numberOfPackages', ''))}
                {style_empty_cell(container.get('descriptionOfGoods', ''))}
                {style_empty_cell(container.get('grossWeight', ''))}
                {style_empty_cell(container.get('measurement', ''))}
            </tr>
            """
            container_info_html += f"""
            <tr>
                {style_empty_cell(container.get('containerNumber', ''))}
                {style_empty_cell(container.get('sealNumber', ''))}
                {style_empty_cell(container.get('containerSize', ''))}
                {style_empty_cell(container.get('containerType', ''))}
            </tr>
                """

        particulars_html += "</table>"
        container_info_html += "</table>"

        return particulars_html, container_info_html, footer_info_html


    def _display_bl_form(self, doc):
        # Apply custom CSS
        from .TEMPLATES.bl_css import custom_css

        st.markdown(custom_css, unsafe_allow_html=True)
        
        # Load and encode the logo
        logo_base64 = self._get_base64_encoded_image(self.logo_img)
        
        # Generate container information HTML
        particulars_html, container_info_html, footer_info_html = self._generate_container_rows(doc['containers'], doc)

        # Create the BL form HTML
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
        
        # Render the BL form
        st.html(bl_html)


    # 화면에 보여질 실제 페이지
    def show_bl_draft_page(self):
        st.title("Bill of Lading Report Draft")
        
        if self.si_data:
            self._display_bl_form(self.si_data)
        else:
            st.warning("Please search for a Shipping Instruction first.")

# 최종 요약 텍스트를 보여주는 페이지
class ReportPage:
    def __init__(self, report_name, missing_answer, summary_answer):
        self.report_name = report_name
        self.missing_answer = missing_answer
        self.summary_answer = summary_answer
    
        # 색상을 적용하여 상태를 출력하는 함수
    def color_status(self, status):
        if status == "OK":
            return '<span style="color:blue">OK</span>'
        elif status == "Missing":
            return '<span style="color:red">Missing</span>'
        elif status == "Warning":
            return '<span style="color:orange">Warning</span>'
        return status

    def generate_report(self):
        try:
            overall_status = self.summary_answer.get('overall_status', 'N/A')
            issues_found = self.summary_answer.get('issues_found', 'N/A')
            missing_summary = self.summary_answer.get('missing_summary', 'N/A')
            conclusion = self.summary_answer.get('conclusion', 'N/A')

            # HTML을 활용하여 상태에 따라 색상 적용
            overall_status_colored = self.color_status(overall_status)

            # 화면에 보고서 내용을 표시
            st.markdown(f"### Overall Status: **{overall_status_colored}**", unsafe_allow_html=True)
            
            st.subheader("Issues Found:")
            st.markdown(issues_found)

            st.subheader("Summary of Missing or Incomplete Information:")
            st.markdown(missing_summary)

            st.subheader("Conclusion:")
            st.markdown(conclusion)

        except Exception as e:
            st.error(f"An error occurred while generating the summary: {e}")

    def generate_missing_report(self):
        try:
            st.subheader("Missing Data - Total Status Overview")
            for key, value in self.missing_answer.items():
                # total_status가 없으면 기본값 "N/A"로 처리
                if key == 'total_status':
                    pass
                elif isinstance(value, dict):
                    total_status = value.get("total_status", "N/A")
                    total_status_colored = self.color_status(total_status)
                    st.markdown(f"- **{key}:** {total_status_colored}", unsafe_allow_html=True)
                else:
                    # value가 dict가 아닐 경우에도 처리
                    st.markdown(f"- **{key}:** N/A", unsafe_allow_html=True)
        except Exception as e:
            st.error(f"An error occurred while generating the missing data report: {e}")



    # 화면에 보여질 실제 페이지
    def show_report_page(self):
        st.title(self.report_name)
        self.generate_report()
        self.generate_missing_report()