import React, { useState } from 'react';
import ChatStream from './ChatStream';
import './App.css';
import axios from 'axios';
import { Tab, Tabs, TabList, TabPanel } from 'react-tabs';
import 'react-tabs/style/react-tabs.css';

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
  );
}

export default App;
