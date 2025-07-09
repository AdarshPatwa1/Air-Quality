from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
from utils import get_latest_aqi_by_location, get_historical_data, get_available_cities
from forecast_model import forecast_aqi
from health_recommendations import get_health_recommendations, get_alert_threshold_message
from heatmap_utils import generate_heatmap_data, get_aqi_statistics
from push_notifications import get_notification_manager
import json
import uuid
import os

app = Flask(__name__, static_folder='frontend/build', static_url_path='')
CORS(app)  # Enable CORS for React frontend

# Serve React App
@app.route('/')
@app.route('/<path:path>')
def serve_react_app(path=''):
    if path != '' and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')

# API Routes for React Frontend
@app.route('/aqi', methods=['POST'])
def get_aqi():
    data = request.get_json()
    location = data.get('location')
    
    try:
        aqi_data = get_latest_aqi_by_location(location)
        if aqi_data:
            # Check if it's an error response
            if 'error' in aqi_data:
                return jsonify(aqi_data), 404
            else:
                return jsonify(aqi_data)
        else:
            return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/history', methods=['POST'])
def get_history():
    data = request.get_json()
    location = data.get('location')
    
    try:
        historical_data = get_historical_data(location)
        
        # Ensure column names match (lowercase, stripped)
        if not all(col in historical_data.columns for col in ['date', 'aqi']):
            return jsonify({'error': f"No valid 'date' or 'aqi' data found for {location}"}), 400
        
        # Convert DataFrame to JSON-serializable format
        history_json = historical_data.to_dict('records')
        return jsonify(history_json)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/forecast', methods=['POST'])
def get_forecast():
    data = request.get_json()
    location = data.get('location')
    
    try:
        forecast = forecast_aqi(location)
        if forecast:
            return jsonify(forecast)
        else:
            return jsonify({'error': 'Unable to generate forecast'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health_alerts', methods=['POST'])
def get_health_alerts():
    data = request.get_json()
    location = data.get('location')
    age_group = data.get('age_group')
    health_conditions = data.get('health_conditions', [])

    try:
        aqi_data = get_latest_aqi_by_location(location)
        if aqi_data:
            # Check if it's an error response
            if 'error' in aqi_data:
                return jsonify(aqi_data), 404
            else:
                recommendations = get_health_recommendations(aqi_data['aqi'], age_group, health_conditions)
                alert_message = get_alert_threshold_message(aqi_data['aqi'])
                return jsonify({'aqi': aqi_data, 'recommendations': recommendations, 'alert_message': alert_message})
        else:
            return jsonify({'error': 'Location not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/heatmap', methods=['GET', 'POST'])
def get_heatmap():
    try:
        heatmap_data = generate_heatmap_data()
        statistics = get_aqi_statistics()
        return jsonify({'heatmap_data': heatmap_data, 'statistics': statistics})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/notifications', methods=['POST'])
def notifications():
    data = request.get_json()
    action = data.get('action')
    notification_manager = get_notification_manager()
    
    try:
        if action == 'subscribe':
            user_id = data.get('user_id', str(uuid.uuid4()))
            location = data.get('location')
            threshold = data.get('threshold', 100)
            age_group = data.get('age_group')
            health_conditions = data.get('health_conditions', [])
            
            success = notification_manager.subscribe_user(
                user_id=user_id, 
                location=location, 
                threshold=threshold, 
                age_group=age_group, 
                health_conditions=health_conditions
            )
            
            if success:
                return jsonify({
                    'message': f'Subscribed to alerts for {location} when AQI exceeds {threshold}',
                    'user_id': user_id,
                    'location': location,
                    'threshold': threshold,
                    'age_group': age_group,
                    'health_conditions': health_conditions
                })
            else:
                return jsonify({'error': 'Failed to subscribe'}), 500
        
        elif action == 'unsubscribe':
            user_id = data.get('user_id')
            success = notification_manager.unsubscribe_user(user_id)
            if success:
                return jsonify({'message': 'Unsubscribed from notifications'})
            else:
                return jsonify({'error': 'Failed to unsubscribe'}), 500
        
        elif action == 'test':
            user_id = data.get('user_id')
            location = data.get('location')
            threshold = data.get('threshold')
            test_result = notification_manager.simulate_immediate_check(user_id, location, threshold)
            return jsonify(test_result)
        
        else:
            return jsonify({'error': 'Invalid action'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/subscriptions', methods=['GET'])
def subscriptions():
    try:
        notification_manager = get_notification_manager()
        subscriptions = notification_manager.get_all_subscriptions()
        return jsonify({'subscriptions': subscriptions})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/cities', methods=['GET'])
def get_cities():
    try:
        cities = get_available_cities()
        return jsonify({'cities': cities})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
