# 💬 Quote Generator

A simple yet elegant Python CLI tool that displays random inspirational quotes. Built to practice Python fundamentals, JSON handling, and professional project documentation.

![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-success)

---

## About

This project demonstrates clean code organization, proper error handling, and comprehensive testing in Python. It features an interactive CLI for browsing inspirational quotes with category filtering.

**Key Features:**
- 30+ curated inspirational quotes
- Random quote selection
- Category filtering (Motivational, Philosophical)
- Flexible selection by number or name
- Clean interface with automatic screen clearing
- Comprehensive unit and integration tests

---

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/Yorss21/quote_generator.git
cd quote-generator
```

### 2. (Optional) Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate   # On Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

---

## Usage

Run the Quote Generator:

```bash
python3 src/quote_generator.py
```

### Menu Options

1. **Get a random quote** - Display a random quote
2. **Get a quote by category** - Filter by category (enter number or name)
3. **View all categories** - See available categories and counts
4. **Exit** - Close the program

---

## Project Structure
To view the project structure, use the tree command:

```bash
tree
```

**Don't have tree installed?**
```bash
# On macOS (with Homebrew)
brew install tree

# On Ubuntu/Debian
sudo apt-get install tree

# On Amazon Linux/RHEL/CentOS
sudo yum install tree
```


---

## Running Tests

Install test dependencies:
```bash
pip install pytest pytest-cov
```

Run all tests:
```bash
pytest tests/
```

Run with coverage report:
```bash
pytest --cov=src tests/
```

---

## Technologies Used

- **Python 3.9+** - Core programming language
- **JSON** - Data storage format
- **pytest** - Testing framework
- **Git/GitHub** - Version control

---

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Author

**Jorge Cruz**

- GitHub: [@Yorss21](https://github.com/Yorss21)

---

**⭐ If you found this project helpful, please consider giving it a star on GitHub!**