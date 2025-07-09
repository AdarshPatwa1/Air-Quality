import React, { useState } from 'react';
import axios from 'axios';
import styled, { createGlobalStyle } from 'styled-components';

const GlobalStyle = createGlobalStyle`
  body {
    margin: 0;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    background-color: ${({ aqi }) => 
      aqi <= 50 ? '#00e400' :
      aqi <= 100 ? '#ffff00' :
      aqi <= 150 ? '#ff7e00' :
      aqi <= 200 ? '#ff0000' :
      aqi <= 300 ? '#8f3f97' : '#7e0023'};
    transition: background-color 0.5s ease;
  }
`;

const Container = styled.div`
  padding: 20px;
  max-width: 800px;
  margin: 20px auto;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 15px;
  backdrop-filter: blur(10px);
`;

const Card = styled.div`
  background: white;
  border-radius: 15px;
  padding: 25px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
`;

const Input = styled.input`
  padding: 10px;
  font-size: 16px;
  width: calc(100% - 22px);
  margin-bottom: 15px;
  border-radius: 5px;
  border: 1px solid #ccc;
`;

const Button = styled.button`
  padding: 10px 20px;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  background-color: #007bff;
  color: white;
  cursor: pointer;
  margin-bottom: 20px;
  &:hover {
    background-color: #0056b3;
  }
`;

const Error = styled.p`
  color: red;
`;

const Title = styled.h1`
  color: white;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

function HomePage() {
  const [location, setLocation] = useState('');
  const [aqiData, setAqiData] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const fetchAQI = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.post('/aqi', { location });
      setAqiData(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('Error fetching AQI data');
      }
    }
    setLoading(false);
  };

  return (
    <>
      <GlobalStyle aqi={aqiData ? (aqiData.aqi || aqiData.AQI || 0) : 0} />
      <Container>
        <Title>🌬️ Air Quality Dashboard</Title>

        <Input 
          type="text" 
          value={location}
          onChange={(e) => setLocation(e.target.value)}
          placeholder="Enter city"
        />

        <Button onClick={fetchAQI}>Get AQI</Button>

        {loading && <p>Loading...</p>}

        {aqiData && (
          <Card>
            <h2>AQI for {location}</h2>
            <p>Overall AQI: {aqiData.aqi || aqiData.AQI}</p>
            <h3>Health Recommendations:</h3>
            <p>{getHealthRecommendations(aqiData.aqi || aqiData.AQI)}</p>
          </Card>
        )}

        {error && <Error>{error}</Error>}
      </Container>
    </>
  );
}

const getHealthRecommendations = (aqi) => {
  if (aqi <= 50) return "Air quality is considered satisfactory, and air pollution poses little or no risk.";
  if (aqi <= 100) return "Air quality is acceptable; however, there may be a moderate health concern for a very small number of people.";
  if (aqi <= 150) return "Members of sensitive groups may experience health effects. The general public is not likely to be affected.";
  if (aqi <= 200) return "Everyone may begin to experience health effects; members of sensitive groups may experience more serious health effects.";
  if (aqi <= 300) return "Health alert: everyone may experience more serious health effects.";
  return "Health warnings of emergency conditions. The entire population is more likely to be affected.";
};

export default HomePage;
