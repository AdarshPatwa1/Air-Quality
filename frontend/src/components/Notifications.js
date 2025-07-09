import React, { useState, useEffect } from 'react';
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

const ActionButton = styled.button`
  padding: 10px 20px;
  margin-right: 10px;
  background: #ff9800;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  
  &:hover {
    background: #e68900;
    transform: translateY(-1px);
  }
`;

const UnsubscribeButton = styled(ActionButton)`
  background: #f44336;
  
  &:hover {
    background: #d32f2f;
  }
`;

const ErrorMessage = styled.div`
  background: #f8d7da;
  color: #721c24;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
  border: 1px solid #f5c6cb;
`;

const SuccessMessage = styled.div`
  background: #d4edda;
  color: #155724;
  padding: 15px;
  border-radius: 10px;
  margin: 20px 0;
  border: 1px solid #c3e6cb;
`;

const SubscriptionList = styled.ul`
  list-style: none;
  padding: 0;
  
  li {
    margin: 15px 0;
    background: #fff;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
`;

const SubscriptionInfo = styled.div`
  h4 {
    margin: 0 0 8px 0;
    color: #333;
  }
  
  p {
    margin: 4px 0;
    color: #666;
    font-size: 14px;
  }
`;

const AlertPopup = styled.div`
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  z-index: 1000;
  max-width: 500px;
  width: 90%;
`;

const AlertOverlay = styled.div`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 999;
`;

function Notifications() {
  const [form, setForm] = useState({
    location: '',
    threshold: 100,
    age_group: '',
    health_conditions: []
  });
  const [subscriptions, setSubscriptions] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [alertPopup, setAlertPopup] = useState(null);

  // Load existing subscriptions on component mount
  useEffect(() => {
    loadSubscriptions();
  }, []);

  const loadSubscriptions = async () => {
    try {
      const response = await axios.get('/subscriptions');
      if (response.data && response.data.subscriptions) {
        const subs = Object.entries(response.data.subscriptions).map(([user_id, sub]) => ({
          user_id,
          ...sub
        }));
        setSubscriptions(subs);
      }
    } catch (err) {
      console.error('Failed to load subscriptions:', err);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    
    try {
      const response = await axios.post('/notifications', {
        action: 'subscribe',
        ...form
      });
      
      if (response.data) {
        const newSubscription = {
          user_id: response.data.user_id,
          location: response.data.location,
          threshold: response.data.threshold,
          age_group: response.data.age_group,
          health_conditions: response.data.health_conditions
        };
        setSubscriptions([...subscriptions, newSubscription]);
        setSuccess(`Successfully subscribed to alerts for ${response.data.location}`);
        setForm({
          location: '',
          threshold: 100,
          age_group: '',
          health_conditions: []
        });
      }
    } catch (err) {
      setError('Failed to subscribe. Please try again.');
    }
  };

  const handleUnsubscribe = async (userId) => {
    try {
      const response = await axios.post('/notifications', {
        action: 'unsubscribe',
        user_id: userId
      });
      
      if (response.data) {
        // Remove from local state
        setSubscriptions(subscriptions.filter(sub => sub.user_id !== userId));
        setSuccess('Successfully unsubscribed from alerts');
        
        // Reload subscriptions to ensure sync
        await loadSubscriptions();
      }
    } catch (err) {
      setError('Failed to unsubscribe. Please try again.');
      console.error('Unsubscribe error:', err);
    }
  };

  const handleTest = async (subscription) => {
    try {
      const response = await axios.post('/notifications', {
        action: 'test',
        user_id: subscription.user_id,
        location: subscription.location,
        threshold: subscription.threshold
      });
      
      if (response.data) {
        setAlertPopup({
          location: subscription.location,
          threshold: subscription.threshold,
          currentAQI: response.data.current_aqi || 'Unknown',
          message: response.data.message || 'Test alert generated',
          level: response.data.level || 'INFO'
        });
      }
    } catch (err) {
      setError('Failed to test alert. Please try again.');
    }
  };

  const handleCheckboxChange = (condition) => {
    const updatedConditions = form.health_conditions.includes(condition)
      ? form.health_conditions.filter(c => c !== condition)
      : [...form.health_conditions, condition];
    
    setForm({ ...form, health_conditions: updatedConditions });
  };

  const closeAlert = () => {
    setAlertPopup(null);
  };

  return (
    <Container>
      <Title>🔔 Push Alert Subscriptions</Title>

      {error && <ErrorMessage>{error}</ErrorMessage>}
      {success && <SuccessMessage>{success}</SuccessMessage>}

      <Card>
        <h3>Subscribe to AQI Alerts</h3>
        <Form onSubmit={handleSubmit}>
          <FormGroup>
            <Label htmlFor="location">City Name:</Label>
            <Input
              type="text"
              id="location"
              name="location"
              value={form.location}
              onChange={(e) => setForm({ ...form, location: e.target.value })}
              placeholder="Enter city name"
              required
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="threshold">AQI Threshold:</Label>
            <Input
              type="number"
              id="threshold"
              name="threshold"
              value={form.threshold}
              onChange={(e) => setForm({ ...form, threshold: parseInt(e.target.value) })}
              placeholder="e.g. 150"
              min="0"
              max="500"
              required
            />
          </FormGroup>

          <FormGroup>
            <Label htmlFor="age_group">Age Group:</Label>
            <Select
              id="age_group"
              name="age_group"
              value={form.age_group}
              onChange={(e) => setForm({ ...form, age_group: e.target.value })}
            >
              <option value="">Select age group</option>
              <option value="child">Child (0-12)</option>
              <option value="teen">Teen (13-19)</option>
              <option value="adult">Adult (20-64)</option>
              <option value="elderly">Elderly (65+)</option>
            </Select>
          </FormGroup>

          <FormGroup>
            <Label>Health Conditions:</Label>
            <CheckboxGroup>
              {['asthma', 'allergies', 'heart_disease', 'copd', 'diabetes'].map(condition => (
                <CheckboxLabel key={condition}>
                  <input
                    type="checkbox"
                    checked={form.health_conditions.includes(condition)}
                    onChange={() => handleCheckboxChange(condition)}
                  />
                  {condition.replace('_', ' ').replace(/\b\w/g, l => l.toUpperCase())}
                </CheckboxLabel>
              ))}
            </CheckboxGroup>
          </FormGroup>

          <Button type="submit">Subscribe to Alerts</Button>
        </Form>
      </Card>

      {subscriptions.length > 0 && (
        <Card>
          <h3>Active Subscriptions</h3>
          <SubscriptionList>
            {subscriptions.map(subscription => (
              <li key={subscription.user_id}>
                <SubscriptionInfo>
                  <h4>{subscription.location}</h4>
                  <p>AQI Threshold: {subscription.threshold}</p>
                  <p>Age Group: {subscription.age_group || 'Not specified'}</p>
                  <p>Health Conditions: {subscription.health_conditions.join(', ') || 'None'}</p>
                </SubscriptionInfo>
                <div>
                  <ActionButton onClick={() => handleTest(subscription)}>
                    Test Alert
                  </ActionButton>
                  <UnsubscribeButton onClick={() => handleUnsubscribe(subscription.user_id)}>
                    Unsubscribe
                  </UnsubscribeButton>
                </div>
              </li>
            ))}
          </SubscriptionList>
        </Card>
      )}

      {alertPopup && (
        <>
          <AlertOverlay onClick={closeAlert} />
          <AlertPopup>
            <h3 style={{ 
              color: alertPopup.level === 'ALERT' ? '#d32f2f' : 
                     alertPopup.level === 'WARNING' ? '#ff9800' : '#4caf50',
              marginBottom: '20px'
            }}>
              🚨 Alert Test Result
            </h3>
            
            <div style={{ marginBottom: '20px' }}>
              <div style={{ marginBottom: '10px' }}>
                <strong>📍 Location:</strong> {alertPopup.location}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>⚠️ Your Threshold:</strong> {alertPopup.threshold}
              </div>
              <div style={{ marginBottom: '10px' }}>
                <strong>🌬️ Current AQI:</strong> 
                <span style={{ 
                  color: alertPopup.currentAQI > alertPopup.threshold ? '#d32f2f' : '#4caf50',
                  fontWeight: 'bold',
                  marginLeft: '8px'
                }}>
                  {alertPopup.currentAQI}
                </span>
              </div>
            </div>
            
            <div style={{ 
              background: alertPopup.level === 'ALERT' ? '#ffebee' : 
                         alertPopup.level === 'WARNING' ? '#fff3e0' : '#e8f5e8',
              padding: '20px',
              borderRadius: '12px',
              margin: '20px 0',
              borderLeft: `4px solid ${alertPopup.level === 'ALERT' ? '#d32f2f' : 
                                      alertPopup.level === 'WARNING' ? '#ff9800' : '#4caf50'}`
            }}>
              <div style={{ 
                fontSize: '16px',
                lineHeight: '1.5',
                color: '#333'
              }}>
                {alertPopup.message}
              </div>
            </div>
            
            <Button onClick={closeAlert}>Close Alert</Button>
          </AlertPopup>
        </>
      )}
    </Container>
  );
}

export default Notifications;
