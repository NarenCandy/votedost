"""Tests for Google Cloud service integrations."""
import unittest
from unittest.mock import patch, MagicMock, call
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestFirestoreIntegration(unittest.TestCase):
    """Tests for Firestore integration."""
    
    def test_firestore_save_called_on_successful_chat(self):
        """Verify Firestore save is called after successful AI response."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'), \
             patch('app.routes.chat.save_chat_to_firestore') as mock_save, \
             patch('app.routes.chat.get_ai_response', return_value='Test response'):
            from app import app as application
            client = application.test_client()
            client.post('/chat',
                json={'message': 'test', 'language': 'English'},
                content_type='application/json')
            mock_save.assert_called_once()
    
    def test_chat_works_when_firestore_fails(self):
        """Ensure chat still works if Firestore is unavailable."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'), \
             patch('app.routes.chat.save_chat_to_firestore', side_effect=Exception("Firestore down")), \
             patch('app.routes.chat.get_ai_response', return_value='Test response'):
            from app import app as application
            client = application.test_client()
            response = client.post('/chat',
                json={'message': 'test', 'language': 'English'},
                content_type='application/json')
            self.assertEqual(response.status_code, 200)

class TestBigQueryIntegration(unittest.TestCase):
    """Tests for BigQuery integration."""
    
    def test_bigquery_log_called_on_successful_chat(self):
        """Verify BigQuery logging is called after successful response."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'), \
             patch('app.routes.chat.log_to_bigquery') as mock_bq, \
             patch('app.routes.chat.get_ai_response', return_value='Test response'):
            from app import app as application
            client = application.test_client()
            client.post('/chat',
                json={'message': 'test', 'language': 'English'},
                content_type='application/json')
            mock_bq.assert_called_once()
    
    def test_chat_works_when_bigquery_fails(self):
        """Ensure chat works if BigQuery is unavailable."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'), \
             patch('app.routes.chat.log_to_bigquery', side_effect=Exception("BQ down")), \
             patch('app.routes.chat.get_ai_response', return_value='Test response'):
            from app import app as application
            client = application.test_client()
            response = client.post('/chat',
                json={'message': 'test', 'language': 'English'},
                content_type='application/json')
            self.assertEqual(response.status_code, 200)

class TestTranslationIntegration(unittest.TestCase):
    """Tests for Translation API integration."""
    
    def test_language_detection_called(self):
        """Verify language detection is called for user messages."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'), \
             patch('app.routes.chat.detect_language', return_value='en') as mock_detect, \
             patch('app.routes.chat.get_ai_response', return_value='Test response'):
            from app import app as application
            client = application.test_client()
            client.post('/chat',
                json={'message': 'test', 'language': 'English'},
                content_type='application/json')
            mock_detect.assert_called_once()
    
    def test_fallback_when_translation_fails(self):
        """Ensure app works if Translation API fails."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'), \
             patch('app.routes.chat.detect_language', side_effect=Exception("Translation down")), \
             patch('app.routes.chat.get_ai_response', return_value='Test response'):
            from app import app as application
            client = application.test_client()
            response = client.post('/chat',
                json={'message': 'test', 'language': 'English'},
                content_type='application/json')
            self.assertEqual(response.status_code, 200)

class TestHealthEndpointServices(unittest.TestCase):
    """Tests for health endpoint Google Services status."""
    
    def test_health_shows_google_services_status(self):
        """Health endpoint should show status of all Google services."""
        with patch('vertexai.init'), \
             patch('vertexai.generative_models.GenerativeModel'):
            from app import app as application
            client = application.test_client()
            response = client.get('/health')
            data = response.get_json()
            self.assertIn('services', data)
            self.assertIn('firestore', data['services'])
            self.assertIn('bigquery', data['services'])
            self.assertIn('translation', data['services'])

if __name__ == '__main__':
    unittest.main()
