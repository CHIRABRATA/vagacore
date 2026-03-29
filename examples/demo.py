"""
VagaCore AI Demo - Text Compression & Fact Extraction

Demonstrates the power of intelligent fact extraction using:
- Named Entity Recognition (NER)
- Dependency Parsing
- Context-Aware Processing
"""

import json

from vagacore import compress


def main():
    """Run the VagaCore demonstration."""
    
    # Sample input text
    text = """
Apple reported $500 million in revenue during Q3 2024 in the Asia-Pacific region.
The profit increased by 15% in the same period.
"""
    
    # Run compression
    result = compress(text)
    
    # Beautiful output
    print("\n" + "=" * 70)
    print("🚀 VagaCore AI - Intelligent Text Compression & Fact Extraction")
    print("=" * 70)
    
    print("\n📥 INPUT TEXT:\n")
    print(text)
    
    print("\n📤 EXTRACTED FACTS:\n")
    print(json.dumps(result, indent=2))
    
    print("\n" + "=" * 70)
    print("✅ Extraction Complete!")
    print("=" * 70)
    
    # Show what was extracted
    print("\n📊 SUMMARY:\n")
    for i, fact in enumerate(result, 1):
        print(f"  Fact {i}:")
        print(f"    • Subject: {fact.get('subject', 'N/A')}")
        print(f"    • Action: {fact.get('action', 'N/A')}")
        print(f"    • Value: {fact.get('value', 'N/A')}")
        print(f"    • Entity: {fact.get('entity', 'N/A')}")
        print(f"    • Time: {fact.get('time', 'N/A')}")
        print()
    
    print("=" * 70)
    print("🎯 VagaCore v0.5 | Hybrid NER + Rule-Based Extraction")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
