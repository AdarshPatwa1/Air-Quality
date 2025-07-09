import React, { useState } from 'react';
import axios from 'axios';
import styled from 'styled-components';

const Container = styled.div`
  min-height: calc(100vh - 40px);
  background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
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

const Form = styled.form`
  display: grid;
  gap: 20px;
  margin-bottom: 30px;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
`;

const Label = styled.label`
  margin-bottom: 8px;
  font-weight: 600;
  color: #333;
`;

const Input = styled.input`
  padding: 15px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.9);
  
  &:focus {
    outline: none;
    border-color: #11998e;
    box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1);
  }
`;

const Select = styled.select`
  padding: 15px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 10px;
  font-size: 16px;
  background: rgba(255, 255, 255, 0.9);
  
  &:focus {
    outline: none;
    border-color: #11998e;
    box-shadow: 0 0 0 3px rgba(17, 153, 142, 0.1);
  }
`;

const CheckboxGroup = styled.div`
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-top: 10px;
`;

const CheckboxLabel = styled.label`
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: normal;
  cursor: pointer;
`;

const Button = styled.button`
  padding: 15px 30px;
  background: linear-gradient(45deg, #11998e, #38ef7d);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(17, 153, 142, 0.4);
  }
`;

const RecommendationCard = styled.div`
  background: ${props => props.color || '#f8f9fa'};
  color: white;
  padding: 20px;
  border-radius: 15px;
  margin: 20px 0;
`;

const RecommendationList = styled.ul`
  list-style: none;
  padding: 0;
  
  li {
    margin: 10px 0;
    padding: 10px;
    background: rgba(255, 255, 255, 0.2);
    border-radius: 8px;
  }
`;

function HealthAlerts() {
  const [formData, setFormData] = useState({
    location: '',
    age_group: '',
    health_conditions: []
  });
  const [recommendations, setRecommendations] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleCheckboxChange = (e) => {
    const { value, checked } = e.target;
    setFormData(prev => ({
      ...prev,
      health_conditions: checked 
        ? [...prev.health_conditions, value]
        : prev.health_conditions.filter(item => item !== value)
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const response = await axios.post('/health_alerts', formData);
      setRecommendations(response.data);
    } catch (err) {
      if (err.response && err.response.data && err.response.data.error) {
        setError(err.response.data.error);
      } else {
        setError('Error fetching health recommendations');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container>
      <Title>🏥 Personalized Health Alerts</Title>
      
      <Card>
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="location">Location:</Label>
            <Input
              type="text"
              id="location"
              name="location"
              value={formData.location}
              onChange={handleInputChange}
              placeholder="Enter city name"
              required
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="age_group">Age Group:</Label>
            <Select
              id="age_group"
              name="age_group"
              value={formData.age_group}
              onChange={handleInputChange}
            >
              <option value="">Select age group</option>
              <option value="child">Child (0-12)</option>
              <option value="teen">Teen (13-19)</option>
              <option value="adult">Adult (20-64)</option>
              <option value="elderly">Elderly (65+)</option>
              <option value="pregnant">Pregnant</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label>Health Conditions (check all that apply):</Label>
            <CheckboxGroup>
              {['asthma', 'copd', 'heart_disease', 'diabetes', 'allergies'].map(condition => (
                <CheckboxLabel key={condition}>
                  <input
                    type="checkbox"
                    value={condition}
                    checked={formData.health_conditions.includes(condition)}
                    onChange={handleCheckboxChange}
                  />
                  {condition.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </CheckboxLabel>
              ))}
            </CheckboxGroup>
          </FormGroup>

          <Button type="submit" disabled={loading}>
            {loading ? 'Loading...' : 'Get Personalized Recommendations'}
          </Button>
        </Form>

        {error && (
          <div className="alert alert-danger">{error}</div>
        )}

        {recommendations && (
          <RecommendationCard color={recommendations.recommendations.color}>
            <h2>Air Quality Status for {formData.location}</h2>
            <h3>AQI: {recommendations.aqi.aqi} - {recommendations.recommendations.category}</h3>
            
            <div>
              <h3>Personalized Recommendations:</h3>
              <RecommendationList>
                {recommendations.recommendations.recommendations.map((rec, index) => (
                  <li key={index}>{rec}</li>
                ))}
              </RecommendationList>
            </div>
            
            {recommendations.alert_message && (
              <div style={{ marginTop: '20px', padding: '15px', backgroundColor: 'rgba(255, 255, 255, 0.2)', borderRadius: '8px' }}>
                <h4>Alert: {recommendations.alert_message.level}</h4>
                <p>{recommendations.alert_message.message}</p>
              </div>
            )}
          </RecommendationCard>
        )}
      </Card>
    </Container>
  );
}

export default HealthAlerts;
