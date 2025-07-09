from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pandas as pd
from utils import get_latest_aqi_by_location, get_historical_data
from forecast_model import forecast_aqi
from health_recommendations import get_health_recommendations, get_alert_threshold_message
from heatmap_utils import generate_heatmap_data, get_aqi_statistics
from push_notifications import get_notification_manager
import json
import uuid

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# API Routes for React frontend
@app.route('/api/aqi', methods=['POST'])
def api_get_aqi():
    data = request.get_json()
    location = data.get('location')
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    aqi_data = get_latest_aqi_by_location(location)
    if not aqi_data:
        return jsonify({'error': 'Location not found'}), 404
    
    recommendations = get_health_recommendations(aqi_data['aqi'])
    alert_message = get_alert_threshold_message(aqi_data['aqi'])
    
    return jsonify({
        'aqi': aqi_data,
        'recommendations': recommendations,
        'alert_message': alert_message
    })

@app.route('/api/forecast', methods=['POST'])
def api_get_forecast():
    data = request.get_json()
    location = data.get('location')
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    forecast = forecast_aqi(location)
    return jsonify(forecast)

@app.route('/api/health-alerts', methods=['POST'])
def api_health_alerts():
    data = request.get_json()
    location = data.get('location')
    age_group = data.get('age_group')
    health_conditions = data.get('health_conditions', [])
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    aqi_data = get_latest_aqi_by_location(location)
    if not aqi_data:
        return jsonify({'error': 'Location not found'}), 404
    
    recommendations = get_health_recommendations(aqi_data['aqi'], age_group, health_conditions)
    alert_message = get_alert_threshold_message(aqi_data['aqi'])
    
    return jsonify({
        'aqi': aqi_data,
        'recommendations': recommendations,
        'alert_message': alert_message
    })

@app.route('/api/heatmap', methods=['GET'])
def api_heatmap():
    heatmap_data = generate_heatmap_data()
    statistics = get_aqi_statistics()
    
    return jsonify({
        'heatmap_data': heatmap_data,
        'statistics': statistics
    })

@app.route('/api/notifications', methods=['GET'])
def api_get_notifications():
    notification_manager = get_notification_manager()
    return jsonify({
        'subscriptions': notification_manager.get_all_subscriptions()
    })

@app.route('/api/notifications/subscribe', methods=['POST'])
def api_subscribe_notifications():
    data = request.get_json()
    user_id = data.get('user_id', str(uuid.uuid4()))
    location = data.get('location')
    threshold = int(data.get('threshold', 100))
    age_group = data.get('age_group')
    health_conditions = data.get('health_conditions', [])
    
    if not location:
        return jsonify({'error': 'Location is required'}), 400
    
    notification_manager = get_notification_manager()
    success = notification_manager.subscribe_user(
        user_id, location, threshold, age_group, health_conditions
    )
    
    if success:
        return jsonify({
            'message': f'Subscribed to alerts for {location}',
            'user_id': user_id,
            'subscriptions': notification_manager.get_all_subscriptions()
        })
    else:
        return jsonify({'error': 'Failed to subscribe'}), 500

@app.route('/api/notifications/unsubscribe', methods=['POST'])
def api_unsubscribe_notifications():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    notification_manager = get_notification_manager()
    success = notification_manager.unsubscribe_user(user_id)
    
    if success:
        return jsonify({
            'message': 'Unsubscribed from notifications',
            'subscriptions': notification_manager.get_all_subscriptions()
        })
    else:
        return jsonify({'error': 'Failed to unsubscribe'}), 500

@app.route('/api/notifications/test', methods=['POST'])
def api_test_notification():
    data = request.get_json()
    user_id = data.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'User ID is required'}), 400
    
    notification_manager = get_notification_manager()
    result = notification_manager.simulate_immediate_check(user_id)
    
    return jsonify(result)

# Keep original routes for backward compatibility
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/aqi', methods=['POST'])
def show_aqi():
    location = request.form['location']
    aqi_data = get_latest_aqi_by_location(location)
    recommendations = get_health_recommendations(aqi_data['aqi'])
    alert_message = get_alert_threshold_message(aqi_data['aqi'])
    return render_template('index.html', location=location, aqi=aqi_data, recommendations=recommendations, alert_message=alert_message)

@app.route('/history', methods=['POST'])
def show_history():
    location = request.form['location']
    historical_data = get_historical_data(location)

    # Ensure column names match (lowercase, stripped)
    if not all(col in historical_data.columns for col in ['date', 'aqi']):
        return f"No valid 'date' or 'aqi' data found for {location}", 400

    graph = historical_data.plot(x='date', y='aqi', title=f"AQI History - {location}").get_figure()
    graph.savefig('static/history.png')
    return render_template('history.html', location=location)

@app.route('/forecast', methods=['POST'])
def show_forecast():
    location = request.form['location']
    forecast = forecast_aqi(location)
    return render_template('forecast.html', forecast=forecast, location=location)

@app.route('/health_alerts', methods=['GET', 'POST'])
def health_alerts():
    if request.method == 'POST':
        location = request.form['location']
        age_group = request.form.get('age_group')
        health_conditions = request.form.getlist('health_conditions')
        
        aqi_data = get_latest_aqi_by_location(location)
        if aqi_data:
            recommendations = get_health_recommendations(aqi_data['aqi'], age_group, health_conditions)
            alert_message = get_alert_threshold_message(aqi_data['aqi'])
            return render_template('health_alerts.html', location=location, aqi=aqi_data, 
                                 recommendations=recommendations, alert_message=alert_message)
        else:
            return render_template('health_alerts.html', error="Location not found")
    
    return render_template('health_alerts.html')

@app.route('/heatmap')
def heatmap():
    heatmap_data = generate_heatmap_data()
    statistics = get_aqi_statistics()
    return render_template('heatmap.html', heatmap_data=json.dumps(heatmap_data), statistics=statistics)

@app.route('/notifications', methods=['GET', 'POST'])
def notifications():
    notification_manager = get_notification_manager()
    
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'subscribe':
            user_id = request.form.get('user_id', str(uuid.uuid4()))
            location = request.form['location']
            threshold = int(request.form.get('threshold', 100))
            age_group = request.form.get('age_group')
            health_conditions = request.form.getlist('health_conditions')
            
            success = notification_manager.subscribe_user(
                user_id, location, threshold, age_group, health_conditions
            )
            
            if success:
                message = f"✅ Subscribed to alerts for {location} when AQI exceeds {threshold}"
                return render_template('notifications.html', 
                                     message=message, 
                                     user_id=user_id,
                                     subscriptions=notification_manager.get_all_subscriptions())
        
        elif action == 'unsubscribe':
            user_id = request.form['user_id']
            success = notification_manager.unsubscribe_user(user_id)
            message = "✅ Unsubscribed from notifications" if success else "❌ Failed to unsubscribe"
            return render_template('notifications.html', 
                                 message=message,
                                 subscriptions=notification_manager.get_all_subscriptions())
        
        elif action == 'test':
            user_id = request.form['user_id']
            test_result = notification_manager.simulate_immediate_check(user_id)
            
            if test_result['success']:
                return render_template('notifications.html', 
                                     test_notification=test_result,
                                     subscriptions=notification_manager.get_all_subscriptions())
            else:
                return render_template('notifications.html', 
                                     message=f"❌ {test_result['message']}",
                                     subscriptions=notification_manager.get_all_subscriptions())
    
    return render_template('notifications.html', subscriptions=notification_manager.get_all_subscriptions())

if __name__ == '__main__':
    app.run(debug=True)
