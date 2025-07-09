import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import styled from 'styled-components';
import HomePage from './components/HomePage';
import HealthAlerts from './components/HealthAlerts';
import Forecast from './components/Forecast';
import Heatmap from './components/Heatmap';
import Notifications from './components/Notifications';
import Navigation from './components/Navigation';
import GlobalStyle from './styles/GlobalStyle';

const AppContainer = styled.div`
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
`;

const ContentContainer = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
`;

function App() {
  return (
    <AppContainer>
      <GlobalStyle />
      <Router>
        <ContentContainer>
          <Navigation />
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/health-alerts" element={<HealthAlerts />} />
            <Route path="/forecast" element={<Forecast />} />
            <Route path="/heatmap" element={<Heatmap />} />
            <Route path="/notifications" element={<Notifications />} />
          </Routes>
        </ContentContainer>
      </Router>
    </AppContainer>
  );
}

export default App;
