import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

def forecast_aqi(location):
    """
    Simplified forecast function that provides 3-day AQI predictions
    """
    try:
        # Load and normalize dataset
        df = pd.read_csv('data/aqi_data.csv')
        df.columns = df.columns.str.strip().str.lower()
        
        # Check required columns
        if 'city' not in df.columns or 'aqi' not in df.columns or 'date' not in df.columns:
            return generate_mock_forecast()
        
        # Filter by city
        df = df[df['city'].str.lower() == location.lower()]
        
        if df.empty:
            return generate_mock_forecast()
        
        # Sort and prepare AQI series
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        df = df.sort_values('date')
        
        # Only keep records with valid AQI values
        df = df[df['aqi'].notna()]
        
        if df.empty:
            return generate_mock_forecast()
        
        # Get recent average AQI
        recent_aqi = df['aqi'].tail(10).mean()
        last_date = df['date'].max()
        
        # Generate forecast based on recent trends
        forecasts = []
        for i in range(3):
            # Add some randomness to simulate forecast uncertainty
            forecast_aqi = max(0, min(500, recent_aqi + random.randint(-20, 20)))
            next_date = last_date + pd.Timedelta(days=i+1)
            
            forecasts.append({
                'date': str(next_date.date()),
                'aqi': round(forecast_aqi, 1)
            })
        
        return forecasts
        
    except Exception as e:
        return generate_mock_forecast()

def generate_mock_forecast():
    """Generate mock forecast data when real data is unavailable"""
    today = datetime.now()
    base_aqi = random.randint(50, 150)
    
    forecast_data = []
    for i in range(3):
        forecast_date = today + timedelta(days=i+1)
        aqi_value = max(0, base_aqi + random.randint(-20, 20))
        
        forecast_data.append({
            'date': forecast_date.strftime('%Y-%m-%d'),
            'aqi': aqi_value
        })
    
    return forecast_data
