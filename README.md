# VagaCore 1.0.1 — Production-Ready Fact Extraction

VagaCore is an NLP pipeline that converts messy, multi-sentence text into structured, time-aware facts for RAG, analytics, and automation. It combines spaCy NER, dependency parsing, rule-based guards, and context memory to avoid hallucinations and keep entities, values, and time properly aligned.

---
## Why VagaCore
- Financial-grade extraction: MONEY, PERCENT, DATE with unit preservation (M/B/k) and correction-handling.
- Entity hygiene: possessive/compound owners ("Nvidia's revenue" → Nvidia), noise filters, and generic-subject resolution.
- Context memory: carries forward time and subjects across sentences; skips negated/hypothetical statements.
- List and pairing smarts: handles "respectively", parallel pairs, and key:value list-style lines.
- Safe outputs: skips negated/hypothetical facts and deduplicates conflicting facts.

---


---
## Module Map
- [vagacore/parser.py](vagacore/parser.py): spaCy load and parsing.
- [vagacore/utils.py](vagacore/utils.py): `clean_text`, noise filtering.
- [vagacore/extractor.py](vagacore/extractor.py): SVO, entity validation, value/time extraction, negation/hypothetical guards.
- [vagacore/compressor.py](vagacore/compressor.py): orchestrates sentences, pairing, list fallback, context memory, dedup, formatting.
- [vagacore/__init__.py](vagacore/__init__.py): package export and version.

---
## Installation
```bash
python -m venv venv
./venv/Scripts/activate    # Windows
# source venv/bin/activate # macOS/Linux
pip install -U pip build twine
pip install -U spacy
python -m spacy download en_core_web_sm
pip install .
```

---
## Quick Start
```python
from vagacore import compress

text = """
Apple reported $81.8 billion in revenue for Q3 2024.
If Apple sells 1M units, it will reach $900M.  # skipped (hypothetical)
Netflix and Disney reported $1B and $2B respectively.
"""

result = compress(text, mode="json")
print(result)
```
Output (shape):
```json
{
  "facts": [
    {"entity": "Apple", "event": "reported", "value": "$81.8 billion", "time": "Q3 2024", "confidence": 0.9},
    {"entity": "Netflix", "event": "reported", "value": "$1B", "time": null, "confidence": 0.9},
    {"entity": "Disney", "event": "reported", "value": "$2B", "time": null, "confidence": 0.9}
  ],
  "version": "1.0.1"
}
```

Other modes:
```python
compress(text, mode="text")  # human-readable
compress(text, mode="llm")   # compact strings for LLM context
```

---
## Key Behaviors
- Negation/hypotheticals: sentences with `neg` deps or modal/"if" are skipped.
- Owner/compound subjects: possessives and compounds pick the real actor (e.g., "Nvidia's data center revenue" → Nvidia).
- Value integrity: regex binds number + unit (M/B/bn/k/%) and strips trailing punctuation.
- State corrections: if a sentence contains "later/actually/corrected" with multiple numbers, keeps the latest value.
- Pairing and lists: handles `respectively`, ordered multi-entity/value pairs, and `Key: Value` list lines.
- Context memory: propagates last seen time; resolves generic subjects ("the company/it") to last entity.
- Dedup: groups facts by entity + semantic verb class + time + value, keeps highest confidence.

---
## Testing
```bash
./venv/Scripts/python.exe -m pytest
# or run bundled demos/tests
python examples/test_script.py
python examples/test_stress.py
```

---
## Production Notes
- Python >= 3.8; spaCy en_core_web_sm required.
- Default model is loaded once in [vagacore/parser.py](vagacore/parser.py); keep the process warm for throughput.
- For large docs, split into paragraphs and feed sequentially; context memory keeps last time/entity.
- Outputs are deterministic given spaCy model; no external APIs required.

---
## Changelog (high level)
- 1.0.1: Money regex hardening, possessive/compound subject priority, subject memory for generic refs, version bump.
- 1.0.0: Negation/hypothetical guards, list fallback, pairing alignment, correction-aware numeric selection.

---
## Architecture (Data Flow)

flowchart TD
    A[Raw Text] --> B[clean_text]
    B --> C[spaCy Parser\nNER + POS + Dependencies]
    C --> D[Noise / Validation Guards\nnegation+hypothetical filters]
    D --> E[Extractor\nSVO + values + time\nowner/compound subjects]
    E --> F[Pairing & Lists\nrespectively / parallel / key:value]
    F --> G[Context Memory\nlast time + last entity]
    G --> H[Deduplication & Confidence]
    H --> I[Formatted Output\nJSON | text | llm]

