## Setup

### mongo db에 json 파일 적재
```bash
python db.py ./si
python db.py ./bkg
```

### 기능 개발 상황
- search page
- party_list page
- llm_summary page
- report page

## 🏃 Getting Started with ContainerGenie.ai

1. Set up the environment:
   Run `poetry install --no-root`
   Run `poetry shell`
`. /Users/seongyeon/Library/Caches/pypoetry/virtualenvs/sigenie-s6yCTN5d-py3.12/bi
n/activate`
2. Configure API keys:
   - Rename `.env_sample` to `.env`
   - Open `.env` and input the required API keys:
     GOOGLE_API_KEY="YOUR_API_KEY"
     TAVILY_API_KEY="YOUR_API_KEY"
     OPENAI_API_KEY="YOUR_API_KEY"

3. Launch the application:
   Execute `streamlit run app.py`