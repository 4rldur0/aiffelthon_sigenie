import base64

def get_base64_encoded_font(font_path):
    with open(font_path, "rb") as font_file:
        return base64.b64encode(font_file.read()).decode('utf-8')

def get_custom_font_css():
    font_base64 = get_base64_encoded_font("./fonts/Freesentation.ttf")
    return f"""
    <style>
    @font-face {{
        font-family: 'Freesentation';
        src: url(data:font/ttf;base64,{font_base64}) format('truetype');
    }}

    * {{
        font-family: 'Freesentation', sans-serif !important;
    }}
    </style>
    """