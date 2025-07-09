# Air Quality App

A modern web application for monitoring air quality with personalized health recommendations, forecasting, and interactive heatmaps.

## Features

- **Real-time AQI Data**: Get current air quality information for any location
- **Health Recommendations**: Personalized advice based on age, health conditions, and AQI levels
- **3-Day Forecast**: Predicted air quality trends with interactive charts
- **Interactive Heatmap**: Visual representation of air quality across different locations
- **Push Notifications**: Subscribe to air quality alerts

## Tech Stack

### Frontend
- React 18
- React Router DOM
- Styled Components
- Chart.js with React Chart.js 2
- Leaflet Maps with React Leaflet
- Axios for API calls

### Backend
- Flask (Python)
- Flask-CORS for cross-origin requests
- Pandas for data processing
- Custom modules for AQI data, forecasting, and notifications

## Setup Instructions

### 1. Backend Setup

1. Install Python dependencies:
```bash
pip install flask flask-cors pandas
```

2. Make sure all your custom modules are in place:
   - `utils.py` - AQI data utilities
   - `forecast_model.py` - Forecasting functionality
   - `health_recommendations.py` - Health advice system
   - `heatmap_utils.py` - Heatmap data generation
   - `push_notifications.py` - Notification system

3. Start the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### 2. Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install Node.js dependencies:
```bash
npm install
```

3. Start the React development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

### 3. Production Build

To create a production build of the React app:

```bash
cd frontend
npm run build
```

This will create a `build` folder that the Flask app can serve directly.

## API Endpoints

### GET /
Serves the React application

### POST /aqi
Get AQI data for a location
```json
{
  "location": "New York"
}
```

### POST /forecast
Get 3-day AQI forecast
```json
{
  "location": "New York"
}
```

### POST /health_alerts
Get personalized health recommendations
```json
{
  "location": "New York",
  "age_group": "adult",
  "health_conditions": ["asthma", "allergies"]
}
```

### GET /heatmap
Get heatmap data for visualization

### POST /notifications
Manage notification subscriptions
```json
{
  "action": "subscribe",
  "user_id": "user123",
  "location": "New York",
  "threshold": 100,
  "age_group": "adult",
  "health_conditions": ["asthma"]
}
```

### GET /subscriptions
Get all notification subscriptions

## Project Structure

```
Air Quality App/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── HomePage.js
│   │   │   ├── HealthAlerts.js
│   │   │   ├── Forecast.js
│   │   │   ├── Heatmap.js
│   │   │   ├── Notifications.js
│   │   │   └── Navigation.js
│   │   ├── styles/
│   │   │   └── GlobalStyle.js
│   │   ├── App.js
│   │   └── index.js
│   ├── public/
│   └── package.json
├── app.py
├── utils.py
├── forecast_model.py
├── health_recommendations.py
├── heatmap_utils.py
├── push_notifications.py
└── README.md
```

## Usage

1. **Home Page**: Enter a city name to get current AQI data
2. **Health Alerts**: Get personalized recommendations based on your profile
3. **Forecast**: View 3-day AQI predictions with interactive charts
4. **Heatmap**: Explore air quality across different locations on an interactive map
5. **Notifications**: Subscribe to air quality alerts for your location

## Notes

- The app uses a proxy configuration to connect the React frontend to the Flask backend
- CORS is enabled to allow cross-origin requests
- The backend serves the React build folder for production deployment
- All API endpoints return JSON responses for seamless integration with the React frontend
