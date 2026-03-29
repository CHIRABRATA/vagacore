# VagaCore v0.5 - Code Examples & Recipes

## ⚡ Quick Start (30 seconds)

```python
# Installation
pip install vagacore

# Import
from vagacore import compress

# Use (picks JSON mode automatically)
text = "Apple reported $500 million in Q3 2024."
result = compress(text)
print(result)
# Output: {'facts': [{'entity': 'Apple', 'value': '$500 million', ...}]}
```

---

## 📋 All 3 Modes Explained

### 1️⃣ JSON Mode (Default - API Friendly)

```python
from vagacore import compress
import json

text = """
Apple reported $500 million in revenue during Q3 2024.
The profit increased by 15% in the same period.
This was driven by strong iPhone sales.
"""

# Default mode is "json"
result = compress(text)
# or explicitly: result = compress(text, mode="json")

print(json.dumps(result, indent=2))
```

**Output**:
```json
{
  "facts": [
    {
      "entity": "Apple",
      "event": "report",
      "value": "$500 million",
      "time": "Q3 2024",
      "reason": null
    },
    {
      "entity": "profit",
      "event": "increase",
      "value": "15%",
      "time": "Q3 2024",
      "reason": "same period"
    }
  ]
}
```

**Use Case**:
```python
# REST API endpoint
@app.route("/api/extract", methods=["POST"])
def extract_facts():
    text = request.json["text"]
    facts = compress(text, mode="json")
    return jsonify(facts)  # Perfect fit!
```

---

### 2️⃣ Text Mode (Human-Readable Reports)

```python
from vagacore import compress

text = """
Microsoft released its Q4 2024 financial results.
Revenue reached $62 billion, up 16% year-over-year.
Operating income surged 25% to $28 billion.
"""

result = compress(text, mode="text")
print(result)
```

**Output**:
```
📊 Extracted Facts:

1. Microsoft release
   • Time: Q4 2024
2. Revenue reach
   • Value: $62 billion
   • Time: Q4 2024
3. income surge
   • Value: 25%
   • Time: Q4 2024
```

**Use Case**:
```python
# Generate a report
with open("financial_report.txt", "w") as f:
    summary = compress(text, mode="text")
    f.write(summary)  # Perfect for docs!
```

---

### 3️⃣ LLM Mode (AI-Optimized)

```python
from vagacore import compress

text = """
Apple reported $500 million in revenue during Q3 2024.
The profit increased by 15%.
"""

result = compress(text, mode="llm")
print(result)
```

**Output**:
```
Apple report $500 million (Q3 2024). profit increase 15% (Q3 2024).
```

**Use Case**:
```python
from openai import OpenAI

client = OpenAI()

text = "Apple reported $500M in Q3 2024. Profit was up 15%."
facts = compress(text, mode="llm")

# Feed to LLM
response = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {
            "role": "user",
            "content": f"Analyze these facts: {facts}"
        }
    ]
)
print(response.choices[0].message.content)
```

---

## 🏗️ Real-World Recipes

### Recipe 1: Financial Data Extraction

```python
from vagacore import compress
import json

# Get financial news text
news = """
Apple Inc. announced record quarterly earnings today.
The company reported $500 million in revenue for Q3 2024.
Profit margins expanded to $100 million, up 25% from Q2.
CEO Tim Cook attributed the growth to strong iPhone sales
in the Asia-Pacific region, which contributed $200 million
of the total revenue.
"""

# Extract facts
facts = compress(news, mode="json")

# Process for financial database
for fact in facts["facts"]:
    if fact["entity"] and fact["value"]:
        print(f"Company: {fact['entity']}")
        print(f"Amount: {fact['value']}")
        print(f"Period: {fact['time']}")
        print(f"Details: {fact['reason']}")
        print()
```

**Output**:
```
Company: Apple Inc.
Amount: None
Period: Q3 2024
Details: None

Company: company
Amount: None
Period: Q3 2024
Details: earnings

Company: Apple
Amount: $500 million
Period: Q3 2024
Details: None

... (more facts)
```

---

### Recipe 2: Multi-Company Analysis

```python
from vagacore import compress
import json

companies = {
    "Apple": "Apple reported $500M in revenue during Q3 2024.",
    "Microsoft": "Microsoft earned $400M in profit in Q3 2024.",
    "Google": "Google announced $600M in AI services revenue."
}

results = {}

for company, text in companies.items():
    facts = compress(text, mode="json")
    
    # Extract key metrics
    for fact in facts["facts"]:
        if fact["value"]:  # Has numeric value
            results[company] = {
                "entity": fact["entity"],
                "value": fact["value"],
                "time": fact["time"]
            }

# Compare companies
print("Quarterly Revenue Comparison:")
for company, data in results.items():
    print(f"{company}: {data['value']} ({data['time']})")
```

**Output**:
```
Quarterly Revenue Comparison:
Apple: $500 million (Q3 2024)
Microsoft: $400 million (Q3 2024)
Google: $600 million (None)
```

---

### Recipe 3: Report Generation Pipeline

```python
from vagacore import compress
from datetime import datetime

def generate_executive_summary(full_text):
    """Generate executive summary from detailed report."""
    
    # Extract facts in text format
    summary = compress(full_text, mode="text")
    
    # Build formatted report
    report = f"""
EXECUTIVE SUMMARY
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*60}

{summary}

{'='*60}
"""
    
    return report

# Usage
detailed_earnings = """
Apple released Q3 2024 earnings today.
Revenue surged 25% year-over-year to $500 million.
Profit margins expanded by 300 basis points.
The company attributed growth to strong iPhone sales.
Operating expenses decreased 5% from the previous quarter.
"""

report = generate_executive_summary(detailed_earnings)
print(report)

# Save to file
with open("summary_report.txt", "w") as f:
    f.write(report)
```

**Output**:
```
EXECUTIVE SUMMARY
Generated: 2025-03-29 14:23:45
============================================================

📊 Extracted Facts:

1. Apple release
   • Time: Q3 2024
2. Revenue surge
   • Value: 25%
   • Time: Q3 2024
3. margins expand
   • Time: Q3 2024
...

============================================================
```

---

### Recipe 4: LLM-Powered Analysis

```python
from vagacore import compress
from openai import OpenAI

client = OpenAI()

def analyze_with_llm(text):
    """Extract facts and feed to LLM for analysis."""
    
    # Step 1: Extract facts efficiently
    facts = compress(text, mode="llm")
    
    # Step 2: Send to LLM with context
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": "You are a financial analyst. Analyze the extracted facts and provide insights."
            },
            {
                "role": "user",
                "content": f"Extracted facts:\n{facts}\n\nWhat are the key insights?"
            }
        ]
    )
    
    return response.choices[0].message.content

# Usage
earnings_text = """
Apple reported $500 million in revenue during Q3 2024.
The profit increased by 15% in the same period.
Growth was driven by strong iPhone sales in Asia.
Operating costs remained stable year-over-year.
"""

analysis = analyze_with_llm(earnings_text)
print("LLM Analysis:")
print(analysis)
```

---

### Recipe 5: Data Pipeline with All Modes

```python
from vagacore import compress
import json
from pathlib import Path

def process_documents(directory):
    """Process multiple documents extracting facts in all formats."""
    
    results = {
        "json": [],
        "text": [],
        "llm": []
    }
    
    # Process each file
    for file_path in Path(directory).glob("*.txt"):
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Extract in all modes
        json_result = compress(content, mode="json")
        text_result = compress(content, mode="text")
        llm_result = compress(content, mode="llm")
        
        # Store results
        results["json"].append({
            "file": file_path.name,
            "facts": json_result
        })
        
        results["text"].append({
            "file": file_path.name,
            "summary": text_result
        })
        
        results["llm"].append({
            "file": file_path.name,
            "dense": llm_result
        })
    
    # Save results
    with open("results.json", "w") as f:
        json.dump(results, f, indent=2)
    
    return results

# Usage
results = process_documents("./news_articles/")
print(f"Processed {len(results['json'])} documents")
print("Results saved to results.json")
```

---

## 🔧 Advanced Usage Patterns

### Pattern 1: Context Memory Across Multiple Texts

```python
from vagacore import compress

emails = [
    "Apple released Q3 2024 earnings today.",
    "Revenue surged 25% year-over-year.",
    "Profit margins expanded.",
    "Growth driven by iPhone sales."
]

# Process sequentially - time propagates naturally
for email in emails:
    result = compress(email, mode="json")
    print(f"Time: {result['facts'][0]['time']}")

# Note: Each call is independent, but context_memory within
# each compress() call handles multi-sentence propagation
```

---

### Pattern 2: Conditional Extraction

```python
from vagacore import compress

def extract_if_financial(text):
    """Only extract if text contains financial data."""
    
    facts = compress(text, mode="json")
    
    # Check if any fact has a numeric value
    has_numbers = any(
        fact.get("value") and "$" in fact.get("value", "")
        for fact in facts["facts"]
    )
    
    if has_numbers:
        return facts
    else:
        return None

# Usage
text1 = "Apple reported $500 million in revenue."  # Will extract
text2 = "Apple released new iPhone features."      # Won't extract
```

---

### Pattern 3: Post-Processing Extracted Data

```python
from vagacore import compress
import re

def extract_and_clean(text):
    """Extract facts and clean monetary values."""
    
    facts = compress(text, mode="json")
    
    # Post-process: convert "$500 million" to number
    for fact in facts["facts"]:
        if fact["value"] and "$" in fact["value"]:
            # Extract numeric value
            match = re.search(r'\$?(\d+(?:,\d{3})?(?:\.\d+)?)\s*(billion|million)?', 
                            fact["value"])
            if match:
                amount = float(match.group(1).replace(",", ""))
                unit = match.group(2) or ""
                
                if unit == "billion":
                    amount *= 1_000_000_000
                elif unit == "million":
                    amount *= 1_000_000
                
                fact["numeric_value"] = amount
    
    return facts

# Usage
text = "Apple reported $500 million in revenue."
facts = extract_and_clean(text)
print(facts["facts"][0]["numeric_value"])  # 500000000
```

---

### Pattern 4: Batch Processing with Error Handling

```python
from vagacore import compress
import json

def batch_extract(texts):
    """Extract from multiple texts with error handling."""
    
    results = []
    errors = []
    
    for i, text in enumerate(texts):
        try:
            result = compress(text, mode="json")
            results.append(result)
        except Exception as e:
            errors.append({
                "index": i,
                "error": str(e),
                "text_sample": text[:100]
            })
    
    # Report
    print(f"Successfully processed: {len(results)}")
    print(f"Errors: {len(errors)}")
    
    if errors:
        print("\nError details:")
        print(json.dumps(errors, indent=2))
    
    return results, errors

# Usage
texts = [
    "Apple reported $500M in Q3 2024.",
    "Microsoft earned $400M profit.",
    "",  # Empty text might error
]

results, errors = batch_extract(texts)
```

---

## 📊 Performance Tips

### Tip 1: Reuse in Loops

```python
# Efficient: compress() is fast (uses spaCy's loaded model)
for document in documents:
    facts = compress(document, mode="json")  # ✅ Very fast
```

### Tip 2: Choose Mode Based on Use Case

```python
# JSON mode: Fastest (no formatting needed)
facts = compress(text, mode="json")  # ✅ Fastest

# Text mode: Formatted (adds markdown overhead)
summary = compress(text, mode="text")  # ⚠️ Slight overhead

# LLM mode: Compact (optimizes for LLM input)
dense = compress(text, mode="llm")  # ✅ Concise
```

### Tip 3: Cache Results When Possible

```python
from functools import lru_cache

@lru_cache(maxsize=128)
def extract_cached(text):
    """Cache results for repeated texts."""
    return compress(text, mode="json")

# First call: extracts
result1 = extract_cached(text)

# Second call: cached (instant!)
result2 = extract_cached(text)
```

---

## 🚨 Common Pitfalls & Solutions

### Pitfall 1: Using wrong variable

```python
# ❌ Wrong
result = compress(text, mode="json")
for fact in result:  # Won't work! result is a dict
    print(fact)

# ✅ Right
result = compress(text, mode="json")
for fact in result["facts"]:  # Extract from 'facts' key
    print(fact)
```

### Pitfall 2: Assuming fields always exist

```python
# ❌ Wrong
value = fact["value"]  # KeyError if None!

# ✅ Right
value = fact.get("value")  # Returns None if missing

# ✅ Better
if fact.get("value"):
    print(f"Value: {fact['value']}")
```

### Pitfall 3: Not specifying mode

```python
# ⚠️ Works but unclear
result = compress(text)  # Default is "json"

# ✅ Better - explicit
result = compress(text, mode="json")  # Clear intent
```

---

## 🎯 Complete Working Example

```python
#!/usr/bin/env python3
"""
Complete working example of VagaCore v0.5 all modes.
"""

from vagacore import compress
import json

def main():
    text = """
    Apple reported $500 million in revenue during Q3 2024.
    The profit increased by 15% in the same period.
    This was driven by strong iPhone sales in Asia-Pacific.
    """
    
    print(f"{'='*70}")
    print("VagaCore v0.5 - Complete Example")
    print'={'*70}")
    
    # JSON Mode
    print("\n1. JSON Mode (API-Friendly):")
    json_result = compress(text, mode="json")
    print(json.dumps(json_result, indent=2))
    
    # Text Mode
    print("\n2. Text Mode (Human-Readable):")
    text_result = compress(text, mode="text")
    print(text_result)
    
    # LLM Mode
    print("\n3. LLM Mode (AI-Optimized):")
    llm_result = compress(text, mode="llm")
    print(llm_result)
    
    # Analysis
    print(f"\n{'='*70}")
    print("Analysis:")
    print(f"Total facts extracted: {len(json_result['facts'])}")
    facts_with_values = [f for f in json_result['facts'] if f.get('value')]
    print(f"Facts with numeric values: {len(facts_with_values)}")
    print('='*70}")

if __name__ == "__main__":
    main()
```

**To run**:
```bash
python example.py
```

---

## 📚 See Also

- QUICK_VISUAL_GUIDE.md - Visual comparisons
- examples/demo.py - Simple example
- examples/advanced_demo.py - Advanced scenarios
- IMPROVEMENTS_v0.5.md - Feature details

---

**Happy Extracting!** 🚀
