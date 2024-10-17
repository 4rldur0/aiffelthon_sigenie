import React from 'react';
import './App.css'; // Assuming you're adding some custom styles

function Sidebar() {
  return (
    <div className="sidebar">
      <h3>Within 7 days</h3>
      <Message id="bkg_202410013432" />
      <h3>Last 7 days</h3>
      <Message id="bkg_202410013432" />
      <Message id="bkg_202410013432" />
    </div>
  );
}

function Message({ id }) {
  return (
    <div className="message">
      <span role="img" aria-label="message">💬</span> {id}
    </div>
  );
}

function MainContent() {
  return (
    <div className="main-content">
      <div className="search-bar">
        <input type="text" placeholder="Text me your episode for SIGenie Story." />
        <button>🔍</button>
      </div>
      <div className="sections">
        <Section
          title="선적지시서 접수"
          items={[
            "JSON 형식 Booking Data 조회",
            "JSON 형식 Shipping Instruction 조회",
            "LLM을 활용한 누락 데이터 식별",
            "Shipping Instruction 접수 보고서 생성"
          ]}
        />
        <Section
          title="선적지시서 검증"
          items={[
            "LLM을 활용한 관련 당사자 정보 확인",
            "RAG 활용한 회사 정책 준수 여부 검증",
            "실시간 선박 및 항구 상황 확인",
            "선적 지시서 최종 검증 보고서 생성"
          ]}
        />
      </div>
    </div>
  );
}

function Section({ title, items }) {
  return (
    <div className="section">
      <h4>{title}</h4>
      <ul>
        {items.map((item, index) => (
          <li key={index}>{item}</li>
        ))}
      </ul>
    </div>
  );
}

function App() {
  return (
    <div className="app">
      <Sidebar />
      <MainContent />
    </div>
  );
}

export default App;