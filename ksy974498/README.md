## Setup

### mongo db에 json 파일 적재
```bash
python db.py ./si
python db.py ./bkg
```

### 수정사항
- `json_bkg.py`
    - html이 깨지는 현상 방지
    - `st.markdown()` 대신 `st.components.v1.html` 함수를 사용