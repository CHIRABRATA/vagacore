# 🚀 VagaCore - Intelligent Text Compression & Fact Extraction Engine

A production-ready NLP system combining Named Entity Recognition (NER), dependency parsing, and context-aware processing for intelligent fact extraction from unstructured text.

## 🎯 Features

### Core Capabilities

- **🧠 Hybrid Extraction**: Combines ML-based NER with rule-based syntax parsing
- **📝 Multi-Sentence Processing**: Handles complex documents with multiple facts
- **🔄 Context Memory**: Maintains temporal awareness across sentences
- **🏢 Named Entity Recognition**: Identifies PERCENT, MONEY, DATE, ORG, PERSON, LOC
- **🎯 Semantic Understanding**: Extracts Subject-Verb-Object patterns with noise removal
- **📊 Structured Output**: Returns clean JSON facts

### Key Innovations

✅ **Context-Aware Extraction**
- Sentences without explicit dates inherit from previous context
- Prevents temporal information loss in multi-sentence documents
- Critical for RAG and knowledge base indexing

✅ **Noise Resistance**
- Removes adjectives and adverbs before processing
- Preserves semantic relationships
- Filters subjective language

✅ **Domain Intelligence**
- Recognizes financial keywords (revenue, profit, earnings, sales)
- Prioritizes domain entities over generic organizations
- Smart quantity filtering (million → context)

## 📊 Example

### Input
```
Apple reported $500 million in revenue during Q3 2024 in the Asia-Pacific region.
The profit increased by 15% in the same period.
```

### Output
```json
[
  {
    "subject": "Apple",
    "action": "report",
    "object": "revenue",
    "entity": "revenue",
    "value": "$500 million",
    "time": "Q3 2024"
  },
  {
    "subject": "profit",
    "action": "increase",
    "object": null,
    "entity": null,
    "value": "15%",
    "time": "Q3 2024"
  }
]
```

## 🏗️ Architecture

```
Input Text
    ↓
┌─────────────────────────────────────┐
│   Parser (spaCy)                    │
│   - Tokenization                    │
│   - POS Tagging                     │
│   - Named Entity Recognition        │
│   - Dependency Parsing              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Noise Removal (Utils)             │
│   - Remove adjectives/adverbs       │
│   - Keep semantic prepositions      │
│   - Filter stop words               │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Hybrid Extraction (Extractor)     │
│                                     │
│   ┌─ ML Path (NER)                 │
│   │  - PERCENT, MONEY              │
│   │  - DATE, TIME                  │
│   │  - ORG, PERSON, LOC            │
│   │                                 │
│   └─ Rule Path (Syntax)             │
│      - Domain keywords              │
│      - Prepositional patterns       │
│      - Subject-Verb-Object          │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│   Context Memory (Compressor)       │
│   - Propagate temporal context      │
│   - Maintain state across sentences │
│   - Prevent information loss        │
└─────────────────────────────────────┘
    ↓
Output: Structured JSON Facts
```

## 📋 Module Overview

### `parser.py`
- Loads spaCy NLP model
- Handles text tokenization and parsing

### `extractor.py`
- **`extract_svo()`**: Subject-Verb-Object extraction with intelligent object selection
- **`extract_entities()`**: Named Entity Recognition with type labels
- **`extract_entities_by_type()`**: Organized entity access by category
- **`extract_details()`**: Hybrid NER + rule-based value/time/entity extraction

### `utils.py`
- **`remove_noise()`**: Removes adjectives/adverbs while preserving semantic relationships

### `compressor.py`
- **`compress()`**: Main pipeline with context memory
- Orchestrates all components
- Implements temporal propagation

## 🚀 Quick Start

### Installation

```bash
cd vagacore
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate # Linux/Mac

pip install spacy
python -m spacy download en_core_web_sm
```

### Basic Usage

```python
from compressor import compress

text = "Apple reported $500 million in revenue during Q3 2024."
result = compress(text)

import json
print(json.dumps(result, indent=2))
```

### Run Demos

```bash
# Simple demo
python examples/demo.py

# Advanced demonstrations
python examples/advanced_demo.py
```

## 🔍 Use Cases

### 1. Retrieval-Augmented Generation (RAG)
Extract structured facts for LLM context:
```python
facts = compress(document_text)
# Feed to LLM for better grounding
```

### 2. Financial Data Extraction
Parse earnings reports and investor documents:
```python
earnings_report = """
Q3 2024 Revenue: $50 million
Operating margin improved by 5%
"""
facts = compress(earnings_report)
```

### 3. Knowledge Base Indexing
Create temporally-aware fact databases:
```python
for document in documents:
    facts = compress(document)
    # Index with time-based grouping
```

### 4. News Analysis
Extract named entities and facts from articles:
```python
article = get_news_article()
entities = compress(article)
```

## 📈 Performance

### What It Handles Well ✅

- Multi-sentence documents
- Temporal references and quarters
- Financial terminology
- Organization names and locations
- Percentage and monetary values
- Contextual pronouns via memory

### Current Limitations ⚠️

- Single main action per sentence
- Simple clause structures work best
- Passive voice sometimes reduced accuracy
- Requires English text

## 🔬 Technical Details

### Extraction Methods

**NER (Named Entity Recognition)**
- Uses spaCy's trained model
- Entity types: PERCENT, MONEY, DATE, ORG, PERSON, GPE, LOC
- Confidence-based extraction

**Dependency Parsing**
- Identifies grammatical relationships
- Key patterns:
  - `nsubj`: Nominal subject
  - `ROOT`: Root verb
  - `dobj`: Direct object
  - `pobj`: Object of preposition
  - `attr`: Predicate attribute

**Context Memory Algorithm**
```
for each sentence:
    extract time from sentence
    if time is None or vague:
        use previous_time
    else:
        update previous_time
```

## 🎓 Learning Resources

- **NLP Basics**: The extraction uses fundamental NLP concepts
- **spaCy**: Learn at https://spacy.io
- **Dependency Parsing**: https://en.wikipedia.org/wiki/Dependency_grammar
- **Context in LLMs**: Essential for RAG systems

## 🤝 Contributing

This is a demonstration project. However, potential improvements:

- [ ] Multi-action sentence support
- [ ] Improved passive voice handling
- [ ] Custom entity type definitions
- [ ] Confidence scoring for facts
- [ ] Multi-language support

## 📄 License

Open source - use freely for learning and development

## 🙌 Acknowledgments

Built with:
- **spaCy**: Industrial-strength NLP
- **Python**: Core language
- **NER Technology**: Modern entity recognition

---

**VagaCore v0.5** | Hybrid NER + Rule-Based Extraction | Context-Aware Processing
something
