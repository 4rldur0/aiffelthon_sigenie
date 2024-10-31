import streamlit as st
import base64
from .STYLES.bl_styles import BLHTML, BLCSS

# 현재 SI를 기반으로 draft B/L을 보여주는 페이지
class BLDraftPage:
    def __init__(self, si_data):
        self.si_data = si_data
        logo_img_path = "./layouts/imgs/containergenie.png"
        logo_img = self._get_base64_encoded_image(logo_img_path)

        self.bl_html = BLHTML(si_data, logo_img).bl_html
        self.bl_css = BLCSS().bl_css

    # 로고 이미지 가져오기 및 출력 형식 지정
    def _get_base64_encoded_image(self, image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')

    # 화면에 보여질 실제 페이지
    def show_bl_draft_page(self):
        st.title("Bill of Lading Report Draft")
        if self.si_data:
            # Apply custom CSS
            st.markdown(self.bl_css, unsafe_allow_html=True)        
            # Render the BL form
            st.html(self.bl_html)
        else:
            st.warning("Please search for a Shipping Instruction first.")

# 최종 요약 텍스트를 보여주는 페이지
class IntakeReportPage:
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

class ValReportPage:
    def __init__(self, report_name, text):
        self.report_name = report_name
        self.text = text

    # 최종 report를 스트리밍 형식으로 보여줌(실제 답변이 스트리밍되는 것은 아님)
    def generate_report(self, placeholder, text):
        try:
            streamed_text = ''
            for chunk in text:
                if chunk is not None:
                    streamed_text += chunk
                    placeholder.info(streamed_text)
        except Exception as e:
            st.error(f"An error occurred while generating the summary: {e}")

    # 화면에 보여질 실제 페이지        
    def show_report_page(self):
        st.title(self.report_name)
        placeholder = st.empty()
        self.generate_report(placeholder, self.text)