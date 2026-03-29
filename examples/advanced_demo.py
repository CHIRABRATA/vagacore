"""
VagaCore Advanced Demo - Multiple Scenarios

Demonstrates VagaCore's capability on diverse text inputs
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from compressor import compress


def demo_financial_report():
    """Demo 1: Financial Report Extraction"""
    print("\n" + "=" * 70)
    print("📊 DEMO 1: Financial Report Extraction")
    print("=" * 70)
    
    text = """
Microsoft released its Q4 2024 financial results.
Revenue reached $62 billion, up 16% year-over-year.
Operating income surged 25% to $28 billion.
Cloud services revenue more than doubled in the same period.
"""
    
    print("\nInput:")
    print(text)
    
    result = compress(text)
    
    print("\nExtracted Facts:")
    print(json.dumps(result, indent=2))


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
    
    print("\nInput (Notice: Only 1st sentence has date):")
    print(text)
    
    result = compress(text)
    
    print("\nExtracted Facts (Notice: All inherit Q3 2024):")
    print(json.dumps(result, indent=2))
    
    print("\n💡 KEY INSIGHT:")
    print("   Without context memory, facts 2-4 would have no time.")
    print("   With context memory, all facts are properly temporalized!")


def demo_hybrid_extraction():
    """Demo 3: Hybrid NER + Rule-Based Extraction"""
    print("\n" + "=" * 70)
    print("🔀 DEMO 3: Hybrid Extraction (NER + Rules)")
    print("=" * 70)
    
    text = """
Google announced record profits of $80 million in Asia-Pacific.
Amazon expanded its cloud services by 40%.
"""
    
    print("\nInput:")
    print(text)
    
    result = compress(text)
    
    print("\nExtracted Facts:")
    print(json.dumps(result, indent=2))
    
    print("\n💡 HYBRID APPROACH:")
    print("   • NER detects: MONEY ($80 million), ORG (Google), LOC (Asia-Pacific)")
    print("   • Rules detect: PERCENT (40%), domain keywords (profits)")
    print("   Both work together for complete extraction!")


def main():
    """Run all demos"""
    print("\n" + "🚀" * 35)
    print("VagaCore Advanced Demonstrations")
    print("🚀" * 35)
    
    demo_financial_report()
    demo_context_memory()
    demo_hybrid_extraction()
    
    print("\n" + "=" * 70)
    print("✨ All demonstrations complete!")
    print("=" * 70 + "\n")


if __name__ == "__main__":
    main()
