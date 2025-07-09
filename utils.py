import pandas as pd
import numpy as np

def load_and_prepare_data():
    # Read the CSV file with proper parsing
    try:
        # Read the CSV file normally - it has proper structure
        df = pd.read_csv('data/aqi_data.csv')
        
        # Rename columns to match expected format
        df = df.rename(columns={
            'City': 'city',
            'Date': 'date',
            'AQI': 'aqi',
            'AQI_Bucket': 'aqi_bucket'
        })
        
        # Filter out rows with missing city, date, or AQI
        df = df.dropna(subset=['city', 'date', 'aqi'])
        
        # Filter out rows with empty city or date
        df = df[df['city'].str.strip() != '']
        df = df[df['date'].str.strip() != '']
        
        # Convert date column to datetime
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        # Add missing columns that the app expects
        df['main_pollutant'] = 'PM2.5'  # Default pollutant
        df['timestamp'] = df['date']
        
        # Select only the columns we need
        df = df[['city', 'date', 'aqi', 'main_pollutant', 'timestamp']]
        
        return df
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def get_available_cities():
    """
    Get list of all available cities in the dataset
    """
    df = load_and_prepare_data()
    
    if df.empty:
        return []
        
    return sorted(df['city'].unique().tolist())

def get_latest_aqi_by_location(location):
    df = load_and_prepare_data()
    
    if df.empty:
        return None
        
    df_location = df[df['city'].str.lower() == location.lower()]
    
    if df_location.empty:
        return {
            'error': f'City "{location}" not found in dataset.'
        }
    
    # Get the latest record with valid AQI
    latest = df_location.sort_values('date', ascending=False).head(1)
    
    if latest.empty:
        return None
    
    result = latest.to_dict(orient='records')[0]
    
    # Handle NaN values - convert to None or appropriate strings
    for key, value in result.items():
        if pd.isna(value):
            result[key] = None
    
    return result

def get_historical_data(location):
    df = load_and_prepare_data()
    
    if df.empty:
        return pd.DataFrame()
        
    df_location = df[df['city'].str.lower() == location.lower()]
    return df_location.sort_values('date') if not df_location.empty else pd.DataFrame()
