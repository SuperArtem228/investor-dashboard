import random
import datetime
import pandas as pd

# Генерация mock-данных инвесторов
def generate_investors(n=30):
    names = [f"Investor_{i+1}" for i in range(n)]
    profiles = random.choices(['VC', 'Angel', 'Corporate', 'Family Office'], k=n)
    stages = random.choices(['Lead', 'Contacted', 'Pitched', 'Due Diligence', 'Negotiation', 'Closed'], k=n)
    investors = pd.DataFrame({
        'investor_id': range(1, n+1),
        'name': names,
        'profile': profiles,
        'stage': stages
    })
    return investors

# Генерация mock-данных коммуникаций
def generate_communications(investors, days=60):
    records = []
    for _, row in investors.iterrows():
        n_msgs = random.randint(3, 20)
        last_date = datetime.datetime.now()
        for i in range(n_msgs):
            days_ago = random.randint(0, days)
            date = last_date - datetime.timedelta(days=days_ago)
            response_time = random.uniform(1, 72)  # часы
            depth = random.randint(1, 5)
            initiative = random.choice(['investor', 'founder'])
            sentiment = random.choice(['positive', 'neutral', 'negative'])
            records.append({
                'investor_id': row['investor_id'],
                'date': date,
                'response_time_h': response_time,
                'depth': depth,
                'initiative': initiative,
                'sentiment': sentiment
            })
    return pd.DataFrame(records) 