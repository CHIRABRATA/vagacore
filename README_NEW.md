<div align="center">

# 🚀 VagaCore

### Intelligent NLP-Based Text Compression & Fact Extraction Engine

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Version](https://img.shields.io/badge/version-1.0.1-green.svg)](https://github.com/CHIRABRATA/vagacore)

**Transform messy, multi-sentence text into structured, time-aware facts for RAG, analytics, and automation.**

[Features](#-features) • [Installation](#-installation) • [Quick Start](#-quick-start) • [Documentation](#-documentation) • [Contributing](#-contributing)

</div>

---

## 📖 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage Examples](#-usage-examples)
- [Architecture](#-architecture)
- [API Reference](#-api-reference)
- [Testing](#-testing)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🎯 Overview

**VagaCore** is a production-ready NLP pipeline that converts unstructured text into structured, queryable facts. Built on spaCy, it combines Named Entity Recognition (NER), dependency parsing, rule-based extraction, and context memory to deliver financial-grade accuracy without hallucinations.

### Why VagaCore?

- **🎯 High Precision**: Financial-grade extraction with proper handling of MONEY, PERCENT, and DATE entities
- **🧠 Context-Aware**: Maintains context across sentences, resolving pronouns and implicit time references
- **🛡️ Hallucination-Free**: Rule-based guards skip negated/hypothetical statements
- **📊 Multi-Format Output**: JSON (API-friendly), Text (human-readable), or LLM (AI-optimized)
- **⚡ Production-Ready**: Deterministic, no external APIs, designed for high-throughput scenarios

---

## ✨ Features

### Core Capabilities

| Feature | Description |
|---------|-------------|
| **Financial-Grade Extraction** | Preserves units (M/B/k/%), handles corrections, maintains numeric precision |
| **Entity Hygiene** | Resolves possessives ("Nvidia's revenue" → Nvidia), compounds, and generic subjects |
| **Context Memory** | Propagates time and entities across sentences; resolves "the company", "it", etc. |
| **Smart Pairing** | Handles "respectively", parallel lists, and key:value formats |
| **Negation/Hypothetical Filtering** | Automatically skips "if", "would", "didn't", "won't" statements |
| **Deduplication** | Merges conflicting facts, keeps highest confidence values |

### Advanced Features

- ✅ Multi-sentence processing with sentence-level context
- ✅ Compound subject resolution ("Apple's iPhone revenue" → Apple)
- ✅ Numeric correction handling ("initially $10M, later corrected to $15M")
- ✅ List parsing with alignment ("Netflix and Disney reported $1B and $2B respectively")
- ✅ Time propagation ("Q3 2024... The profit increased by 15%")
- ✅ Three output modes: JSON, Text, LLM

---

## 🔧 Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Step 1: Clone or Download

```bash
git clone https://github.com/CHIRABRATA/vagacore.git
cd vagacore
```

### Step 2: Create Virtual Environment

```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -U pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

### Step 4: Install VagaCore

```bash
pip install .
```

### Verify Installation

```bash
python -c "from vagacore import compress; print('VagaCore installed successfully!')"
```

---

## 🚀 Quick Start

### Basic Example

```python
from vagacore import compress

text = """
Apple reported $81.8 billion in revenue for Q3 2024.
The profit increased by 15% in the same quarter.
Netflix and Disney reported $1B and $2B respectively.
"""

# Extract facts as JSON
result = compress(text, mode="json")
print(result)
```

### Output

```json
{
  "facts": [
    {
      "entity": "Apple",
      "event": "reported",
      "value": "$81.8 billion",
      "time": "Q3 2024",
      "confidence": 0.9
    },
    {
      "entity": "Apple",
      "event": "increased",
      "value": "15%",
      "time": "Q3 2024",
      "confidence": 0.85
    },
    {
      "entity": "Netflix",
      "event": "reported",
      "value": "$1B",
      "time": null,
      "confidence": 0.9
    },
    {
      "entity": "Disney",
      "event": "reported",
      "value": "$2B",
      "time": null,
      "confidence": 0.9
    }
  ],
  "version": "1.0.1"
}
```

---

## 📚 Usage Examples

### Example 1: Financial News Extraction

```python
from vagacore import compress

text = """
Tesla announced Q4 2023 revenue of $25.17 billion.
The company's automotive revenue grew by 1% year-over-year.
Energy generation and storage revenue increased by 10%.
"""

facts = compress(text, mode="json")
# Returns structured facts with proper entity, value, time alignment
```

### Example 2: Context Memory

```python
text = """
Microsoft reported strong earnings in Q1 2024.
The company's cloud division grew by 30%.
It also announced a new AI initiative.
"""

facts = compress(text, mode="json")
# "The company" and "It" are resolved to "Microsoft"
# Time "Q1 2024" propagates to subsequent facts
```

### Example 3: Negation Filtering

```python
text = """
Amazon earned $150 billion in 2023.
If Amazon expands to Mars, it could earn $1 trillion.
Amazon did not acquire SpaceX.
"""

facts = compress(text, mode="json")
# Only the first fact is extracted
# Hypothetical and negated statements are automatically filtered
```

### Example 4: Output Modes

```python
text = "Apple's revenue reached $100B in Q3 2024."

# JSON mode (API-friendly)
json_output = compress(text, mode="json")

# Text mode (human-readable)
text_output = compress(text, mode="text")
# Output: "Apple reported revenue of $100B in Q3 2024."

# LLM mode (optimized for AI context)
llm_output = compress(text, mode="llm")
# Output: "Apple|revenue|$100B|Q3 2024"
```

---

## 🏗️ Architecture

### Data Flow Pipeline

```mermaid
flowchart TD
    A[Raw Text Input] --> B[Text Cleaning]
    B --> C[spaCy NLP Parser<br/>NER + POS + Dependencies]
    C --> D[Validation Guards<br/>Negation + Hypothetical Filters]
    D --> E[Entity Extractor<br/>SVO + Values + Time]
    E --> F[Pairing & Lists<br/>Respectively + Parallel + Key:Value]
    F --> G[Context Memory<br/>Time + Entity Propagation]
    G --> H[Deduplication<br/>Confidence Scoring]
    H --> I[Output Formatter<br/>JSON | Text | LLM]
```

### Module Structure

```
vagacore/
├── __init__.py          # Package exports and version
├── parser.py            # spaCy model loading and parsing
├── utils.py             # Text cleaning and noise filtering
├── extractor.py         # SVO extraction, entity validation, guards
└── compressor.py        # Orchestration, context memory, formatting
```

| Module | Responsibility |
|--------|---------------|
| **parser.py** | Loads spaCy model, parses sentences into NLP docs |
| **utils.py** | Text cleaning, noise filtering, preprocessing |
| **extractor.py** | Extracts SVO triples, validates entities, filters negation/hypotheticals |
| **compressor.py** | Orchestrates pipeline, manages context memory, deduplicates facts |

---

## 📖 API Reference

### `compress(text, mode="json")`

Main extraction function that processes text and returns structured facts.

**Parameters:**

- `text` (str): Input text to process (can be multi-sentence)
- `mode` (str): Output format - `"json"`, `"text"`, or `"llm"` (default: `"json"`)

**Returns:**

- **JSON mode**: Dictionary with `{"facts": [...], "version": "1.0.1"}`
- **Text mode**: Human-readable string of facts
- **LLM mode**: Compact pipe-separated strings

**Example:**

```python
from vagacore import compress

result = compress("Tesla earned $25B in Q4 2023.", mode="json")
```

---

## 🧪 Testing

### Run Unit Tests

```bash
# Run all tests
python test_phase4.py
python test_advanced_phase4.py
python test_comprehensive_phase4.py

# Run example demos
python examples/demo.py
python examples/advanced_demo.py
python examples/test_script.py
```

### Test Coverage

The test suite covers:

- ✅ Context memory propagation
- ✅ Multi-sentence processing
- ✅ Financial value extraction
- ✅ Negation/hypothetical filtering
- ✅ Entity resolution and deduplication
- ✅ List and pairing alignment
- ✅ All output modes

---

## 🤝 Contributing

We welcome contributions! Here's how you can help improve VagaCore:

### How to Contribute

1. **Fork the Repository**
   ```bash
   git clone https://github.com/CHIRABRATA/vagacore.git
   cd vagacore
   ```

2. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Set Up Development Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or .\venv\Scripts\activate on Windows
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   pip install -e .
   ```

4. **Make Your Changes**
   - Write clean, documented code
   - Follow existing code style and patterns
   - Add tests for new features
   - Update documentation as needed

5. **Test Your Changes**
   ```bash
   # Run existing tests
   python test_phase4.py
   python test_advanced_phase4.py
   
   # Add new tests for your feature
   # Test with examples
   python examples/demo.py
   ```

6. **Commit Your Changes**
   ```bash
   git add .
   git commit -m "feat: add your feature description"
   ```
   
   **Commit Message Guidelines:**
   - `feat:` for new features
   - `fix:` for bug fixes
   - `docs:` for documentation changes
   - `test:` for test additions/changes
   - `refactor:` for code refactoring

7. **Push and Create Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub with:
   - Clear description of changes
   - Why the change is needed
   - Any breaking changes
   - Test results

### Areas for Contribution

We especially welcome contributions in these areas:

- 🐛 **Bug Fixes**: Report or fix issues
- ✨ **New Features**: Entity types, extraction patterns, output formats
- 📝 **Documentation**: Tutorials, examples, API docs
- 🧪 **Tests**: Additional test cases and edge cases
- ⚡ **Performance**: Optimization and efficiency improvements
- 🌍 **Internationalization**: Support for other languages

### Development Guidelines

- **Code Quality**: Write clean, readable code with comments
- **Testing**: All new features must include tests
- **Documentation**: Update README and docstrings for new features
- **Compatibility**: Ensure Python 3.8+ compatibility
- **Dependencies**: Minimize new dependencies; justify if needed

### Reporting Issues

Found a bug? Have a feature request?

1. Check [existing issues](https://github.com/CHIRABRATA/vagacore/issues)
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce (for bugs)
   - Expected vs actual behavior
   - Python version and environment details
   - Code samples demonstrating the issue

### Code Review Process

1. All submissions require review
2. Maintainers will review PRs within 1 week
3. Address review feedback promptly
4. Once approved, maintainers will merge

### Community

- 💬 **Discussions**: Share ideas, ask questions
- 📧 **Contact**: Reach out to maintainers for guidance
- ⭐ **Star the repo**: Show your support!

---

## 📜 License

This project is licensed under the **MIT License** - see below for details:

```
MIT License

Copyright (c) 2024 THE CHIRABRATA

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 🙏 Acknowledgments

- Built with [spaCy](https://spacy.io/) - Industrial-strength NLP
- Developed by **THE CHIRABRATA**
- Inspired by the need for accurate, hallucination-free fact extraction

---

## 📊 Project Status

- ✅ **Stable**: Version 1.0.1
- ✅ **Production-Ready**: Used in real-world applications
- ✅ **Actively Maintained**: Regular updates and bug fixes

---

## 📞 Support

- 📧 **Email**: Create an issue on GitHub
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/CHIRABRATA/vagacore/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/CHIRABRATA/vagacore/discussions)

---

## 🌟 Changelog

### Version 1.0.1 (Current)
- 🔧 Money regex hardening and unit preservation
- 🎯 Possessive/compound subject priority refinement
- 🧠 Subject memory for generic references ("the company", "it")
- 📦 Package structure improvements

### Version 1.0.0
- ✅ Initial production release
- 🛡️ Negation/hypothetical filtering
- 📋 List and pairing support
- 🔄 Context memory system
- 📊 Multi-format output (JSON/Text/LLM)

---

<div align="center">

**Made with ❤️ by THE CHIRABRATA**

[⭐ Star this repo](https://github.com/CHIRABRATA/vagacore) • [🐛 Report Bug](https://github.com/CHIRABRATA/vagacore/issues) • [💡 Request Feature](https://github.com/CHIRABRATA/vagacore/issues)

</div>
