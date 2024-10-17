import React, { useState } from 'react';
import ChatStream from './ChatStream';
import './App.css';
import axios from 'axios';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

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

// function App() {
//   return (
//     <div className="main-content">
//       <div className="search-bar">
//         <input type="text" placeholder="Text me your episode for SIGenie Story." />
//         <button>🔍</button>
//       </div>
//       <div className="sections">
//         <Section
//           title="선적지시서 접수"
//           items={[
//             "JSON 형식 Booking Data 조회",
//             "JSON 형식 Shipping Instruction 조회",
//             "LLM을 활용한 누락 데이터 식별",
//             "Shipping Instruction 접수 보고서 생성"
//           ]}
//         />
//         <Section
//           title="선적지시서 검증"
//           items={[
//             "LLM을 활용한 관련 당사자 정보 확인",
//             "RAG 활용한 회사 정책 준수 여부 검증",
//             "실시간 선박 및 항구 상황 확인",
//             "선적 지시서 최종 검증 보고서 생성"
//           ]}
//         />
//       </div>
//     </div>
//   );
// }

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
  const [query, setQuery] = useState('');
  const [workflow, setWorkflow] = useState('ch1');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [tabData, setTabData] = useState({
    get_si: '',
    check_missing_data: '',
    generate_intake_report: '',
    check_parties: '',
    verify_company_policy: '',
    verify_vessel_port_situation: '',
    generate_validation_report: '',
  });

  const handleWorkflowChange = (e) => setWorkflow(e.target.value);
  const handleInputChange = (e) => setQuery(e.target.value);
  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!query.trim()) return; // Avoid empty queries
    setLoading(true);
    setError(null); // Reset error before making request
    try {
      const response = await axios.get(`http://127.0.0.1:8000/streaming_sync/chat/${workflow}`, {
        params: { query: encodeURIComponent(query) }
      });
      setTabData({
        get_si: response.data.get_si || 'No data available for get_si',
        check_missing_data: response.data.check_missing_data || 'No data available for check_missing_data',
        generate_intake_report: response.data.generate_intake_report || 'No data available for generate_intake_report',
        check_parties: response.data.check_parties || 'No data available for check_parties',
        verify_company_policy: response.data.verify_company_policy || 'No data available for verify_company_policy',
        verify_vessel_port_situation: response.data.verify_vessel_port_situation || 'No data available for verify_vessel_port_situation',
        generate_validation_report: response.data.generate_validation_report || 'No data available for generate_validation_report',
      });
    } catch (error) {
      // Catch network issues or server errors
      if (error.response) {
        setError(`Server Error: ${error.response.data.detail || error.message}`);
      } else {
        setError(`Network Error: ${error.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <Sidebar />
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
      <div className="shipment-query-section">
        <h1>Shipment Workflow Query</h1>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="query">Enter your query:</label>
            <input
              type="text"
              id="query"
              value={query}
              onChange={handleInputChange}
              placeholder="Enter shipment or policy query..."
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="workflow">Select Workflow:</label>
            <select id="workflow" value={workflow} onChange={handleWorkflowChange}>
              <option value="ch1">Workflow CH1</option>
              <option value="ch2">Workflow CH2</option>
            </select>
          </div>
          <button type="submit" className="submit-btn" disabled={loading}>
            {loading ? 'Processing...' : 'Submit'}
          </button>
        </form>
        {loading && <div className="spinner">Loading...</div>}
        {error && <div className="error">{error}</div>}
        <Tabs>
          <TabList>
            {workflow === 'ch1' ? (
              <>
                <Tab>Get SI</Tab>
                <Tab>Check Missing Data</Tab>
                <Tab>Generate Intake Report</Tab>
              </>
            ) : (
              <>
                <Tab>Check Parties</Tab>
                <Tab>Verify Company Policy</Tab>
                <Tab>Verify Vessel/Port Situation</Tab>
                <Tab>Generate Validation Report</Tab>
              </>
            )}
          </TabList>
          {workflow === 'ch1' ? (
            <>
              <TabPanel>
                <h2>Get SI Data</h2>
                <p>{tabData.get_si}</p>
              </TabPanel>
              <TabPanel>
                <h2>Check Missing Data</h2>
                <p>{tabData.check_missing_data}</p>
              </TabPanel>
              <TabPanel>
                <h2>Generate Intake Report</h2>
                <p>{tabData.generate_intake_report}</p>
              </TabPanel>
            </>
          ) : (
            <>
              <TabPanel>
                <h2>Check Parties</h2>
                <p>{tabData.check_parties}</p>
              </TabPanel>
              <TabPanel>
                <h2>Verify Company Policy</h2>
                <p>{tabData.verify_company_policy}</p>
              </TabPanel>
              <TabPanel>
                <h2>Verify Vessel/Port Situation</h2>
                <p>{tabData.verify_vessel_port_situation}</p>
              </TabPanel>
              <TabPanel>
                <h2>Generate Validation Report</h2>
                <p>{tabData.generate_validation_report}</p>
              </TabPanel>
            </>
          )}
        </Tabs>
        {/* Streaming component */}
        <ChatStream workflow={workflow} query={query} />
      </div>
    </div>
  );
}

export default App;