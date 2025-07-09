import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import styled from 'styled-components';

const NavContainer = styled.nav`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  padding: 15px 0;
  border-radius: 15px;
  margin: 20px 0;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
`;

const NavList = styled.ul`
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
`;

const NavItem = styled.li`
  margin: 0 10px;
`;

const NavLink = styled(Link)`
  color: white;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 25px;
  transition: all 0.3s ease;
  font-weight: 500;
  background: ${({active}) => active ? 'rgba(255, 255, 255, 0.2)' : 'transparent'};
  border: 2px solid ${({active}) => active ? 'rgba(255, 255, 255, 0.3)' : 'transparent'};
  
  &:hover {
    background: rgba(255, 255, 255, 0.2);
    border-color: rgba(255, 255, 255, 0.3);
    transform: translateY(-2px);
  }
`;

function Navigation() {
  const location = useLocation();

  const navItems = [
    { path: '/', label: '🏠 Home' },
    { path: '/health-alerts', label: '🏥 Health Alerts' },
    { path: '/forecast', label: '🌤️ Forecast' },
    { path: '/heatmap', label: '🗺️ Heatmap' },
    { path: '/notifications', label: '🔔 Notifications' }
  ];

  return (
    <NavContainer>
      <NavList>
        {navItems.map((item) => (
          <NavItem key={item.path}>
            <NavLink 
              to={item.path} 
              active={location.pathname === item.path ? 'true' : 'false'}
            >
              {item.label}
            </NavLink>
          </NavItem>
        ))}
      </NavList>
    </NavContainer>
  );
}

export default Navigation;
