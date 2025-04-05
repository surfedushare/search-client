import unittest

from search_client.opensearch.indices.utils import prepare_suggest_completion


class TestPrepareCompletionSuggest(unittest.TestCase):

    def test_removes_non_alpha_chars(self):
        """Test that non-alphabetic characters are removed."""
        result = prepare_suggest_completion("hello123", "world!")
        self.assertEqual(result, ["hello", "world"])

    def test_handles_empty_strings(self):
        """Test that empty strings work properly."""
        result = prepare_suggest_completion("", "test")
        self.assertEqual(result, ["", "test"])

    def test_handles_no_input(self):
        """Test that no input returns an empty list."""
        result = prepare_suggest_completion()
        self.assertEqual(result, [])

    def test_removes_accents(self):
        """Test that accents are removed correctly."""
        result = prepare_suggest_completion("résumé", "café")
        self.assertEqual(result, ["resume", "cafe"])

    def test_multiple_texts(self):
        """Test with multiple text inputs with mixed characters."""
        result = prepare_suggest_completion("Hello!", "Привет", "Olá-123", "żółć")
        self.assertEqual(result, ["Hello", "Privet", "Ola", "zolc"])
