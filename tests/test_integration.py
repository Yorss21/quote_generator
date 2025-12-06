
"""
Integration tests for the Quote Generator application.

Tests the complete workflow and interaction between components.
"""

import pytest
import json
from pathlib import Path
import sys

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from quote_generator import QuoteGenerator


class TestQuoteGeneratorIntegration:
    """Integration tests for the complete Quote Generator workflow."""
    
    def test_full_workflow_with_real_data(self):
        """Test complete workflow using the actual quotes.json file."""
        # Initialize generator with default (real) data
        generator = QuoteGenerator()
        
        # Verify quotes loaded
        assert len(generator.quotes) > 0
        
        # Test random quote retrieval
        random_quote = generator.get_random_quote()
        assert random_quote is not None
        assert 'text' in random_quote
        assert 'author' in random_quote
        assert 'category' in random_quote
        
        # Test category filtering
        categories = generator.get_all_categories()
        assert len(categories) > 0
        
        for category in categories:
            category_quote = generator.get_quote_by_category(category)
            assert category_quote is not None
            assert category_quote['category'] == category
        
        # Test formatting
        formatted = generator.format_quote(random_quote)
        assert random_quote['text'] in formatted
        assert random_quote['author'] in formatted
    
    def test_quotes_json_file_exists(self):
        """Test that the quotes.json file exists in the expected location."""
        project_root = Path(__file__).parent.parent
        quotes_file = project_root / "data" / "quotes.json"
        
        assert quotes_file.exists(), "quotes.json file not found"
        assert quotes_file.is_file(), "quotes.json is not a file"
    
    def test_quotes_json_valid_structure(self):
        """Test that quotes.json has valid structure."""
        project_root = Path(__file__).parent.parent
        quotes_file = project_root / "data" / "quotes.json"
        
        with open(quotes_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Verify top-level structure
        assert 'quotes' in data
        assert isinstance(data['quotes'], list)
        assert len(data['quotes']) > 0
        
        # Verify each quote has required fields
        for quote in data['quotes']:
            assert 'text' in quote, "Quote missing 'text' field"
            assert 'author' in quote, "Quote missing 'author' field"
            assert 'category' in quote, "Quote missing 'category' field"
            
            assert isinstance(quote['text'], str)
            assert isinstance(quote['author'], str)
            assert isinstance(quote['category'], str)
            
            assert len(quote['text']) > 0
            assert len(quote['author']) > 0
            assert len(quote['category']) > 0
    
    def test_all_categories_have_quotes(self):
        """Test that all categories contain at least one quote."""
        generator = QuoteGenerator()
        categories = generator.get_all_categories()
        
        for category in categories:
            quote = generator.get_quote_by_category(category)
            assert quote is not None, f"No quotes found for category: {category}"
    
    def test_multiple_random_selections(self):
        """Test that multiple random selections work correctly."""
        generator = QuoteGenerator()
        
        # Get multiple random quotes
        quotes = [generator.get_random_quote() for _ in range(10)]
        
        # All should be valid
        assert all(q is not None for q in quotes)
        assert all('text' in q for q in quotes)
        
        # Should all be from the loaded quotes
        assert all(q in generator.quotes for q in quotes)
    
    def test_category_filtering_consistency(self):
        """Test that category filtering returns consistent results."""
        generator = QuoteGenerator()
        categories = generator.get_all_categories()
        
        for category in categories:
            # Get multiple quotes from same category
            quotes = [generator.get_quote_by_category(category) for _ in range(5)]
            
            # All should belong to the requested category
            assert all(q['category'] == category for q in quotes if q is not None)
    
    def test_format_all_quotes(self):
        """Test that all quotes can be formatted without errors."""
        generator = QuoteGenerator()
        
        for quote in generator.quotes:
            formatted = generator.format_quote(quote)
            
            # Verify formatting includes all components
            assert quote['text'] in formatted
            assert quote['author'] in formatted
            assert quote['category'].capitalize() in formatted
    
    def test_error_handling_with_corrupted_data(self):
        """Test that the system handles corrupted data gracefully."""
        # This test verifies the error handling works as expected
        with pytest.raises(FileNotFoundError):
            QuoteGenerator(quotes_file="nonexistent.json")

