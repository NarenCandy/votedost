"""Accessibility tests for VoteDost HTML structure."""
import unittest
from unittest.mock import patch
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestHTMLAccessibility(unittest.TestCase):
    """Tests for HTML accessibility standards."""
    
    def setUp(self):
        with patch('vertexai.init'), patch('vertexai.generative_models.GenerativeModel'):
            from app import app as application
            self.app = application.test_client()
        self.html = self.app.get('/').data.decode()
    
    def test_skip_link_present(self):
        """Skip navigation link must be present."""
        self.assertIn('skip-link', self.html)
    
    def test_main_landmark_present(self):
        """Main landmark must be present."""
        self.assertIn('role="main"', self.html)
    
    def test_navigation_landmark_present(self):
        """Navigation landmark must be present."""
        self.assertIn('role="navigation"', self.html)
    
    def test_aria_labels_on_interactive_elements(self):
        """All interactive elements must have aria-labels."""
        self.assertIn('aria-label=', self.html)
    
    def test_lang_attribute_on_html(self):
        """HTML element must have lang attribute."""
        self.assertIn('lang="en"', self.html)
    
    def test_aria_live_regions_present(self):
        """Aria live regions must be present for dynamic content."""
        self.assertIn('aria-live=', self.html)
    
    def test_roles_present(self):
        """ARIA roles must be present throughout."""
        self.assertIn('role=', self.html)

if __name__ == '__main__':
    unittest.main()
