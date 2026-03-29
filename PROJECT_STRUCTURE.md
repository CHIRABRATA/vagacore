"""
VagaCore Project Structure & Documentation

VagaCore/
├── 📄 README.md                  # Comprehensive project documentation
├── 📄 __init__.py                # Package initialization
│
├── 📂 Core Modules/
│   ├── parser.py                 # spaCy NLP initialization & parsing
│   ├── extractor.py              # SVO extraction, NER, details extraction
│   ├── utils.py                  # Noise removal & text preprocessing
│   └── compressor.py             # Main pipeline with context memory
│
├── 📂 Examples/
│   ├── demo.py                   # Beautiful demonstration script
│   ├── advanced_demo.py           # Multiple scenarios showcase
│   ├── test_context.py            # Context memory tests
│   ├── test_context2.py           # Temporal propagation demos  
│   └── test_context3.py           # RAG scenario examples
│
├── 📂 Virtual Environment/
│   └── venv/                     # Python dependencies (spacy, etc.)
│
└── 📂 Supporting Files/
    └── requirements.txt          # Python package requirements

═══════════════════════════════════════════════════════════════════════════════

MODULE RESPONSIBILITIES:

parser.py
---------
Purpose: NLP Foundation
- Loads spaCy English model (en_core_web_sm)
- Provides parse_text() function
- Handles tokenization, POS tagging, dependency parsing, NER

Key Functions:
- parse_text(text) -> spaCy Doc object

────────────────────────────────────────────────────────────────────────────────

extractor.py
------------
Purpose: Intelligent Fact Extraction
- Implements hybrid NER + rule-based extraction
- Custom subject-verb-object extraction with intelligent filtering
- Named entity recognition and organization by type
- Domain-aware detail extraction

Key Functions:
- extract_svo(doc) -> (subject, verb, object)
- extract_entities(doc) -> [(entity_text, entity_type), ...]
- extract_entities_by_type(doc) -> {entity_type: [entities]}
- extract_details(doc) -> (value, time, entity)

────────────────────────────────────────────────────────────────────────────────

utils.py
--------
Purpose: Text Preprocessing
- Removes linguistic noise while preserving semantics
- Filters adjectives, adverbs, and generic stop words
- Preserves important prepositions for relationship maintenance

Key Functions:
- remove_noise(doc) -> cleaned_text

────────────────────────────────────────────────────────────────────────────────

compressor.py
-----------
Purpose: Main Pipeline & Context Management
- Orchestrates all extraction components
- Implements context memory for temporal propagation
- Handles multi-sentence documents
- Produces clean structured JSON output

Key Functions:
- compress(text) -> [fact_dict, ...]
  Where fact_dict = {
    "subject": str,
    "action": str,
    "object": str,
    "entity": str,
    "value": str,
    "time": str
  }

═══════════════════════════════════════════════════════════════════════════════

PIPELINE FLOW:

Raw Text Input
    ↓
[parser.py] → Tokenize, POS tag, parse dependencies, recognize entities
    ↓
[utils.py] → Remove noise while preserving semantics
    ↓
[extractor.py] → Extract SVO, details, entities using hybrid methods
    ↓
[compressor.py] → Apply context memory, propagate temporal info
    ↓
Structured JSON Output

═══════════════════════════════════════════════════════════════════════════════

RUNNING THE SYSTEM:

1. Simple Demo:
   python examples/demo.py

2. Advanced Demos:
   python examples/advanced_demo.py

3. Programmatic Usage:
   from compressor import compress
   facts = compress("Your text here")
   import json
   print(json.dumps(facts, indent=2))

═══════════════════════════════════════════════════════════════════════════════

KEY CONCEPTS:

1. Hybrid Extraction
   - ML Path: spaCy NER identifies PERCENT, MONEY, DATE, ORG, LOC
   - Rule Path: Dependency parsing finds grammatical patterns
   - Combined: Best of both statistical and symbolic approaches

2. Context Memory
   - Tracks temporal information as sentences are processed
   - Sentences without explicit time inherit from previous
   - Prevents information loss in temporal reasoning

3. Noise Removal
   - Filters subjective language (adjectives, adverbs)
   - Preserves semantic relationships
   - Improves parsing accuracy without data loss

4. Named Entity Recognition
   - PERCENT: 10%, 25%
   - MONEY: $500 million, €1 billion
   - DATE: Q3 2024, January 2024
   - ORG: Apple, Microsoft, Google
   - PERSON: John Smith, CEO names
   - LOC: Asia-Pacific, Europe, country names

═══════════════════════════════════════════════════════════════════════════════

VERSION HISTORY:

v0.1 - Basic multi-sentence support
v0.2 - Noise removal (adjectives/adverbs)
v0.3 - Named Entity Recognition integration
v0.4 - Fixed extraction logic (entity priority, object filtering)
v0.5 - Context memory & temporal propagation (CURRENT)

═══════════════════════════════════════════════════════════════════════════════
"""

if __name__ == "__main__":
    print(__doc__)
