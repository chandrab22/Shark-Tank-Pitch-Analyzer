def generate_persona_feedback(transcript_text, tone_metrics, business_metrics):
    """
    Generate feedback from four personas: Visionary, Finance, Customer Advocate, Skeptic
    """
    tone_score = tone_metrics.get('tone_score', 0)
    business_score = business_metrics.get('business_score', 0)
    sections = business_metrics.get('structure', {})
    feedback_dict = {}

    # Visionary: market and differentiation focus
    visionary_comments = []
    if business_score >= 70:
        visionary_comments.append("I see strong market potential and a clear value prop.")
    else:
        visionary_comments.append("Interesting idea, but I need clearer evidence of market size and differentiation.")
    if sections.get('solution'):
        visionary_comments.append("The solution appears coherent; consider adding growth milestones.")
    feedback_dict['Visionary'] = ' '.join(visionary_comments)

    # Finance: revenue and margins
    finance_comments = []
    if business_score >= 60 and business_metrics.get('revenue_signals', 0) > 0:
        finance_comments.append("Revenue signals are present — clarify unit economics and margins.")
    else:
        finance_comments.append("Revenue model unclear. Show pricing, CAC and LTV assumptions.")
    if tone_score < 40:
        finance_comments.append("Delivery lacks confidence which weakens the financial pitch.")
    feedback_dict['Finance'] = ' '.join(finance_comments)

    # Customer Advocate: focus on problem and customer pain
    customer_comments = []
    if sections.get('problem'):
        customer_comments.append("Problem is defined; provide customer examples and pain quantification.")
    else:
        customer_comments.append("I am not convinced the customer pain is real — add testimonials or data.")
    feedback_dict['Customer Advocate'] = ' '.join(customer_comments)

    # Skeptic: risks and delivery
    skeptic_comments = []
    skeptic_comments.append("What are the key risks? Competitive response and execution are unclear.")
    if tone_score < 50:
        skeptic_comments.append("Also your delivery had several hesitations; practice to reduce filler words.")
    feedback_dict['Skeptic'] = ' '.join(skeptic_comments)

    # Recommendation logic
    recommendation_result = "Need More Info"
    if business_score >= 75 and tone_score >= 60:
        recommendation_result = "Invest"
    elif business_score < 40 or tone_score < 30:
        recommendation_result = "Not Invest"

    return feedback_dict, recommendation_result

if __name__ == "__main__":
    # Demo run
    feedback, recommendation = generate_persona_feedback(
        "demo",
        {'tone_score': 55},
        {'business_score': 45, 'structure': {}}
    )
    print(feedback)
    print("Recommendation:", recommendation)
