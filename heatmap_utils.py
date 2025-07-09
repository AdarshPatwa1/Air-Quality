import pandas as pd
import json
from utils import load_and_prepare_data

def get_city_coordinates():
    """
    Mapping of cities to their coordinates for heatmap visualization
    """
    return {
        'ahmedabad': {'lat': 23.0225, 'lng': 72.5714},
        'bengaluru': {'lat': 12.9716, 'lng': 77.5946},
        'chennai': {'lat': 13.0827, 'lng': 80.2707},
        'delhi': {'lat': 28.7041, 'lng': 77.1025},
        'hyderabad': {'lat': 17.3850, 'lng': 78.4867},
        'kolkata': {'lat': 22.5726, 'lng': 88.3639},
        'mumbai': {'lat': 19.0760, 'lng': 72.8777},
        'pune': {'lat': 18.5204, 'lng': 73.8567},
        'jaipur': {'lat': 26.9124, 'lng': 75.7873},
        'lucknow': {'lat': 26.8467, 'lng': 80.9462},
        'kanpur': {'lat': 26.4499, 'lng': 80.3319},
        'nagpur': {'lat': 21.1458, 'lng': 79.0882},
        'indore': {'lat': 22.7196, 'lng': 75.8577},
        'thane': {'lat': 19.2183, 'lng': 72.9781},
        'bhopal': {'lat': 23.2599, 'lng': 77.4126},
        'visakhapatnam': {'lat': 17.6868, 'lng': 83.2185},
        'pimpri chinchwad': {'lat': 18.6298, 'lng': 73.7997},
        'patna': {'lat': 25.5941, 'lng': 85.1376},
        'vadodara': {'lat': 22.3072, 'lng': 73.1812},
        'ludhiana': {'lat': 30.9010, 'lng': 75.8573},
        'agra': {'lat': 27.1767, 'lng': 78.0081},
        'nashik': {'lat': 19.9975, 'lng': 73.7898},
        'faridabad': {'lat': 28.4089, 'lng': 77.3178},
        'meerut': {'lat': 28.9845, 'lng': 77.7064},
        'rajkot': {'lat': 22.3039, 'lng': 70.8022},
        'kalyan dombivali': {'lat': 19.2403, 'lng': 73.1305},
        'vasai virar': {'lat': 19.4912, 'lng': 72.8054},
        'varanasi': {'lat': 25.3176, 'lng': 82.9739},
        'srinagar': {'lat': 34.0837, 'lng': 74.7973},
        'aurangabad': {'lat': 19.8762, 'lng': 75.3433},
        'dhanbad': {'lat': 23.7957, 'lng': 86.4304},
        'amritsar': {'lat': 31.6340, 'lng': 74.8723},
        'navi mumbai': {'lat': 19.0330, 'lng': 73.0297},
        'allahabad': {'lat': 25.4358, 'lng': 81.8463},
        'ranchi': {'lat': 23.3441, 'lng': 85.3096},
        'howrah': {'lat': 22.5958, 'lng': 88.2636},
        'coimbatore': {'lat': 11.0168, 'lng': 76.9558},
        'jabalpur': {'lat': 23.1815, 'lng': 79.9864},
        'gwalior': {'lat': 26.2183, 'lng': 78.1828},
        'vijayawada': {'lat': 16.5062, 'lng': 80.6480},
        'jodhpur': {'lat': 26.2389, 'lng': 73.0243},
        'madurai': {'lat': 9.9252, 'lng': 78.1198},
        'raipur': {'lat': 21.2514, 'lng': 81.6296},
        'kota': {'lat': 25.2138, 'lng': 75.8648},
        'chandigarh': {'lat': 30.7333, 'lng': 76.7794},
        'guwahati': {'lat': 26.1445, 'lng': 91.7362},
        'solapur': {'lat': 17.6599, 'lng': 75.9064},
        'hubballi dharwad': {'lat': 15.3647, 'lng': 75.1240},
        'tiruchirappalli': {'lat': 10.7905, 'lng': 78.7047},
        'bareilly': {'lat': 28.3670, 'lng': 79.4304},
        'moradabad': {'lat': 28.8386, 'lng': 78.7733},
        'mysore': {'lat': 12.2958, 'lng': 76.6394},
        'tiruppur': {'lat': 11.1085, 'lng': 77.3411},
        'gurgaon': {'lat': 28.4595, 'lng': 77.0266},
        'aligarh': {'lat': 27.8974, 'lng': 78.0880},
        'jalandhar': {'lat': 31.3260, 'lng': 75.5762},
        'bhubaneswar': {'lat': 20.2961, 'lng': 85.8245},
        'salem': {'lat': 11.6643, 'lng': 78.1460},
        'warangal': {'lat': 17.9689, 'lng': 79.5941},
        'guntur': {'lat': 16.3067, 'lng': 80.4365},
        'bhiwandi': {'lat': 19.3002, 'lng': 73.0630},
        'saharanpur': {'lat': 29.9680, 'lng': 77.5552},
        'gorakhpur': {'lat': 26.7606, 'lng': 83.3732},
        'bikaner': {'lat': 28.0229, 'lng': 73.3119},
        'amravati': {'lat': 20.9319, 'lng': 77.7523},
        'noida': {'lat': 28.5355, 'lng': 77.3910},
        'jamshedpur': {'lat': 22.8046, 'lng': 86.2029},
        'bhilai nagar': {'lat': 21.1938, 'lng': 81.3509},
        'cuttack': {'lat': 20.4625, 'lng': 85.8828},
        'firozabad': {'lat': 27.1592, 'lng': 78.3957},
        'kochi': {'lat': 9.9312, 'lng': 76.2673},
        'bhavnagar': {'lat': 21.7645, 'lng': 72.1519},
        'dehradun': {'lat': 30.3165, 'lng': 78.0322},
        'durgapur': {'lat': 23.5204, 'lng': 87.3119},
        'asansol': {'lat': 23.6739, 'lng': 86.9524},
        'nanded waghala': {'lat': 19.1383, 'lng': 77.2975},
        'kolhapur': {'lat': 16.7050, 'lng': 74.2433},
        'ajmer': {'lat': 26.4499, 'lng': 74.6399},
        'akola': {'lat': 20.7002, 'lng': 77.0082},
        'gulbarga': {'lat': 17.3297, 'lng': 76.8343},
        'jamnagar': {'lat': 22.4707, 'lng': 70.0577},
        'ujjain': {'lat': 23.1765, 'lng': 75.7885},
        'loni': {'lat': 28.7506, 'lng': 77.2897},
        'siliguri': {'lat': 26.7271, 'lng': 88.3953},
        'jhansi': {'lat': 25.4484, 'lng': 78.5685},
        'ulhasnagar': {'lat': 19.2183, 'lng': 73.1535},
        'jammu': {'lat': 32.7266, 'lng': 74.8570},
        'sangli miraj kupwad': {'lat': 16.8524, 'lng': 74.5815},
        'mangalore': {'lat': 12.9141, 'lng': 74.8560},
        'erode': {'lat': 11.3410, 'lng': 77.7172},
        'belgaum': {'lat': 15.8497, 'lng': 74.4977},
        'ambattur': {'lat': 13.1143, 'lng': 80.1548},
        'tirunelveli': {'lat': 8.7139, 'lng': 77.7567},
        'malegaon': {'lat': 20.5579, 'lng': 74.5287},
        'gaya': {'lat': 24.7914, 'lng': 85.0002},
        'udaipur': {'lat': 24.5854, 'lng': 73.7125},
        'kakinada': {'lat': 16.9891, 'lng': 82.2475},
        'davanagere': {'lat': 14.4644, 'lng': 75.9216},
        'kozhikode': {'lat': 11.2588, 'lng': 75.7804},
        'akola': {'lat': 20.7002, 'lng': 77.0082},
        'kurnool': {'lat': 15.8281, 'lng': 78.0373}
    }

def get_latest_aqi_for_all_cities():
    """
    Get the latest AQI data for all cities in the dataset
    """
    df = load_and_prepare_data()
    city_coords = get_city_coordinates()
    
    # Get the latest AQI for each city
    latest_data = []
    
    for city in df['city'].unique():
        city_data = df[df['city'].str.lower() == city.lower()]
        if city_data.empty:
            continue
            
        # Get latest record with valid AQI
        city_with_aqi = city_data[city_data['aqi'].notna()]
        if city_with_aqi.empty:
            continue
            
        latest_record = city_with_aqi.sort_values('date', ascending=False).iloc[0]
        
        # Get coordinates
        city_key = city.lower().replace(' ', '').replace('-', '')
        coords = city_coords.get(city_key, city_coords.get(city.lower()))
        
        if coords:
            latest_data.append({
                'city': city,
                'aqi': float(latest_record['aqi']),
                'aqi_bucket': latest_record.get('aqi_bucket', 'Unknown'),
                'date': latest_record['date'].strftime('%Y-%m-%d'),
                'lat': coords['lat'],
                'lng': coords['lng']
            })
    
    return latest_data

def generate_heatmap_data():
    """
    Generate heatmap data in the format required for visualization
    """
    cities_data = get_latest_aqi_for_all_cities()
    
    # Convert to format suitable for heatmap
    heatmap_points = []
    for city in cities_data:
        # Normalize AQI for heatmap intensity (0-1 scale)
        intensity = min(city['aqi'] / 500, 1.0)  # Cap at 500 AQI
        
        heatmap_points.append({
            'lat': city['lat'],
            'lng': city['lng'],
            'intensity': intensity,
            'city': city['city'],
            'aqi': city['aqi'],
            'category': city['aqi_bucket'],
            'date': city['date']
        })
    
    return heatmap_points

def get_aqi_statistics():
    """
    Generate statistics for the dashboard
    """
    cities_data = get_latest_aqi_for_all_cities()
    
    if not cities_data:
        return {
            'total_cities': 0,
            'avg_aqi': 0,
            'max_aqi': 0,
            'min_aqi': 0,
            'unhealthy_cities': 0
        }
    
    aqi_values = [city['aqi'] for city in cities_data]
    
    return {
        'total_cities': len(cities_data),
        'avg_aqi': round(sum(aqi_values) / len(aqi_values), 2),
        'max_aqi': max(aqi_values),
        'min_aqi': min(aqi_values),
        'unhealthy_cities': len([aqi for aqi in aqi_values if aqi > 100]),
        'cities_data': cities_data
    }
