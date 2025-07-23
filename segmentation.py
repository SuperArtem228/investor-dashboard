def segment_investors(engagement_scores, likelihood_scores):
    segments = {}
    for inv_id in engagement_scores:
        eng = engagement_scores[inv_id]
        lik = likelihood_scores[inv_id]
        if eng > 12 and lik > 70:
            segment = 'Hot Prospect'
        elif eng > 8 and lik > 50:
            segment = 'Warm Lead'
        elif eng > 5 and lik > 30:
            segment = 'Cold Contact'
        else:
            segment = 'Inactive'
        segments[inv_id] = segment
    return segments 