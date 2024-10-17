import React, { useState } from 'react';
import axios from 'axios';
import './App.css';  // CSS 파일 불러오기

function App() {
  const [bookingReference, setBookingReference] = useState('');
  const [processStarted, setProcessStarted] = useState(false);
  const [stepResult, setStepResult] = useState('');
  const [activeTab, setActiveTab] = useState('get_bkg');

  const steps = ['get_bkg', 'get_si', 'check_missing_data', 'generate_intake_report'];

  // 탭 클릭 시 활성화되는 탭 설정 및 API 호출
  const handleTabClick = async (tab) => {
    setActiveTab(tab);

    try {
      const response = await axios.post(`http://127.0.0.1:8000/step/${tab}`, { booking_reference: bookingReference });
      if (response && response.data) {
        setStepResult(response.data);
      } else {
        setStepResult("Error: No data returned from server");
      }
    } catch (error) {
      if (error.response) {
        setStepResult(`Error: ${error.response.data.detail}`);
      } else if (error.request) {
        setStepResult("Error: No response from server");
      } else {
        setStepResult(`Error: ${error.message}`);
      }
    }
  };

  const handleStartProcess = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/start_process/', { booking_reference: bookingReference });
      if (response && response.data) {
        setProcessStarted(true);
        setStepResult(response.data.message);
      } else {
        setStepResult("Error: No data returned from server");
      }
    } catch (error) {
      if (error.response) {
        setStepResult(`Error: ${error.response.data.detail}`);
      } else if (error.request) {
        setStepResult("Error: No response from server");
      } else {
        setStepResult(`Error: ${error.message}`);
      }
    }
  };

  return (
    <div className="App">
      <h1>SI Intake Process</h1>
      <input
        type="text"
        value={bookingReference}
        onChange={(e) => setBookingReference(e.target.value)}
        placeholder="Enter Booking Reference"
      />
      <button onClick={handleStartProcess} disabled={!bookingReference}>Start Process</button>

      {processStarted && (
        <div className="tabs">
          {steps.map((step) => (
            <button
              key={step}
              className={`tab-button ${activeTab === step ? 'active' : ''}`}
              onClick={() => handleTabClick(step)}
            >
              {step.replace('_', ' ')}
            </button>
          ))}
        </div>
      )}

      {stepResult && (
        <div className="tab-content">
          <p>{JSON.stringify(stepResult)}</p>
        </div>
      )}
    </div>
  );
}

export default App;
