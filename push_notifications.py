import json
import threading
import time
from datetime import datetime, timedelta
from utils import get_latest_aqi_by_location
from health_recommendations import get_alert_threshold_message

class NotificationManager:
    def __init__(self):
        self.subscriptions = {}  # In production, use a database
        self.alert_history = {}  # Track recent alerts to avoid spam
        self.monitoring_active = False
        self.monitoring_thread = None
        
    def subscribe_user(self, user_id, location, threshold=100, age_group=None, health_conditions=None):
        """
        Subscribe a user to push notifications for a specific location and threshold
        """
        self.subscriptions[user_id] = {
            'location': location,
            'threshold': threshold,
            'age_group': age_group,
            'health_conditions': health_conditions,
            'created_at': datetime.now(),
            'last_alert': None
        }
        
        if not self.monitoring_active:
            self.start_monitoring()
            
        return True
    
    def unsubscribe_user(self, user_id):
        """
        Unsubscribe a user from notifications
        """
        if user_id in self.subscriptions:
            del self.subscriptions[user_id]
            return True
        return False
    
    def start_monitoring(self):
        """
        Start the background monitoring thread
        """
        if not self.monitoring_active:
            self.monitoring_active = True
            self.monitoring_thread = threading.Thread(target=self._monitor_aqi_levels)
            self.monitoring_thread.daemon = True
            self.monitoring_thread.start()
    
    def stop_monitoring(self):
        """
        Stop the background monitoring
        """
        self.monitoring_active = False
        if self.monitoring_thread:
            self.monitoring_thread.join()
    
    def _monitor_aqi_levels(self):
        """
        Background thread to monitor AQI levels and send alerts
        """
        while self.monitoring_active:
            try:
                for user_id, subscription in self.subscriptions.items():
                    self._check_user_threshold(user_id, subscription)
                
                # Check every 30 minutes
                time.sleep(1800)
                
            except Exception as e:
                print(f"Error in monitoring thread: {e}")
                time.sleep(60)  # Wait 1 minute before retrying
    
    def _check_user_threshold(self, user_id, subscription):
        """
        Check if a user's threshold has been exceeded
        """
        try:
            location = subscription['location']
            threshold = subscription['threshold']
            
            # Get current AQI
            aqi_data = get_latest_aqi_by_location(location)
            if not aqi_data or aqi_data['aqi'] is None:
                return
            
            current_aqi = float(aqi_data['aqi'])
            
            # Check if threshold is exceeded
            if current_aqi > threshold:
                # Check if we've sent an alert recently (within 2 hours)
                last_alert = subscription.get('last_alert')
                if last_alert and datetime.now() - last_alert < timedelta(hours=2):
                    return
                
                # Generate alert message
                alert_message = get_alert_threshold_message(current_aqi)
                
                # Send notification (simulate - in production, use real push service)
                self._send_push_notification(user_id, subscription, current_aqi, alert_message)
                
                # Update last alert time
                subscription['last_alert'] = datetime.now()
                
        except Exception as e:
            print(f"Error checking threshold for user {user_id}: {e}")
    
    def _send_push_notification(self, user_id, subscription, current_aqi, alert_message):
        """
        Send push notification to user (simulated)
        """
        notification = {
            'user_id': user_id,
            'location': subscription['location'],
            'aqi': current_aqi,
            'threshold': subscription['threshold'],
            'message': alert_message['message'] if alert_message else f"AQI threshold exceeded: {current_aqi}",
            'level': alert_message['level'] if alert_message else "ALERT",
            'timestamp': datetime.now().isoformat(),
            'age_group': subscription.get('age_group'),
            'health_conditions': subscription.get('health_conditions')
        }
        
        # In production, this would integrate with services like:
        # - Firebase Cloud Messaging (FCM)
        # - Apple Push Notification Service (APNS)
        # - Web Push Protocol
        # - SMS/Email services
        
        # For now, log the notification
        print(f"🚨 PUSH NOTIFICATION: {notification}")
        
        # Store in alert history
        if user_id not in self.alert_history:
            self.alert_history[user_id] = []
        
        self.alert_history[user_id].append(notification)
        
        # Keep only last 10 alerts per user
        if len(self.alert_history[user_id]) > 10:
            self.alert_history[user_id] = self.alert_history[user_id][-10:]
    
    def get_user_alert_history(self, user_id):
        """
        Get alert history for a user
        """
        return self.alert_history.get(user_id, [])
    
    def get_all_subscriptions(self):
        """
        Get all active subscriptions (for admin dashboard)
        """
        return self.subscriptions
    
    def simulate_immediate_check(self, user_id, location=None, threshold=None):
        """
        Trigger immediate check for a user (for testing)
        """
        if user_id in self.subscriptions:
            subscription = self.subscriptions[user_id]
            
            # Get current AQI
            aqi_data = get_latest_aqi_by_location(subscription['location'])
            if not aqi_data or aqi_data['aqi'] is None:
                return {
                    'success': False,
                    'message': f"Unable to get AQI data for {subscription['location']}"
                }
            
            current_aqi = float(aqi_data['aqi'])
            threshold = subscription['threshold']
            location = subscription['location']
            
            # Generate detailed alert message
            if current_aqi > threshold:
                comparison = "higher"
                status = "ALERT"
                precaution = self._get_precaution_message(current_aqi, subscription.get('age_group'), subscription.get('health_conditions', []))
            elif current_aqi == threshold:
                comparison = "equal to"
                status = "WARNING"
                precaution = "Monitor air quality closely and be prepared to take precautions if levels rise."
            else:
                comparison = "lower"
                status = "SAFE"
                precaution = "Air quality is acceptable. Continue with normal activities."
            
            detailed_message = f"The current AQI of {location} is {current_aqi}, which is {comparison} than your threshold of {threshold}. {precaution}"
            
            # Create test notification
            test_notification = {
                'user_id': user_id,
                'location': location,
                'current_aqi': current_aqi,
                'threshold': threshold,
                'message': detailed_message,
                'level': status,
                'timestamp': datetime.now().isoformat(),
                'age_group': subscription.get('age_group'),
                'health_conditions': subscription.get('health_conditions'),
                'is_test': True,
                'success': True
            }
            
            # Store in alert history
            if user_id not in self.alert_history:
                self.alert_history[user_id] = []
            
            self.alert_history[user_id].append(test_notification)
            
            # Keep only last 10 alerts per user
            if len(self.alert_history[user_id]) > 10:
                self.alert_history[user_id] = self.alert_history[user_id][-10:]
            
            return test_notification
        
        # If no subscription found, but location and threshold provided, create a test alert
        if location and threshold is not None:
            aqi_data = get_latest_aqi_by_location(location)
            if not aqi_data or aqi_data['aqi'] is None:
                return {
                    'success': False,
                    'message': f"Unable to get AQI data for {location}",
                    'current_aqi': 'Unknown'
                }
            
            current_aqi = float(aqi_data['aqi'])
            
            # Generate detailed alert message
            if current_aqi > threshold:
                comparison = "higher"
                status = "ALERT"
                precaution = self._get_precaution_message(current_aqi, None, [])
            elif current_aqi == threshold:
                comparison = "equal to"
                status = "WARNING"
                precaution = "Monitor air quality closely and be prepared to take precautions if levels rise."
            else:
                comparison = "lower"
                status = "SAFE"
                precaution = "Air quality is acceptable. Continue with normal activities."
            
            detailed_message = f"The current AQI of {location} is {current_aqi}, which is {comparison} than your threshold of {threshold}. {precaution}"
            
            return {
                'success': True,
                'location': location,
                'current_aqi': current_aqi,
                'threshold': threshold,
                'message': detailed_message,
                'level': status,
                'is_test': True
            }
        
        return {
            'success': False,
            'message': 'User subscription not found',
            'current_aqi': 'Unknown'
        }
    
    def _get_precaution_message(self, aqi, age_group, health_conditions):
        """
        Generate precaution message based on AQI and user profile
        """
        base_message = ""
        
        if aqi <= 50:
            base_message = "Air quality is good. Perfect for outdoor activities."
        elif aqi <= 100:
            base_message = "Air quality is acceptable. Sensitive individuals should monitor symptoms."
        elif aqi <= 150:
            base_message = "Sensitive groups should limit outdoor activities. Consider wearing masks outdoors."
        elif aqi <= 200:
            base_message = "Everyone should limit outdoor activities. Wear masks when going outside."
        elif aqi <= 300:
            base_message = "Avoid outdoor activities entirely. Keep windows closed and use air purifiers."
        else:
            base_message = "Emergency conditions. Stay indoors and avoid all outdoor activities."
        
        # Add age-specific advice
        if age_group == 'child' and aqi > 100:
            base_message += " Children should avoid outdoor play and sports."
        elif age_group == 'elderly' and aqi > 80:
            base_message += " Elderly individuals should minimize outdoor exposure."
        
        # Add health condition-specific advice
        if health_conditions:
            if 'asthma' in health_conditions and aqi > 100:
                base_message += " Keep rescue inhaler readily available."
            if 'heart_disease' in health_conditions and aqi > 100:
                base_message += " Avoid strenuous activities and monitor symptoms."
            if 'copd' in health_conditions and aqi > 80:
                base_message += " Use supplemental oxygen as prescribed."
        
        return base_message

# Global notification manager instance
notification_manager = NotificationManager()

def get_notification_manager():
    """
    Get the global notification manager instance
    """
    return notification_manager
