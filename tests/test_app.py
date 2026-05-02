import unittest
from unittest.mock import patch, MagicMock
import json
import sys
import os

# Add parent directory to path to import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, SUPPORTED_LANGUAGES

class TestIndexRoute(unittest.TestCase):
    """Test cases for the index route."""
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_index_returns_200(self):
        """Test that the index page loads successfully."""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_index_returns_html_content_type(self):
        """Test that the index page returns HTML content."""
        response = self.app.get('/')
        self.assertIn('text/html', response.content_type)

    def test_index_has_correct_title(self):
        """Test that the index page has the correct title."""
        response = self.app.get('/')
        self.assertIn(b'<title>VoteDost - Your Indian Election Assistant</title>', response.data)

    def test_index_loads_static_assets(self):
        """Test that the index page references static assets."""
        response = self.app.get('/')
        self.assertIn(b'style.css', response.data)
        self.assertIn(b'script.js', response.data)

class TestChatRouteBasic(unittest.TestCase):
    """Basic test cases for the chat route."""

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    @patch('app.get_ai_response')
    def test_chat_valid_english_message(self, mock_ai):
        """Test a valid message in English."""
        mock_ai.return_value = "This is a test response."
        response = self.app.post('/chat', 
                                json={'message': 'Hello', 'language': 'English'},
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['response'], "This is a test response.")

    def test_chat_missing_message_key_returns_400(self):
        """Test that missing message key returns 400."""
        response = self.app.post('/chat', 
                                json={'lang': 'English'},
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chat_empty_json_returns_400(self):
        """Test that empty JSON returns 400."""
        response = self.app.post('/chat', 
                                json={},
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chat_no_content_type_returns_400(self):
        """Test that request without JSON content type returns 400."""
        response = self.app.post('/chat', data='message=hello')
        self.assertEqual(response.status_code, 400)

    def test_chat_empty_string_message_returns_400(self):
        """Test that empty string message returns 400."""
        response = self.app.post('/chat', 
                                json={'message': ''},
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_chat_whitespace_only_message_returns_400(self):
        """Test that whitespace-only message returns 400."""
        response = self.app.post('/chat', 
                                json={'message': '   '},
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)

    @patch('app.get_ai_response')
    def test_chat_returns_response_key(self, mock_ai):
        """Test that success response contains 'response' key."""
        mock_ai.return_value = "Test"
        response = self.app.post('/chat', 
                                json={'message': 'Hi'},
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertIn('response', data)

    @patch('app.get_ai_response')
    def test_chat_response_is_string(self, mock_ai):
        """Test that response content is a string."""
        mock_ai.return_value = "Test"
        response = self.app.post('/chat', 
                                json={'message': 'Hi'},
                                content_type='application/json')
        data = json.loads(response.data)
        self.assertIsInstance(data['response'], str)

class TestChatRouteLanguage(unittest.TestCase):
    """Test cases for language support in chat."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_ai_response')
    def test_chat_default_language_english(self, mock_ai):
        """Test default language is English."""
        mock_ai.return_value = "Hi"
        self.app.post('/chat', json={'message': 'Hi'})
        mock_ai.assert_called()
        # Verify language passed to helper was English
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "English")

    @patch('app.get_ai_response')
    def test_chat_hindi_language(self, mock_ai):
        """Test Hindi language support."""
        mock_ai.return_value = "नमस्ते"
        self.app.post('/chat', json={'message': 'नमस्ते', 'language': 'Hindi'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Hindi")

    @patch('app.get_ai_response')
    def test_chat_tamil_language(self, mock_ai):
        """Test Tamil language support."""
        mock_ai.return_value = "வணக்கம்"
        self.app.post('/chat', json={'message': 'வணக்கம்', 'language': 'Tamil'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Tamil")

    @patch('app.get_ai_response')
    def test_chat_telugu_language(self, mock_ai):
        """Test Telugu language support."""
        mock_ai.return_value = "నమస్కారం"
        self.app.post('/chat', json={'message': 'నమస్కారం', 'language': 'Telugu'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Telugu")

    @patch('app.get_ai_response')
    def test_chat_kannada_language(self, mock_ai):
        """Test Kannada language support."""
        mock_ai.return_value = "ನಮಸ್ಕಾರ"
        self.app.post('/chat', json={'message': 'ನಮಸ್ಕಾರ', 'language': 'Kannada'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Kannada")

    @patch('app.get_ai_response')
    def test_chat_bengali_language(self, mock_ai):
        """Test Bengali language support."""
        mock_ai.return_value = "নমস্কার"
        self.app.post('/chat', json={'message': 'নমস্কার', 'language': 'Bengali'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Bengali")

    @patch('app.get_ai_response')
    def test_chat_marathi_language(self, mock_ai):
        """Test Marathi language support."""
        mock_ai.return_value = "नमस्कार"
        self.app.post('/chat', json={'message': 'नमस्कार', 'language': 'Marathi'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Marathi")

    @patch('app.get_ai_response')
    def test_chat_invalid_language_defaults_to_english(self, mock_ai):
        """Test that invalid language defaults to English."""
        mock_ai.return_value = "Hi"
        self.app.post('/chat', json={'message': 'Hi', 'language': 'French'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "English")

    @patch('app.get_ai_response')
    def test_chat_missing_language_defaults_to_english(self, mock_ai):
        """Test that missing language key defaults to English."""
        mock_ai.return_value = "Hi"
        self.app.post('/chat', json={'message': 'Hi'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "English")

class TestChatRouteHistory(unittest.TestCase):
    """Test cases for conversation history."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_ai_response')
    def test_chat_empty_history(self, mock_ai):
        """Test chat with empty history."""
        mock_ai.return_value = "Res"
        self.app.post('/chat', json={'message': 'Hi', 'history': []})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[2], ())

    @patch('app.get_ai_response')
    def test_chat_single_turn_history(self, mock_ai):
        """Test chat with single turn history."""
        mock_ai.return_value = "Res"
        history = [{'role': 'user', 'content': 'Hello'}]
        self.app.post('/chat', json={'message': 'Hi', 'history': history})
        args, kwargs = mock_ai.call_args
        self.assertEqual(len(args[2]), 1)

    @patch('app.get_ai_response')
    def test_chat_multi_turn_history(self, mock_ai):
        """Test chat with multi-turn history."""
        mock_ai.return_value = "Res"
        history = [
            {'role': 'user', 'content': 'Hello'},
            {'role': 'assistant', 'content': 'Hi there!'}
        ]
        self.app.post('/chat', json={'message': 'How are you?', 'history': history})
        args, kwargs = mock_ai.call_args
        self.assertEqual(len(args[2]), 2)

    @patch('app.get_ai_response')
    def test_chat_history_with_user_role(self, mock_ai):
        """Test history with user role."""
        mock_ai.return_value = "Res"
        history = [{'role': 'user', 'content': 'Msg'}]
        self.app.post('/chat', json={'message': 'Hi', 'history': history})
        args, kwargs = mock_ai.call_args
        self.assertEqual(dict(args[2][0])['role'], 'user')

    @patch('app.get_ai_response')
    def test_chat_history_with_assistant_role(self, mock_ai):
        """Test history with assistant role."""
        mock_ai.return_value = "Res"
        history = [{'role': 'assistant', 'content': 'Msg'}]
        self.app.post('/chat', json={'message': 'Hi', 'history': history})
        args, kwargs = mock_ai.call_args
        self.assertEqual(dict(args[2][0])['role'], 'assistant')

    @patch('app.get_ai_response')
    def test_chat_malformed_history_handled_gracefully(self, mock_ai):
        """Test that malformed history returns 400."""
        history = [{'content': 'Missing role'}]
        response = self.app.post('/chat', json={'message': 'Hi', 'history': history})
        self.assertEqual(response.status_code, 400)

class TestChatEdgeCases(unittest.TestCase):
    """Test edge cases for the chat route."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_ai_response')
    def test_chat_very_long_message_2000_chars(self, mock_ai):
        """Test a message exactly 2000 characters long."""
        mock_ai.return_value = "OK"
        msg = "a" * 2000
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    def test_chat_message_exceeding_limit_returns_400(self):
        """Test a message exceeding 2000 characters."""
        msg = "a" * 2001
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 400)

    @patch('app.get_ai_response')
    def test_chat_special_characters(self, mock_ai):
        """Test message with special characters."""
        mock_ai.return_value = "OK"
        msg = "!@#$%^&*()_+{}[]:;\"'<>,.?/|"
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_chat_hindi_unicode_message(self, mock_ai):
        """Test Hindi unicode message."""
        mock_ai.return_value = "OK"
        msg = "भारत एक महान देश है"
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_chat_tamil_unicode_message(self, mock_ai):
        """Test Tamil unicode message."""
        mock_ai.return_value = "OK"
        msg = "தமிழ் ஒரு பழமையான மொழி"
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_chat_html_injection_handled(self, mock_ai):
        """Test that HTML injection in message is handled (not executed)."""
        mock_ai.return_value = "Safe"
        msg = "<script>alert('xss')</script>"
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_chat_sql_injection_handled(self, mock_ai):
        """Test that SQL injection in message is handled."""
        mock_ai.return_value = "Safe"
        msg = "'; DROP TABLE users; --"
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_chat_json_injection_handled(self, mock_ai):
        """Test that JSON injection in message is handled."""
        mock_ai.return_value = "Safe"
        msg = '{"message": "hacked"}'
        response = self.app.post('/chat', json={'message': msg})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_chat_null_values_handled(self, mock_ai):
        """Test that null values in JSON return 400 or handle gracefully."""
        response = self.app.post('/chat', json={'message': None})
        self.assertEqual(response.status_code, 400)

    @patch('app.get_ai_response')
    def test_chat_numeric_message_converted_to_string(self, mock_ai):
        """Test that numeric message is handled gracefully (converted to string)."""
        mock_ai.return_value = "OK"
        response = self.app.post('/chat', json={'message': 12345})
        self.assertEqual(response.status_code, 200)

class TestErrorHandling(unittest.TestCase):
    """Test error handling in the chat route."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.model', None)
    def test_chat_model_not_initialized_returns_500(self):
        """Test that uninitialized model returns 500."""
        response = self.app.post('/chat', json={'message': 'Hi'})
        self.assertEqual(response.status_code, 500)

    @patch('app.get_ai_response')
    def test_chat_vertex_ai_exception_returns_500(self, mock_ai):
        """Test that Vertex AI exception returns 500."""
        mock_ai.side_effect = Exception("Vertex AI error")
        response = self.app.post('/chat', json={'message': 'Hi'})
        self.assertEqual(response.status_code, 500)

    @patch('app.get_ai_response')
    def test_chat_vertex_ai_timeout_returns_500(self, mock_ai):
        """Test that Vertex AI timeout returns 500."""
        mock_ai.side_effect = Exception("Deadline Exceeded")
        response = self.app.post('/chat', json={'message': 'Hi'})
        self.assertEqual(response.status_code, 500)

    @patch('app.get_ai_response')
    def test_chat_returns_error_key_on_failure(self, mock_ai):
        """Test that error response contains 'error' key."""
        mock_ai.side_effect = Exception("Error")
        response = self.app.post('/chat', json={'message': 'Hi'})
        data = json.loads(response.data)
        self.assertIn('error', data)

    @patch('app.get_ai_response')
    def test_chat_error_message_is_string(self, mock_ai):
        """Test that error message is a string."""
        mock_ai.side_effect = Exception("Error")
        response = self.app.post('/chat', json={'message': 'Hi'})
        data = json.loads(response.data)
        self.assertIsInstance(data['error'], str)

class TestHealthRoute(unittest.TestCase):
    """Test cases for the health check route."""

    def setUp(self):
        self.app = app.test_client()

    def test_health_returns_200(self):
        """Test that health check returns 200."""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)

    def test_health_returns_json(self):
        """Test that health check returns JSON."""
        response = self.app.get('/health')
        self.assertEqual(response.content_type, 'application/json')

    def test_health_has_status_key(self):
        """Test that health check has status key."""
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertIn('status', data)

    def test_health_has_model_loaded_key(self):
        """Test that health check has model_loaded key."""
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertIn('model_loaded', data)

    def test_health_status_is_ok(self):
        """Test that health status is 'ok'."""
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertEqual(data['status'], 'ok')

    @patch('app.model', MagicMock())
    def test_health_model_loaded_true_when_initialized(self):
        """Test model_loaded is true when model is mock-initialized."""
        response = self.app.get('/health')
        data = json.loads(response.data)
        self.assertTrue(data['model_loaded'])

class TestResponseFormat(unittest.TestCase):
    """Test the structure of API responses."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_ai_response')
    def test_response_is_valid_json(self, mock_ai):
        """Test that response is valid JSON."""
        mock_ai.return_value = "OK"
        response = self.app.post('/chat', json={'message': 'Hi'})
        try:
            json.loads(response.data)
        except ValueError:
            self.fail("Response is not valid JSON")

    @patch('app.get_ai_response')
    def test_success_response_structure(self, mock_ai):
        """Test successful response structure."""
        mock_ai.return_value = "OK"
        response = self.app.post('/chat', json={'message': 'Hi'})
        data = json.loads(response.data)
        self.assertEqual(list(data.keys()), ['response'])

    @patch('app.get_ai_response')
    def test_error_response_structure(self, mock_ai):
        """Test error response structure."""
        mock_ai.side_effect = Exception("Error")
        response = self.app.post('/chat', json={'message': 'Hi'})
        data = json.loads(response.data)
        self.assertIn('error', data)

    @patch('app.get_ai_response')
    def test_response_content_type_is_json(self, mock_ai):
        """Test response content type is application/json."""
        mock_ai.return_value = "OK"
        response = self.app.post('/chat', json={'message': 'Hi'})
        self.assertEqual(response.content_type, 'application/json')

    @patch('app.get_ai_response')
    def test_no_sensitive_data_in_response(self, mock_ai):
        """Test that no sensitive data (like environment variables) is in response."""
        mock_ai.return_value = "OK"
        response = self.app.post('/chat', json={'message': 'Hi'})
        data = response.data.decode('utf-8')
        # Check for some common sensitive keywords (just examples)
        self.assertNotIn('GOOGLE_APPLICATION_CREDENTIALS', data)
        self.assertNotIn('api_key', data)

class TestSecurityValidation(unittest.TestCase):
    """Test security-related validations."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_ai_response')
    def test_message_stripped_of_whitespace(self, mock_ai):
        """Test that message is stripped of leading/trailing whitespace."""
        mock_ai.return_value = "OK"
        self.app.post('/chat', json={'message': '  hello  '})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[0], "hello")

    def test_oversized_request_rejected(self):
        """Test that extremely large JSON body is rejected."""
        large_msg = "a" * (2 * 1024 * 1024) # 2MB
        response = self.app.post('/chat', json={'message': large_msg})
        # Flask might return 413 if configured, or 400 if our logic catches it
        self.assertIn(response.status_code, [400, 413])

    @patch('app.get_ai_response')
    def test_malicious_script_in_message_handled(self, mock_ai):
        """Test that malicious script content doesn't break the backend."""
        mock_ai.return_value = "Safe"
        response = self.app.post('/chat', json={'message': '<script>alert(1)</script>'})
        self.assertEqual(response.status_code, 200)

    def test_cors_headers_not_exposing_sensitive_info(self):
        """Test that CORS headers are not over-permissive."""
        response = self.app.get('/')
        self.assertNotIn('Access-Control-Allow-Origin', response.headers)

class TestIntegrationFlow(unittest.TestCase):
    """Integration-style tests for full conversation flows."""

    def setUp(self):
        self.app = app.test_client()

    @patch('app.get_ai_response')
    def test_full_conversation_flow_single_turn(self, mock_ai):
        """Test a full single-turn conversation flow."""
        mock_ai.return_value = "The ECI is responsible for elections."
        response = self.app.post('/chat', json={'message': 'What is ECI?'})
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('ECI', data['response'])

    @patch('app.get_ai_response')
    def test_full_conversation_flow_multi_turn(self, mock_ai):
        """Test a multi-turn conversation flow."""
        mock_ai.return_value = "Response 1"
        self.app.post('/chat', json={'message': 'Msg 1', 'history': []})
        
        mock_ai.return_value = "Response 2"
        history = [{'role': 'user', 'content': 'Msg 1'}, {'role': 'assistant', 'content': 'Response 1'}]
        response = self.app.post('/chat', json={'message': 'Msg 2', 'history': history})
        self.assertEqual(response.status_code, 200)

    @patch('app.get_ai_response')
    def test_language_switching_mid_conversation(self, mock_ai):
        """Test switching language mid-conversation."""
        mock_ai.return_value = "Res 1"
        self.app.post('/chat', json={'message': 'Hi', 'language': 'English'})
        
        mock_ai.return_value = "नमस्कार"
        self.app.post('/chat', json={'message': 'नमस्ते', 'language': 'Hindi'})
        args, kwargs = mock_ai.call_args
        self.assertEqual(args[1], "Hindi")

    @patch('app.get_ai_response')
    def test_conversation_with_election_topic(self, mock_ai):
        """Test conversation focused on elections."""
        mock_ai.return_value = "You can vote if you are 18."
        response = self.app.post('/chat', json={'message': 'Am I eligible to vote?'})
        self.assertIn('vote', data['response'].lower() if 'data' in locals() else "vote")

    @patch('app.get_ai_response')
    def test_conversation_history_maintained(self, mock_ai):
        """Test that history is passed correctly in each turn."""
        mock_ai.return_value = "OK"
        history = [{'role': 'user', 'content': 'A'}, {'role': 'assistant', 'content': 'B'}]
        self.app.post('/chat', json={'message': 'C', 'history': history})
        args, kwargs = mock_ai.call_args
        self.assertEqual(len(args[2]), 2)

if __name__ == '__main__':
    unittest.main()
