from vagacore import compress

level_3_tests = [
    # 1. Complex Coreference (Does 'the company' link to 'Apple'?)
    "Apple released the Vision Pro. The company expects it to generate $1 billion.",

    # 2. Revisions & Updates (Testing state-change logic)
    "Amazon initially reported a 5% loss, but later clarified it was actually a 2% gain.",

    # 3. Interrupted Facts (Testing noise handling in the middle of a fact)
    "Google, despite facing massive regulatory pressure in Europe, earned $70 billion.",

    # 4. Multi-Entity / Multi-Value (The "Respectively" stress test)
    "Tesla and Ford produced 50k and 30k electric vehicles respectively last month.",

    # 5. Semantic Negation (Words that mean 'no' without saying 'not')
    "Microsoft failed to reach its target of $400 million this year.",

    # 6. Comparative Context (Does it extract the current or the old value?)
    "Netflix revenue hit $10B, up from $8B in the previous year.",

    # 7. Possessive Subjects
    "Nvidia's data center revenue surged to $18 billion in the last quarter.",

    # 8. Range Values (Can it handle 'between X and Y'?)
    "Meta expects total expenses to be between $94 billion and $99 billion.",

    # 9. List-Style Input (Common in financial summaries)
    "2024 Results: Revenue: $50M; Profit: $10M; Employees: 500.",

    # 10. Non-Financial Logic (Testing general SVO extraction)
    "The doctor treated the patient with a new experimental drug at the clinic."
]

for i, text in enumerate(level_3_tests, 1):
    print(f"\n===== TEST {i} =====")
    print("INPUT:", text)

    try:
        output = compress(text)
        print("OUTPUT:", output)
    except Exception as e:
        print("❌ ERROR:", e)