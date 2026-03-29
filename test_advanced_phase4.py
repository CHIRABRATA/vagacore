#!/usr/bin/env python3
"""Advanced test for Phase 4 - Numeric reasoning and deduplication."""

import json
import sys

# Handle unicode on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from vagacore import compress
from vagacore.parser import parse_text
from vagacore.extractor import analyze_numeric_comparison

# Test numeric comparisons
test_comparisons = [
    "Apple revenue grew by 25% in Q3 2024.",
    "Amazon sales declined by 10% compared to previous year.",
    "Microsoft profits increased by $2 billion.",
    "Tesla's growth surged by 35% year-over-year.",
]

print("=" * 70)
print("VagaCore v0.6.0 - Numeric Reasoning Test")
print("=" * 70)
print()

for text in test_comparisons:
    print(f"Text: {text}")
    
    doc = parse_text(text)
    comparison = analyze_numeric_comparison(doc)
    
    if comparison:
        print(f"  Direction: {comparison['direction']}")
        print(f"  Magnitude: {comparison['magnitude']}")
        print(f"  Is Percentage: {comparison['percent']}")
        print(f"  Comparison Text: {comparison['comparison_text']}")
    else:
        print("  No numeric comparison found")
    
    # Also show fact extraction
    result = compress(text, mode="json")
    facts = result.get('facts', [])
    for fact in facts:
        print(f"  Fact: {fact['entity']} {fact['event']} {fact['value']} ({fact['time']})")
    print()

# Test deduplication with duplicate facts
print("\n" + "=" * 70)
print("Deduplication Test")
print("=" * 70)
print()

# Multi-sentence with potential duplicates
dup_text = """
Microsoft reported $40 billion in Q2 2024.
Microsoft had revenue of $40 billion in Q2 2024.
Microsoft generated $40 billion income during Q2 2024.
Microsoft earned $41 billion (revised) in Q2 2024.
"""

print(f"Text: {dup_text.strip()}")
print("\nExtracted facts (after deduplication):")

result = compress(dup_text, mode="json")
facts = result.get('facts', [])
print(f"Total facts extracted: {len(facts)}")

for i, fact in enumerate(facts, 1):
    print(f"\n{i}. Entity: {fact['entity']}")
    print(f"   Event: {fact['event']}")
    print(f"   Value: {fact['value']}")
    print(f"   Time: {fact['time']}")
    print(f"   Confidence: {fact['confidence']:.0%}")

print("\n" + "=" * 70)
print("Testing Complete")
print("=" * 70)
