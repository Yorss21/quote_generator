"""
Quote Generator - A simple CLI tool for displaying random inspirational quotes.

This module provides functionality to load quotes from a JSON file,
select random quotes, and display them in a formatted manner.
"""

import json
import random
import os
from pathlib import Path
from typing import List, Dict, Optional
import platform

def clear_screen():
    """Clear the terminal screen based on the operating system."""
    # For Windows
    if platform.system() == "Windows":
        os.system('cls')
    # For macOS and Linux
    else:
        os.system('clear')

class QuoteGenerator:
    """Main class for managing and displaying quotes."""
    
    def __init__(self, quotes_file: str = None):
        """
        Initialize the QuoteGenerator.
        
        Args:
            quotes_file: Path to the JSON file containing quotes.
                        If None, uses default path.
        """
        if quotes_file is None:
            # Get the project root directory (parent of src/)
            project_root = Path(__file__).parent.parent
            quotes_file = project_root / "data" / "quotes.json"
        
        self.quotes_file = quotes_file
        self.quotes = []
        self.load_quotes()
    
    def load_quotes(self) -> None:
        """
        Load quotes from the JSON file.
        
        Raises:
            FileNotFoundError: If the quotes file doesn't exist.
            json.JSONDecodeError: If the JSON file is malformed.
        """
        try:
            with open(self.quotes_file, 'r', encoding='utf-8') as file:
                data = json.load(file)
                self.quotes = data.get('quotes', [])
                
            if not self.quotes:
                print("Warning: No quotes found in the file.")
        
        except FileNotFoundError:
            raise FileNotFoundError(
                f"Quotes file not found: {self.quotes_file}"
                "Please ensure the data/quotes.json file exists."
            )
        except json.JSONDecodeError as e:
            raise json.JSONDecodeError(
                f"Invalid JSON in quotes file: {e.msg}",
                e.doc,
                e.pos
            )
    
    def get_random_quote(self) -> Optional[Dict[str, str]]:
        """
        Get a random quote from the loaded quotes.
        
        Returns:
            A dictionary containing the quote, author, and category,
            or None if no quotes are available.
        """
        if not self.quotes:
            return None
        return random.choice(self.quotes)
    
    def get_quote_by_category(self, category: str) -> Optional[Dict[str, str]]:
        """
        Get a random quote from a specific category.
        
        Args:
            category: The category to filter by (e.g., 'motivational', 'philosophical').
        
        Returns:
            A dictionary containing the quote, author, and category,
            or None if no quotes match the category.
        """
        filtered_quotes = [
            quote for quote in self.quotes 
            if quote.get('category', '').lower() == category.lower()
        ]
        
        if not filtered_quotes:
            return None
        return random.choice(filtered_quotes)
    
    def get_all_categories(self) -> List[str]:
        """
        Get a list of all unique categories in the quotes.
        
        Returns:
            A sorted list of category names.
        """
        categories = set(quote.get('category', 'unknown') for quote in self.quotes)
        return sorted(categories)
    
    def format_quote(self, quote: Dict[str, str]) -> str:
        """
        Format a quote for display.
        
        Args:
            quote: Dictionary containing 'text', 'author', and 'category'.
        
        Returns:
            A formatted string representation of the quote.
        """
        if not quote:
            return "No quote available."
        
        text = quote.get('text', 'Unknown quote')
        author = quote.get('author', 'Unknown')
        category = quote.get('category', 'unknown')
        
        return f"""
"{text}"

— {author}
[{category.capitalize()}]
"""


def display_menu() -> None:
    """Display the main menu options."""
    print("" + "="*50)
    print("  QUOTE GENERATOR")
    print("="*50)
    print("1. Get a random quote")
    print("2. Get a quote by category")
    print("3. View all categories")
    print("4. Exit")
    print("" + "="*50)


def main():
    """Main function to run the Quote Generator CLI."""
    try:
        generator = QuoteGenerator()
        clear_screen()
        print("Welcome to Quote Generator!")
        print(f"Loaded {len(generator.quotes)} quotes.\n")

        while True:
            display_menu()
            choice = input("\nEnter your choice (1-4): ").strip()

            if choice == '1':
                clear_screen()
                quote = generator.get_random_quote()
                print(generator.format_quote(quote))

            elif choice == '2':
                clear_screen()
                categories = generator.get_all_categories()
                print("Available categories: ")
                for i, cat in enumerate(categories, 1):
                    print(f"  {i}. {cat.capitalize()}")
                cat_input = input("Enter category number or name: ").strip()
                # Try to parse as number first
                selected_category = None
                try:
                    cat_number = int(cat_input)
                    if 1 <= cat_number <= len(categories):
                        selected_category = categories[cat_number - 1]
                    else:
                        print(f"Invalid number. Please enter a number between 1 and {len(categories)}.")
                except ValueError:
                    # If not a number, treat as category name
                    selected_category = cat_input
                if selected_category:
                    clear_screen()
                    quote = generator.get_quote_by_category(selected_category)
                    if quote:
                        print(generator.format_quote(quote))
                    else:
                        print(f"No quotes found for category: {selected_category}")

            elif choice == '3':
                clear_screen()
                categories = generator.get_all_categories()
                print("Available categories:")
                for cat in categories:
                    count = sum(1 for q in generator.quotes if q.get('category') == cat)
                    print(f"  • {cat.capitalize()} ({count} quotes)")

            elif choice == '4':
                clear_screen()
                print("Thanks for using Quote Generator! Stay inspired!\n\n")
                break
            else:
                clear_screen()
                print("Invalid choice. Please enter a number between 1 and 4.")
            input("\nPress Enter to continue...")
            clear_screen()

    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format in quotes file.")
        return 1
    except KeyboardInterrupt:
        print("Goodbye!")
        return 0

    return 0



if __name__ == "__main__":
    exit(main())

