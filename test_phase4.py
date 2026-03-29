#!/usr/bin/env python3
"""Test Phase 4 enhancements - core validation & normalization layers."""

import json
import sys

# Handle unicode on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from vagacore import compress

# Test cases - real-world financial news
test_cases = [
    "Apple reported $500 million in revenue for Q3 2024.",
    "Amazon grew by 25% compared to last quarter in Q2 2024.",
    "Microsoft declined in profits during Q1 while expenses surged.",
    "The company earned $2 billion in Q4 from smartphone sales.",
    "Tesla's quarterly revenue reached 1.2 trillion dollars in Q3 2024.",
]

print("=" * 70)
print("VagaCore v0.6.0 - Phase 4 Testing")
print("=" * 70)
print()

for i, text in enumerate(test_cases, 1):
    print(f"Test {i}: {text}")
    print("-" * 70)
    
    # Test JSON mode (structured output)
    result_json = compress(text, mode="json")
    print("\n[JSON Mode]")
    
    # result_json is already a dict in JSON mode
    if isinstance(result_json, str):
        parsed = json.loads(result_json)
    else:
        parsed = result_json
    
    print(f"Version: {parsed.get('version')}")
    print(f"Facts extracted: {len(parsed.get('facts', []))}")
    
    for fact in parsed.get('facts', []):
        print(f"\n  Entity: {fact.get('entity')}")
        print(f"  Event: {fact.get('event')}")
        print(f"  Value: {fact.get('value')}")
        print(f"  Time: {fact.get('time')}")
        print(f"  Confidence: {fact.get('confidence', 'N/A'):.1%}")
    
    # Test TEXT mode (human readable)
    print("\n[TEXT Mode]")
    result_text = compress(text, mode="text")
    print(result_text)
    
    print("\n")

print("=" * 70)
print("Testing Complete")
print("=" * 70)
