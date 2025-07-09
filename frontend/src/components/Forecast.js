import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import { Line } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const Container = styled.div`
  min-height: calc(100vh - 40px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  border-radius: 15px;
  margin-top: 20px;
`;

const Card = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 25px;
  margin: 20px 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
`;

const PageTitle = styled.h1`
  color: white;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

const Form = styled.form`
  display: flex;
  gap: 15px;
  margin-bottom: 30px;
  align-items: center;
`;

const Input = styled.input`
  flex: 1;
  padding: 15px;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.9);
  &:focus {
    outline: none;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.3);
  }
`;

const Button = styled.button`
  padding: 15px 30px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }
`;

const ChartContainer = styled.div`
  background: white;
  border-radius: 15px;
  padding: 20px;
  margin: 20px 0;
`;

function Forecast() {
  const [location, setLocation] = useState('');
  const [forecastData, setForecastData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/forecast', { location });
      setForecastData(response.data);
    } catch (err) {
      setError('Error fetching forecast data');
    } finally {
      setLoading(false);
    }
  };

  const getChartData = () => {
    if (!forecastData) return null;

    const labels = forecastData.map(item => item.date);
    const data = forecastData.map(item => item.aqi);

    return {
      labels,
      datasets: [
        {
          label: 'Predicted AQI',
          data,
          borderColor: 'rgb(75, 192, 192)',
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          tension: 0.1,
        },
      ],
    };
  };

  const chartOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'top',
      },
      title: {
        display: true,
        text: `AQI Forecast for ${location}`,
      },
    },
    scales: {
      y: {
        beginAtZero: true,
        title: {
          display: true,
          text: 'AQI Value',
        },
      },
    },
  };

  return (
    <Container>
      <PageTitle>🌤️ AQI Forecast</PageTitle>
      
      <Card>
        <Form onSubmit={handleSubmit}>
          <Input
            type="text"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            placeholder="Enter city name"
            required
          />
          <Button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Get Forecast'}
          </Button>
        </Form>

        {error && (
          <div className="alert alert-danger">{error}</div>
        )}

        {forecastData && (
          <>
            <ChartContainer>
              <Line data={getChartData()} options={chartOptions} />
            </ChartContainer>
            
            <div>
              <h3>3-Day Forecast</h3>
              <ul>
                {forecastData.map((item, index) => (
                  <li key={index}>
                    {item.date}: AQI {item.aqi}
                  </li>
                ))}
              </ul>
            </div>
          </>
        )}
      </Card>
    </Container>
  );
}

export default Forecast;
