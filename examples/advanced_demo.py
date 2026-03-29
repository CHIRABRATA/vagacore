"""
VagaCore Advanced Demo - Multiple Scenarios & Output Modes

Demonstrates VagaCore's capability on diverse text inputs with:
- JSON mode (API-friendly)
- Text mode (human-readable)
- LLM mode (AI-optimized)
"""

import json
from vagacore import compress


def demo_financial_report():
    """Demo 1: Financial Report with Multiple Output Modes"""
    print("\n" + "=" * 70)
    print("📊 DEMO 1: Financial Report Extraction (All Modes)")
    print("=" * 70)
    
    text = """
Microsoft released its Q4 2024 financial results.
Revenue reached $62 billion, up 16% year-over-year.
Operating income surged 25% to $28 billion.
Cloud services revenue more than doubled in the same period.
"""
    
    print("\n📥 Input:")
    print(text)
    
    # JSON mode
    print("\n📤 JSON Mode (API-Friendly):")
    result_json = compress(text, mode="json")
    print(json.dumps(result_json, indent=2))
    
    # Text mode
    print("\n📄 Text Mode (Human-Readable):")
    result_text = compress(text, mode="text")
    print(result_text)
    
    # LLM mode
    print("\n🤖 LLM Mode (AI-Optimized):")
    result_llm = compress(text, mode="llm")
    print(result_llm)


def demo_context_memory():
    """Demo 2: Context Memory - Temporal Propagation"""
    print("\n" + "=" * 70)
    print("🧠 DEMO 2: Context Memory & Temporal Propagation")
    print("=" * 70)
    
    text = """
Apple released Q3 2024 earnings today.
Revenue surged 25% year-over-year.
Profit margins expanded by 300 basis points.
The company attributed growth to strong iPhone sales.
"""
    
    print("\n📥 Input (Notice: Only 1st sentence has date):")
    print(text)
    
    result = compress(text, mode="json")
    
    print("\n📤 Extracted Facts (Notice: All inherit Q3 2024):")
    print(json.dumps(result, indent=2))
    
    print("\n💡 KEY INSIGHT:")
    print("   Without context memory, facts 2-4 would have no time.")
    print("   With context memory, all facts are properly temporalized!")


def demo_entity_separation():
    """Demo 3: No Cross-Entity Mixing"""
    print("\n" + "=" * 70)
    print("🔀 DEMO 3: Multi-Entity Separation (No Cross-Mixing)")
    print("=" * 70)
    
    text = """
Google announced record profits of $80 million in Asia-Pacific.
Amazon expanded its cloud services by 40% in the same quarter.
Microsoft reported $62 billion in revenue from enterprise solutions.
"""
    
    print("\n📥 Input:")
    print(text)
    
    result = compress(text, mode="json")
    
    print("\n📤 Extracted Facts (Each entity separate):")
    print(json.dumps(result, indent=2))
    
    print("\n💡 KEY INSIGHT:")
    print("   Each fact properly tracked to its entity (Google, Amazon, Microsoft)")
    print("   No mixing of competitors' data ✓")


def demo_number_preservation():
    """Demo 4: Complete Number/Time Preservation"""
    print("\n" + "=" * 70)
    print("💰 DEMO 4: Complete Number & Time Preservation")
    print("=" * 70)
    
    text = """
Apple reported $500 million in Q3 2024.
Growth increased by 15%.
Expenses totaled $120 million in the period.
"""
    
    print("\n📥 Input:")
    print(text)
    
    result_json = compress(text, mode="json")
    result_llm = compress(text, mode="llm")
    
    print("\n📤 JSON Output (Full precision preserved):")
    print(json.dumps(result_json, indent=2))
    
    print("\n🤖 LLM Output (Concise, unambiguous):")
    print(result_llm)
    
    print("\n💡 IMPROVEMENTS:")
    print("   ✓ Preserves exact numbers: $500M, 15%, $120M")
    print("   ✓ Keeps time expressions: Q3 2024")
    print("   ✓ Maintains context across sentences")


def main():
    """Run all demos"""
    print("\n" + "🚀" * 35)
    print("VagaCore Advanced Demonstrations - v0.5+")
    print("🚀" * 35)
    
    demo_financial_report()
    demo_context_memory()
    demo_entity_separation()
    demo_number_preservation()
    
    print("\n" + "=" * 70)
    print("✨ All demonstrations complete!")
    print("=" * 70)
    print("\n📚 Summary of Improvements:")
    print("   ✅ Core Quality: Numbers preserved, no entity mixing")
    print("   ✅ Usable Output: JSON, Text, LLM modes")
    print("   ✅ Zero Friction: Auto-downloads spaCy model")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
