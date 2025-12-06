
"""
Unit tests for the Quote Generator module.

Tests individual functions and methods in isolation.
"""

import pytest
import json
import tempfile
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from quote_generator import QuoteGenerator


@pytest.fixture
def sample_quotes_data():
    """Fixture providing sample quotes data for testing."""
    return {
        "quotes": [
            {
                "text": "Test quote 1",
                "author": "Test Author 1",
                "category": "motivational"
            },
            {
                "text": "Test quote 2",
                "author": "Test Author 2",
                "category": "philosophical"
            },
            {
                "text": "Test quote 3",
                "author": "Test Author 3",
                "category": "motivational"
            }
        ]
    }


@pytest.fixture
def temp_quotes_file(sample_quotes_data):
    """Fixture creating a temporary quotes JSON file."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(sample_quotes_data, f)
        temp_path = f.name
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink()


@pytest.fixture
def quote_generator(temp_quotes_file):
    """Fixture providing a QuoteGenerator instance with test data."""
    return QuoteGenerator(quotes_file=temp_quotes_file)


class TestQuoteGeneratorInit:
    """Tests for QuoteGenerator initialization."""
    
    def test_init_with_custom_file(self, temp_quotes_file):
        """Test initialization with a custom quotes file."""
        generator = QuoteGenerator(quotes_file=temp_quotes_file)
        assert generator.quotes_file == temp_quotes_file
        assert len(generator.quotes) == 3
    
    def test_init_with_default_file(self):
        """Test initialization with default quotes file."""
        generator = QuoteGenerator()
        assert generator.quotes_file is not None
        assert len(generator.quotes) > 0


class TestLoadQuotes:
    """Tests for the load_quotes method."""
    
    def test_load_quotes_success(self, quote_generator):
        """Test successful loading of quotes."""
        assert len(quote_generator.quotes) == 3
        assert all('text' in quote for quote in quote_generator.quotes)
        assert all('author' in quote for quote in quote_generator.quotes)
        assert all('category' in quote for quote in quote_generator.quotes)
    
    def test_load_quotes_file_not_found(self):
        """Test handling of missing quotes file."""
        with pytest.raises(FileNotFoundError):
            QuoteGenerator(quotes_file="nonexistent_file.json")
    
    def test_load_quotes_invalid_json(self):
        """Test handling of invalid JSON file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            f.write("{ invalid json }")
            temp_path = f.name
        
        try:
            with pytest.raises(json.JSONDecodeError):
                QuoteGenerator(quotes_file=temp_path)
        finally:
            Path(temp_path).unlink()
    
    def test_load_quotes_empty_quotes_array(self):
        """Test handling of empty quotes array."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"quotes": []}, f)
            temp_path = f.name
        
        try:
            generator = QuoteGenerator(quotes_file=temp_path)
            assert len(generator.quotes) == 0
        finally:
            Path(temp_path).unlink()


class TestGetRandomQuote:
    """Tests for the get_random_quote method."""
    
    def test_get_random_quote_returns_dict(self, quote_generator):
        """Test that get_random_quote returns a dictionary."""
        quote = quote_generator.get_random_quote()
        assert isinstance(quote, dict)
    
    def test_get_random_quote_has_required_fields(self, quote_generator):
        """Test that returned quote has all required fields."""
        quote = quote_generator.get_random_quote()
        assert 'text' in quote
        assert 'author' in quote
        assert 'category' in quote
    
    def test_get_random_quote_from_available_quotes(self, quote_generator):
        """Test that returned quote is from the loaded quotes."""
        quote = quote_generator.get_random_quote()
        assert quote in quote_generator.quotes
    
    def test_get_random_quote_empty_quotes(self):
        """Test get_random_quote with no quotes loaded."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump({"quotes": []}, f)
            temp_path = f.name
        
        try:
            generator = QuoteGenerator(quotes_file=temp_path)
            quote = generator.get_random_quote()
            assert quote is None
        finally:
            Path(temp_path).unlink()


class TestGetQuoteByCategory:
    """Tests for the get_quote_by_category method."""
    
    def test_get_quote_by_category_valid(self, quote_generator):
        """Test getting a quote from a valid category."""
        quote = quote_generator.get_quote_by_category("motivational")
        assert quote is not None
        assert quote['category'] == 'motivational'
    
    def test_get_quote_by_category_case_insensitive(self, quote_generator):
        """Test that category matching is case-insensitive."""
        quote = quote_generator.get_quote_by_category("MOTIVATIONAL")
        assert quote is not None
        assert quote['category'] == 'motivational'
    
    def test_get_quote_by_category_invalid(self, quote_generator):
        """Test getting a quote from a non-existent category."""
        quote = quote_generator.get_quote_by_category("nonexistent")
        assert quote is None
    
    def test_get_quote_by_category_returns_correct_category(self, quote_generator):
        """Test that returned quote matches requested category."""
        quote = quote_generator.get_quote_by_category("philosophical")
        assert quote['category'] == 'philosophical'


class TestGetAllCategories:
    """Tests for the get_all_categories method."""
    
    def test_get_all_categories_returns_list(self, quote_generator):
        """Test that get_all_categories returns a list."""
        categories = quote_generator.get_all_categories()
        assert isinstance(categories, list)
    
    def test_get_all_categories_contains_expected(self, quote_generator):
        """Test that all expected categories are present."""
        categories = quote_generator.get_all_categories()
        assert 'motivational' in categories
        assert 'philosophical' in categories
    
    def test_get_all_categories_sorted(self, quote_generator):
        """Test that categories are returned in sorted order."""
        categories = quote_generator.get_all_categories()
        assert categories == sorted(categories)
    
    def test_get_all_categories_unique(self, quote_generator):
        """Test that categories list contains no duplicates."""
        categories = quote_generator.get_all_categories()
        assert len(categories) == len(set(categories))


class TestFormatQuote:
    """Tests for the format_quote method."""
    
    def test_format_quote_valid(self, quote_generator):
        """Test formatting a valid quote."""
        quote = {
            "text": "Test quote",
            "author": "Test Author",
            "category": "motivational"
        }
        formatted = quote_generator.format_quote(quote)
        
        assert "Test quote" in formatted
        assert "Test Author" in formatted
        assert "Motivational" in formatted
    
    def test_format_quote_none(self, quote_generator):
        """Test formatting None quote."""
        formatted = quote_generator.format_quote(None)
        assert formatted == "No quote available."
    
    def test_format_quote_empty_dict(self, quote_generator):
        """Test formatting empty dictionary."""
        formatted = quote_generator.format_quote({})
        assert "Unknown quote" in formatted
        assert "Unknown" in formatted
    
    def test_format_quote_capitalizes_category(self, quote_generator):
        """Test that category is capitalized in output."""
        quote = {
            "text": "Test",
            "author": "Author",
            "category": "motivational"
        }
        formatted = quote_generator.format_quote(quote)
        assert "Motivational" in formatted
        assert "motivational" not in formatted

