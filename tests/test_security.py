"""Security-focused tests for VoteDost application."""
import unittest
from unittest.mock import patch, MagicMock
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestSecurityHeaders(unittest.TestCase):
    """Tests for security headers and practices."""
    
    def setUp(self):
        with patch('vertexai.init'), patch('vertexai.generative_models.GenerativeModel'):
            from app import app as application
            self.app = application.test_client()
    
    def test_no_server_header_exposed(self):
        """Ensure server technology is not exposed in headers."""
        response = self.app.get('/')
        self.assertNotIn('X-Powered-By', response.headers)
    
    def test_security_headers_present(self):
        """Ensure critical security headers are present."""
        response = self.app.get('/')
        self.assertEqual(response.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(response.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertIn('Content-Security-Policy', response.headers)
    
    def test_sensitive_data_not_in_response(self):
        """Ensure API keys and secrets not returned in responses."""
        response = self.app.get('/health')
        data = str(response.get_json())
        self.assertNotIn('api_key', data)
        self.assertNotIn('secret', data.lower())
    
    def test_oversized_payload_rejected(self):
        """Test that oversized payloads are rejected."""
        huge_message = 'A' * 2001
        response = self.app.post('/chat',
            json={'message': huge_message},
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_xss_payload_handled(self):
        """Test XSS payloads are handled safely."""
        with patch('app.routes.chat.get_ai_response', return_value='Safe response'):
            response = self.app.post('/chat',
                json={'message': '<script>alert("xss")</script>'},
                content_type='application/json')
            self.assertIn(response.status_code, [200, 400])
    
    def test_path_traversal_handled(self):
        """Test path traversal attempts are handled."""
        response = self.app.get('/../../../etc/passwd')
        self.assertIn(response.status_code, [404, 400])

class TestInputSanitization(unittest.TestCase):
    """Tests for input sanitization."""
    
    def setUp(self):
        with patch('vertexai.init'), patch('vertexai.generative_models.GenerativeModel'):
            from app import app as application
            self.app = application.test_client()
    
    def test_null_byte_in_message(self):
        """Test null byte injection is handled."""
        with patch('app.routes.chat.get_ai_response', return_value='Safe'):
            response = self.app.post('/chat',
                json={'message': 'test\x00message'},
                content_type='application/json')
            self.assertIn(response.status_code, [200, 400])
    
    def test_unicode_normalization(self):
        """Test Unicode messages are handled correctly."""
        with patch('app.routes.chat.get_ai_response', return_value='Safe'):
            response = self.app.post('/chat',
                json={'message': 'வாக்குப்பதிவு என்றால் என்ன?'},
                content_type='application/json')
            self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
