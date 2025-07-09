import React, { useState, useEffect } from 'react';
import axios from 'axios';
import styled from 'styled-components';
import { MapContainer, TileLayer, CircleMarker, Popup, Tooltip } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

const Container = styled.div`
  min-height: calc(100vh - 40px);
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
  border-radius: 15px;
  margin-top: 20px;
`;

const Title = styled.h1`
  color: white;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2.5rem;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
`;

const Card = styled.div`
  background: rgba(255, 255, 255, 0.95);
  border-radius: 15px;
  padding: 25px;
  margin: 20px 0;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  backdrop-filter: blur(10px);
`;

const LoadMapButton = styled.button`
  padding: 15px 30px;
  background: linear-gradient(45deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-bottom: 20px;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
  }
`;

const MapWrapper = styled.div`
  height: 600px;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  margin-bottom: 20px;
`;

const Legend = styled.div`
  background: white;
  padding: 20px;
  border-radius: 15px;
  margin-top: 20px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const LegendTitle = styled.h3`
  margin-bottom: 15px;
  color: #333;
  font-size: 1.2rem;
`;

const LegendItem = styled.div`
  display: flex;
  align-items: center;
  margin: 10px 0;
  gap: 12px;
`;

const ColorDot = styled.div`
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background-color: ${props => props.color};
  border: 2px solid white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
`;

const ErrorMessage = styled.div`
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
  border: 1px solid #f5c6cb;
`;

const LoadingMessage = styled.div`
  text-align: center;
  padding: 20px;
  color: white;
  font-size: 16px;
`;

const StatsCard = styled.div`
  background: white;
  padding: 20px;
  border-radius: 15px;
  margin: 20px 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const StatsGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-top: 15px;
`;

const StatItem = styled.div`
  text-align: center;
  padding: 15px;
  background: ${props => props.color || '#f8f9fa'};
  border-radius: 10px;
  color: ${props => props.textColor || '#333'};
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 5px;
`;

const StatLabel = styled.div`
  font-size: 0.9rem;
  opacity: 0.9;
`;

function Heatmap() {
  const [mapData, setMapData] = useState(null);
  const [statistics, setStatistics] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [mapCenter, setMapCenter] = useState([20.5937, 78.9629]); // Center of India

  useEffect(() => {
    loadHeatmapData();
  }, []);

  const loadHeatmapData = async () => {
    setLoading(true);
    setError('');
    try {
      const response = await axios.get('/heatmap');
      if (response.data.heatmap_data) {
        setMapData(response.data.heatmap_data);
        setStatistics(response.data.statistics);
      } else {
        setMapData(response.data);
        setStatistics(null);
      }
    } catch (err) {
      setError('Error fetching heatmap data. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const getAQIColor = (aqi) => {
    if (aqi <= 50) return '#00e400'; // Good
    if (aqi <= 100) return '#ffff00'; // Moderate
    if (aqi <= 150) return '#ff7e00'; // Unhealthy for Sensitive Groups
    if (aqi <= 200) return '#ff0000'; // Unhealthy
    if (aqi <= 300) return '#8f3f97'; // Very Unhealthy
    return '#7e0023'; // Hazardous
  };

  const getAQICategory = (aqi) => {
    if (aqi <= 50) return 'Good';
    if (aqi <= 100) return 'Moderate';
    if (aqi <= 150) return 'Unhealthy for Sensitive Groups';
    if (aqi <= 200) return 'Unhealthy';
    if (aqi <= 300) return 'Very Unhealthy';
    return 'Hazardous';
  };

  const getHealthRecommendation = (aqi) => {
    if (aqi <= 50) return 'Air quality is good - perfect for outdoor activities';
    if (aqi <= 100) return 'Air quality is acceptable for most people';
    if (aqi <= 150) return 'Sensitive groups should limit outdoor activities';
    if (aqi <= 200) return 'Everyone should limit outdoor activities';
    if (aqi <= 300) return 'Avoid outdoor activities entirely';
    return 'Emergency conditions - stay indoors';
  };

  const getRadius = (aqi) => {
    // Dynamic radius based on AQI severity
    if (aqi <= 50) return 8;
    if (aqi <= 100) return 12;
    if (aqi <= 150) return 16;
    if (aqi <= 200) return 20;
    if (aqi <= 300) return 24;
    return 28;
  };

  const legendItems = [
    { color: '#00e400', label: '0-50: Good', range: 'Safe for everyone' },
    { color: '#ffff00', label: '51-100: Moderate', range: 'Acceptable for most' },
    { color: '#ff7e00', label: '101-150: Unhealthy for Sensitive Groups', range: 'Sensitive groups at risk' },
    { color: '#ff0000', label: '151-200: Unhealthy', range: 'Everyone at risk' },
    { color: '#8f3f97', label: '201-300: Very Unhealthy', range: 'Serious health effects' },
    { color: '#7e0023', label: '301+: Hazardous', range: 'Emergency conditions' }
  ];

  return (
    <Container>
      <Title>🗺️ Interactive AQI Heatmap</Title>
      
      {!mapData && !loading && (
        <Card>
          <LoadMapButton onClick={loadHeatmapData}>
            Load Interactive Map
          </LoadMapButton>
        </Card>
      )}

      {loading && <LoadingMessage>Loading map data...</LoadingMessage>}
      {error && <ErrorMessage>{error}</ErrorMessage>}

      {statistics && (
        <StatsCard>
          <h3>Air Quality Statistics</h3>
          <StatsGrid>
            <StatItem color="rgba(102, 126, 234, 0.1)">
              <StatValue>{statistics.total_cities}</StatValue>
              <StatLabel>Cities Monitored</StatLabel>
            </StatItem>
            <StatItem color="rgba(255, 193, 7, 0.1)">
              <StatValue>{statistics.avg_aqi}</StatValue>
              <StatLabel>Average AQI</StatLabel>
            </StatItem>
            <StatItem color="rgba(220, 53, 69, 0.1)">
              <StatValue>{statistics.max_aqi}</StatValue>
              <StatLabel>Highest AQI</StatLabel>
            </StatItem>
            <StatItem color="rgba(40, 167, 69, 0.1)">
              <StatValue>{statistics.min_aqi}</StatValue>
              <StatLabel>Lowest AQI</StatLabel>
            </StatItem>
            <StatItem color="rgba(220, 53, 69, 0.2)" textColor="#721c24">
              <StatValue>{statistics.unhealthy_cities}</StatValue>
              <StatLabel>Unhealthy Cities (AQI > 100)</StatLabel>
            </StatItem>
          </StatsGrid>
        </StatsCard>
      )}

      {mapData && (
        <Card>
          <MapWrapper>
            <MapContainer 
              center={mapCenter} 
              zoom={5} 
              style={{ height: '100%', width: '100%' }}
              scrollWheelZoom={true}
            >
              <TileLayer
                attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              />
              
              {mapData.map((city, index) => (
                <CircleMarker
                  key={index}
                  center={[city.lat, city.lng]}
                  radius={getRadius(city.aqi)}
                  pathOptions={{
                    color: 'white',
                    weight: 2,
                    opacity: 0.8,
                    fillColor: getAQIColor(city.aqi),
                    fillOpacity: 0.8
                  }}
                >
                  <Popup>
                    <div style={{ minWidth: '200px' }}>
                      <h4 style={{ margin: '0 0 10px 0', color: '#333' }}>{city.city}</h4>
                      <p style={{ margin: '5px 0', fontSize: '16px', fontWeight: 'bold' }}>
                        AQI: <span style={{ color: getAQIColor(city.aqi) }}>{city.aqi}</span>
                      </p>
                      <p style={{ margin: '5px 0', fontSize: '14px' }}>
                        Status: <strong>{getAQICategory(city.aqi)}</strong>
                      </p>
                      <p style={{ margin: '5px 0', fontSize: '12px' }}>
                        {getHealthRecommendation(city.aqi)}
                      </p>
                      <p style={{ margin: '5px 0', fontSize: '11px', color: '#666' }}>
                        Last updated: {city.date}
                      </p>
                    </div>
                  </Popup>
                  
                  <Tooltip direction="top" offset={[0, -10]} opacity={0.9}>
                    <div style={{ textAlign: 'center' }}>
                      <strong>{city.city}</strong><br/>
                      AQI: {city.aqi}<br/>
                      {getAQICategory(city.aqi)}
                    </div>
                  </Tooltip>
                </CircleMarker>
              ))}
            </MapContainer>
          </MapWrapper>

          <Legend>
            <LegendTitle>AQI Color Legend</LegendTitle>
            {legendItems.map((item, index) => (
              <LegendItem key={index}>
                <ColorDot color={item.color} />
                <div>
                  <strong>{item.label}</strong>
                  <div style={{ fontSize: '12px', color: '#666' }}>{item.range}</div>
                </div>
              </LegendItem>
            ))}
          </Legend>
        </Card>
      )}
    </Container>
  );
}

export default Heatmap;
