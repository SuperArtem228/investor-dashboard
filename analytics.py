import matplotlib.pyplot as plt
import pandas as pd

def plot_funnel(investors_df):
    stage_order = ['Lead', 'Contacted', 'Pitched', 'Due Diligence', 'Negotiation', 'Closed']
    counts = investors_df['stage'].value_counts().reindex(stage_order, fill_value=0)
    plt.figure(figsize=(8,4))
    plt.bar(stage_order, counts)
    plt.title('Pipeline Funnel')
    plt.xlabel('Stage')
    plt.ylabel('Number of Investors')
    plt.tight_layout()
    plt.savefig('funnel.png')
    plt.close()

def plot_engagement_trend(comms_df):
    comms_df['date'] = pd.to_datetime(comms_df['date'])
    comms_df['day'] = comms_df['date'].dt.date
    daily = comms_df.groupby('day').size()
    plt.figure(figsize=(10,4))
    plt.plot(daily.index, daily.values)
    plt.title('Engagement Trend (Messages per Day)')
    plt.xlabel('Date')
    plt.ylabel('Messages')
    plt.tight_layout()
    plt.savefig('engagement_trend.png')
    plt.close()

def plot_response_rate_trend(comms_df):
    comms_df['date'] = pd.to_datetime(comms_df['date'])
    comms_df['day'] = comms_df['date'].dt.date
    avg_response = comms_df.groupby('day')['response_time_h'].mean()
    plt.figure(figsize=(10,4))
    plt.plot(avg_response.index, avg_response.values)
    plt.title('Response Time Trend (Avg Hours)')
    plt.xlabel('Date')
    plt.ylabel('Avg Response Time (h)')
    plt.tight_layout()
    plt.savefig('response_time_trend.png')
    plt.close() 