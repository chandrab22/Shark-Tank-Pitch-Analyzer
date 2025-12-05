import re
from collections import Counter

def clean_text(input_text):
    """Normalize text by stripping whitespace and converting to lowercase"""
    return re.sub(r"\s+", " ", input_text.strip().lower())

def extract_pitch_deck_sections(text):
    """Naive detection of core pitch deck sections via keyword search"""
    text_lower = text.lower()
    sections_present = {'hook': False, 'problem': False, 'solution': False, 'ask': False}

    if any(word in text_lower for word in ['introduce', 'introducing', 'we built', 'our product', 'imagine', 'pitch']):
        sections_present['hook'] = True
    if any(word in text_lower for word in ['problem', 'pain', 'challenge', 'struggle']):
        sections_present['problem'] = True
    if any(word in text_lower for word in ['solution', 'we solve', 'our platform', 'our product', 'we provide']):
        sections_present['solution'] = True
    if any(word in text_lower for word in ['ask', 'raise', 'investment', 'funding', 'seeking', 'i am asking']):
        sections_present['ask'] = True

    return sections_present

def score_business_content(text):
    normalized = clean_text(text)
    sections = extract_pitch_deck_sections(normalized)

    base_score = 50.0
    # reward presence of key sections
    base_score += 10 * sum(1 for present in sections.values() if present)

    # reward mentions of revenue-related terms
    revenue_terms = ['revenue', 'price', 'subscription', 'fee', 'margin', 'monetize', 'sell']
    revenue_count = sum(normalized.count(term) for term in revenue_terms)
    base_score += min(20, revenue_count * 5)

    # reward mentions of market-related terms
    market_terms = ['market', 'customers', 'users', 'addressable', 'tpm', 'tpmg']
    market_count = sum(normalized.count(term) for term in market_terms)
    base_score += min(15, market_count * 3)

    # penalize overly short transcripts
    if len(normalized.split()) < 30:
        base_score -= 15

    final_score = max(0.0, min(100.0, base_score))
    details = {
        'structure': sections,
        'revenue_signals': revenue_count,
        'market_signals': market_count,
        'business_score': round(final_score, 2)
    }

    return details

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", required=True, help="Input transcript text")
    args = parser.parse_args()
    print(score_business_content(args.text))
