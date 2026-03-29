"""
VagaCore AI Demo - Text Compression & Fact Extraction

Demonstrates the power of intelligent fact extraction using:
- Named Entity Recognition (NER)
- Dependency Parsing
- Context-Aware Processing with Multiple Output Modes
"""

import json
from vagacore import compress


def main():
    """Run the VagaCore demonstration."""
    
    # Sample input text
    text = """
Apple reported $500 million in revenue during Q3 2024 in the Asia-Pacific region.
The profit increased by 15% in the same period.
This was driven by strong iPhone sales.
"""
    
    # Beautiful output
    print("\n" + "=" * 70)
    print("🚀 VagaCore AI - Intelligent Text Compression & Fact Extraction")
    print("=" * 70)
    
    print("\n📥 INPUT TEXT:\n")
    print(text)
    
    # MODE 1: JSON (API-friendly)
    print("\n" + "=" * 70)
    print("📤 MODE 1: JSON Output (API-Friendly)")
    print("=" * 70)
    result_json = compress(text, mode="json")
    print(json.dumps(result_json, indent=2))
    
    # MODE 2: Text (Human-readable)
    print("\n" + "=" * 70)
    print("📄 MODE 2: Text Output (Human-Readable)")
    print("=" * 70)
    result_text = compress(text, mode="text")
    print(result_text)
    
    # MODE 3: LLM (Optimized for AI consumption)
    print("\n" + "=" * 70)
    print("🤖 MODE 3: LLM Output (AI-Optimized)")
    print("=" * 70)
    result_llm = compress(text, mode="llm")
    print(result_llm)
    
    print("\n" + "=" * 70)
    print("✅ Extraction Complete!")
    print("=" * 70)
    print("\n🎯 VagaCore v0.5 | Hybrid NER + Rule-Based Extraction")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
