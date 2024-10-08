custom_css = """
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