# 🚢 SiGenie.ai
- LangChain, RAG, and Intelligent Agent.

## What is SI?
- SI : Shipping Instruction


## WorkFlow
### **chapter 1**

1. 예약서, si 조회 
2. si에서 빠진 부분 없는지 확인
3. 확인한 결과 정리해서 보여주기

### **chapter 2**

1. si 조회
2. parties 확인 (수정할 사항 표시)
    - Validation 항목
        - Mandatory Mark
        - Address Logic & Standard Address
3. 정책 확인
    - comliance with company policies
4. 실시간 데이터 확인
5. 확인한 결과 정리해서 보여주기

## 디렉토리 구조
```
.  
├── aiffel_gru : 그루 개인 폴더   
│   ├── daehyeon_ko  
│   ├── hail_ro  
│   ├── isbyeon  
│   ├── ksy974498  
│   └── nakyoung_kim   
├── dongyang_systems : 동양시스템즈   
│   ├── frontend  
│   └── sigenie  
├── **main**  : final version   
│   ├── frontend  
│   └── backend  
└── **st_si_validation_story**  : streamlit version app   
```