import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

const App = () => {
  const [bookingReference, setBookingReference] = useState('');
  const [processStarted, setProcessStarted] = useState(false);
  const [stepResult, setStepResult] = useState(null);

  const handleStartProcess = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/start_process/', { booking_reference: bookingReference });
      setProcessStarted(true);
      setStepResult(response.data.message);
    } catch (error) {
      setStepResult(`Error: ${error.response.data.detail}`);
    }
  };

  const handleStep = async (stepName) => {
    try {
      const response = await axios.post(`http://127.0.0.1:8000/step/${stepName}`, { booking_reference: bookingReference });
      setStepResult(response.data);
    } catch (error) {
      setStepResult(`Error: ${error.response.data.detail}`);
    }
  };

  const handleFinishProcess = async () => {
    try {
      const response = await axios.post('http://127.0.0.1:8000/finish_process/', { booking_reference: bookingReference });
      setProcessStarted(false);
      setStepResult(response.data.message);
      setBookingReference('');
    } catch (error) {
      setStepResult(`Error: ${error.response.data.detail}`);
    }
  };

  return (
    <div className="app">
      <h1>SI Intake Process</h1>
      
      <div>
        <label>Booking Reference: </label>
        <input
          type="text"
          value={bookingReference}
          onChange={(e) => setBookingReference(e.target.value)}
          placeholder="Enter booking reference"
          disabled={processStarted}
        />
      </div>

      {!processStarted ? (
        <button onClick={handleStartProcess}>Start Process</button>
      ) : (
        <div>
          <h3>Run Steps:</h3>
          <button onClick={() => handleStep('get_bkg')}>Get BKG</button>
          <button onClick={() => handleStep('get_si')}>Get SI</button>
          <button onClick={() => handleStep('check_missing_data')}>Check Missing Data</button>
          <button onClick={() => handleStep('generate_intake_report')}>Generate Intake Report</button>
          <br />
          <button onClick={handleFinishProcess}>Finish Process</button>
        </div>
      )}

      {stepResult && (
        <div className="result">
          <h3>Result:</h3>
          <pre>{JSON.stringify(stepResult, null, 2)}</pre>
        </div>
      )}
    </div>
  );
};

export default App;
