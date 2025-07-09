def get_health_recommendations(aqi_value, age_group=None, health_conditions=None):
    """
    Generate personalized health recommendations based on AQI value and user profile
    """
    if aqi_value is None:
        return {"category": "Unknown", "recommendations": ["Unable to provide recommendations - AQI data unavailable"]}
    
    # Convert string AQI to float if needed
    if isinstance(aqi_value, str):
        try:
            aqi_value = float(aqi_value)
        except ValueError:
            return {"category": "Unknown", "recommendations": ["Unable to provide recommendations - Invalid AQI data"]}
    
    # Base recommendations by AQI category
    if aqi_value <= 50:
        category = "Good"
        color = "green"
        base_recommendations = [
            "Air quality is good - perfect for outdoor activities",
            "Great day for exercising outdoors",
            "All outdoor activities are safe for everyone"
        ]
    elif aqi_value <= 100:
        category = "Moderate"
        color = "yellow"
        base_recommendations = [
            "Air quality is acceptable for most people",
            "Sensitive individuals may experience minor symptoms",
            "Outdoor activities are generally safe"
        ]
    elif aqi_value <= 150:
        category = "Unhealthy for Sensitive Groups"
        color = "orange"
        base_recommendations = [
            "Sensitive groups should limit outdoor activities",
            "Consider wearing a mask if you have respiratory conditions",
            "Keep windows closed and use air purifiers indoors"
        ]
    elif aqi_value <= 200:
        category = "Unhealthy"
        color = "red"
        base_recommendations = [
            "Everyone should limit outdoor activities",
            "Wear N95 masks when going outside",
            "Avoid strenuous outdoor exercise",
            "Stay indoors with air purifiers running"
        ]
    elif aqi_value <= 300:
        category = "Very Unhealthy"
        color = "purple"
        base_recommendations = [
            "Avoid outdoor activities entirely",
            "Wear high-quality masks (N95/N99) if you must go outside",
            "Keep all windows and doors closed",
            "Use air purifiers and avoid cooking that creates smoke"
        ]
    else:
        category = "Hazardous"
        color = "maroon"
        base_recommendations = [
            "Emergency conditions - avoid all outdoor activities",
            "Wear N99 masks if you must go outside",
            "Seal your home and use multiple air purifiers",
            "Consider relocating temporarily if possible"
        ]
    
    # Personalized recommendations based on age group
    personalized_recommendations = base_recommendations.copy()
    
    if age_group:
        if age_group == "child" and aqi_value > 100:
            personalized_recommendations.extend([
                "Children should avoid outdoor play",
                "Schools should consider indoor recess",
                "Monitor children for coughing or breathing difficulties"
            ])
        elif age_group == "elderly" and aqi_value > 80:
            personalized_recommendations.extend([
                "Elderly individuals should minimize outdoor exposure",
                "Take medications as prescribed for respiratory conditions",
                "Consider visiting air-conditioned public spaces"
            ])
        elif age_group == "pregnant" and aqi_value > 100:
            personalized_recommendations.extend([
                "Pregnant women should avoid outdoor activities",
                "Consult your doctor about air quality concerns",
                "Consider using air purifiers in the bedroom"
            ])
    
    # Health condition-specific recommendations
    if health_conditions:
        if "asthma" in health_conditions and aqi_value > 80:
            personalized_recommendations.extend([
                "Keep rescue inhaler readily available",
                "Monitor symptoms closely",
                "Consider pre-medicating before going outside"
            ])
        if "heart_disease" in health_conditions and aqi_value > 100:
            personalized_recommendations.extend([
                "Avoid strenuous activities",
                "Monitor heart rate and blood pressure",
                "Consult your cardiologist if symptoms worsen"
            ])
        if "copd" in health_conditions and aqi_value > 80:
            personalized_recommendations.extend([
                "Use supplemental oxygen as prescribed",
                "Avoid all outdoor activities",
                "Have emergency medications ready"
            ])
    
    return {
        "category": category,
        "color": color,
        "aqi_value": aqi_value,
        "recommendations": personalized_recommendations
    }

def get_alert_threshold_message(aqi_value):
    """
    Generate alert messages for threshold breaches
    """
    if aqi_value is None:
        return None
    
    if isinstance(aqi_value, str):
        try:
            aqi_value = float(aqi_value)
        except ValueError:
            return None
    
    if aqi_value > 200:
        return {
            "level": "CRITICAL",
            "message": f"CRITICAL AIR QUALITY ALERT: AQI is {aqi_value}. Avoid all outdoor activities immediately!",
            "color": "red"
        }
    elif aqi_value > 150:
        return {
            "level": "HIGH",
            "message": f"HIGH AIR QUALITY ALERT: AQI is {aqi_value}. Sensitive groups should stay indoors.",
            "color": "orange"
        }
    elif aqi_value > 100:
        return {
            "level": "MODERATE",
            "message": f"MODERATE AIR QUALITY ALERT: AQI is {aqi_value}. Sensitive individuals should limit outdoor activities.",
            "color": "yellow"
        }
    
    return None
