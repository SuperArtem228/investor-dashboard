import numpy as np

def calc_engagement_score(comms_df):
    # Примерная формула: глубина обсуждений, инициатива, скорость ответа, частота, настроение
    scores = {}
    for investor_id, group in comms_df.groupby('investor_id'):
        depth = group['depth'].mean()
        initiative = (group['initiative'] == 'investor').mean()
        response_speed = 1 / (group['response_time_h'].mean() + 1)
        freq = len(group) / 60  # за 60 дней
        sentiment = (group['sentiment'] == 'positive').mean() - (group['sentiment'] == 'negative').mean()
        score = 0.3*depth + 0.2*initiative + 0.2*response_speed + 0.2*freq + 0.1*sentiment
        scores[investor_id] = score * 20  # нормируем до 0-20
    return scores

def calc_investment_likelihood(investors_df, comms_df):
    # Примерная формула: профиль, стадия, активность
    profile_map = {'VC': 1.0, 'Angel': 0.8, 'Corporate': 0.7, 'Family Office': 0.6}
    stage_map = {'Lead': 0.3, 'Contacted': 0.5, 'Pitched': 0.7, 'Due Diligence': 0.85, 'Negotiation': 0.95, 'Closed': 1.0}
    scores = {}
    for _, row in investors_df.iterrows():
        profile_score = profile_map.get(row['profile'], 0.5)
        stage_score = stage_map.get(row['stage'], 0.3)
        comms = comms_df[comms_df['investor_id'] == row['investor_id']]
        activity = min(len(comms) / 10, 1.0)
        score = 0.4*profile_score + 0.4*stage_score + 0.2*activity
        scores[row['investor_id']] = score * 100  # нормируем до 0-100
    return scores 