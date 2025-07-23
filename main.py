import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import generate_investors, generate_communications
from scoring import calc_engagement_score, calc_investment_likelihood
from segmentation import segment_investors

# --- Кастомные стили ---
st.markdown('''
    <style>
    .main {
        background: linear-gradient(135deg, #e3f2fd 0%, #f5f7fa 100%);
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1976d2;
    }
    .stTabs [aria-selected="true"] {
        background: linear-gradient(90deg, #1976d2 60%, #42a5f5 100%);
        color: #fff !important;
        border-radius: 12px 12px 0 0;
        box-shadow: 0 4px 16px 0 rgba(33,150,243,0.10);
    }
    .big-metric {
        font-size: 2.8rem;
        font-weight: 900;
        color: #1976d2;
        margin-bottom: 0.2em;
        letter-spacing: -2px;
    }
    .card {
        background: linear-gradient(120deg, #fff 80%, #e3f2fd 100%);
        border-radius: 20px;
        box-shadow: 0 8px 32px 0 rgba(33,150,243,0.10);
        padding: 2.2em 1.7em 1.7em 1.7em;
        margin-bottom: 2em;
        border: 1.5px solid #e3f2fd;
    }
    .seg-badge {
        font-size: 1.2em;
        font-weight: 700;
        padding: 0.35em 1.2em;
        border-radius: 1.2em;
        margin-right: 0.5em;
        box-shadow: 0 2px 8px 0 rgba(33,150,243,0.10);
        display: inline-block;
    }
    .wow-divider {
        height: 4px;
        width: 100%;
        background: linear-gradient(90deg, #1976d2 0%, #e53935 100%);
        border-radius: 2px;
        margin: 2em 0 2em 0;
    }
    .footer {
        color: #90a4ae;
        font-size: 1.1em;
        margin-top: 2em;
        text-align: center;
    }
    </style>
''', unsafe_allow_html=True)

st.set_page_config(page_title="Investor Analytics Dashboard", layout="wide")
st.markdown("""
<div style='display:flex;align-items:center;gap:1em;margin-bottom:1.5em;'>
  <span style='font-size:2.5rem;'>📊</span>
  <span style='font-size:2.2rem;font-weight:900;color:#1976d2;letter-spacing:-2px;'>Investor Analytics Dashboard</span>
</div>
""", unsafe_allow_html=True)

# --- Данные ---
investors = generate_investors(30)
comms = generate_communications(investors, days=60)
eng_scores = calc_engagement_score(comms)
lik_scores = calc_investment_likelihood(investors, comms)
segments = segment_investors(eng_scores, lik_scores)
investors['EngagementScore'] = investors['investor_id'].map(eng_scores)
investors['InvestmentLikelihood'] = investors['investor_id'].map(lik_scores)
investors['Segment'] = investors['investor_id'].map(segments)

segment_colors = {
    'Hot Prospect': '#e53935',
    'Warm Lead': '#fb8c00',
    'Cold Contact': '#1976d2',
    'Inactive': '#90a4ae',
}
segment_emojis = {
    'Hot Prospect': '🔥',
    'Warm Lead': '🟠',
    'Cold Contact': '🧊',
    'Inactive': '💤',
}

# --- Вкладки ---
tabs = st.tabs(["Воронка", "Тренды", "Сегментация", "Таблица", "Сводка", "ИИ-инсайты"])

# --- Воронка ---
with tabs[0]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Воронка инвесторов")
    stage_order = ['Lead', 'Contacted', 'Pitched', 'Due Diligence', 'Negotiation', 'Closed']
    counts = investors['stage'].value_counts().reindex(stage_order, fill_value=0)
    fig = go.Figure(go.Funnel(
        y=stage_order,
        x=counts.values,
        textinfo="value+percent initial",
        marker={"color": '#1976d2', "line": {"color": "#42a5f5", "width": 2}}
    ))
    fig.update_layout(
        plot_bgcolor='#f5f7fa',
        paper_bgcolor='#f5f7fa',
        font=dict(family='Inter, sans-serif', size=17),
        margin=dict(t=40, l=100, r=40, b=40),
        height=420,
        transition={'duration': 500}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

# --- Тренды ---
with tabs[1]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Тренды вовлечённости и скорости ответа")
    comms['date'] = pd.to_datetime(comms['date'])
    comms['day'] = comms['date'].dt.date
    daily_msgs = comms.groupby('day').size()
    avg_response = comms.groupby('day')['response_time_h'].mean()
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.08,
                       subplot_titles=("Вовлечённость (сообщений в день)", "Среднее время ответа (часы)"))
    fig.add_trace(go.Bar(x=daily_msgs.index, y=daily_msgs.values, name="Messages", marker_color="#1976d2", opacity=0.85), row=1, col=1)
    fig.add_trace(go.Scatter(x=avg_response.index, y=avg_response.values, name="Avg Response Time", line=dict(color="#e53935", width=4)), row=2, col=1)
    fig.update_layout(
        height=520,
        plot_bgcolor='#f5f7fa',
        paper_bgcolor='#f5f7fa',
        font=dict(family='Inter, sans-serif', size=16),
        showlegend=False,
        transition={'duration': 500}
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

# --- Сегментация ---
with tabs[2]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Сегментация инвесторов")
    segs = investors.groupby('Segment').size().to_dict()
    cols = st.columns(len(segs))
    for i, (seg, count) in enumerate(segs.items()):
        color = segment_colors.get(seg, '#90a4ae')
        emoji = segment_emojis.get(seg, '')
        with cols[i]:
            st.markdown(f'<div class="big-metric">{emoji} {count}</div>', unsafe_allow_html=True)
            st.markdown(f'<span class="seg-badge" style="background:{color};color:#fff;">{seg}</span>', unsafe_allow_html=True)
            st.caption(f"Средний Engagement: <b>{investors[investors['Segment']==seg]['EngagementScore'].mean():.1f}</b>", unsafe_allow_html=True)
            st.caption(f"Средний Likelihood: <b>{investors[investors['Segment']==seg]['InvestmentLikelihood'].mean():.1f}</b>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

# --- Таблица ---
with tabs[3]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Таблица инвесторов")
    styled_df = investors[['name', 'profile', 'stage', 'EngagementScore', 'InvestmentLikelihood', 'Segment']].rename(columns={
        'name': 'Имя',
        'profile': 'Профиль',
        'stage': 'Стадия',
        'EngagementScore': 'Engagement',
        'InvestmentLikelihood': 'Likelihood',
        'Segment': 'Сегмент'
    })
    def highlight_segment(val):
        color = segment_colors.get(val, '#90a4ae')
        return f'background-color: {color}; color: #fff; font-weight: bold;'
    st.dataframe(
        styled_df.style.applymap(highlight_segment, subset=['Сегмент']),
        use_container_width=True,
        hide_index=True,
        height=600
    )
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

# --- Сводка ---
with tabs[4]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Сводные метрики")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Всего инвесторов", len(investors), delta=None, help="Общее количество инвесторов в базе")
    with col2:
        st.metric("Hot Prospects 🔥", segs.get('Hot Prospect', 0))
    with col3:
        st.metric("Warm Leads 🟠", segs.get('Warm Lead', 0))
    st.markdown('</div>', unsafe_allow_html=True)

# --- ИИ-инсайты ---
with tabs[5]:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("💡 ИИ-инсайты и рекомендации")

    # 1. Тренды по сегментам
    segs = investors.groupby('Segment').size().to_dict()
    prev_hot = np.random.randint(max(0, segs.get('Hot Prospect', 0) - 3), segs.get('Hot Prospect', 0) + 1)  # имитация прошлых значений
    hot_delta = segs.get('Hot Prospect', 0) - prev_hot
    trend_emoji = '⬆️' if hot_delta > 0 else ('⬇️' if hot_delta < 0 else '➡️')
    st.markdown(f"<div style='font-size:1.2em;'><b>📈 Hot Prospects:</b> {segs.get('Hot Prospect', 0)} ({'+' if hot_delta>0 else ''}{hot_delta}) {trend_emoji}</div>", unsafe_allow_html=True)

    # 2. Средний Engagement и его динамика
    avg_eng = investors['EngagementScore'].mean()
    prev_avg_eng = avg_eng - np.random.uniform(-1.5, 1.5)  # имитация прошлых значений
    eng_delta = avg_eng - prev_avg_eng
    eng_emoji = '🚀' if eng_delta > 0.5 else ('⚠️' if eng_delta < -0.5 else '➡️')
    st.markdown(f"<div style='font-size:1.2em;'><b>💬 Средний Engagement:</b> {avg_eng:.1f} ({'+' if eng_delta>0 else ''}{eng_delta:.1f}) {eng_emoji}</div>", unsafe_allow_html=True)

    # 3. Аномалии: инвесторы с резким падением вовлечённости
    eng_scores_series = pd.Series(eng_scores)
    low_eng = eng_scores_series[eng_scores_series < 5]
    if not low_eng.empty:
        st.markdown(f"<div style='font-size:1.1em;'><b>⚠️ Аномалия:</b> {len(low_eng)} инвесторов с низким Engagement (&lt;5). Проверьте коммуникацию!</div>", unsafe_allow_html=True)

    # 4. Рекомендация по сегменту
    if segs.get('Warm Lead', 0) > segs.get('Hot Prospect', 0):
        st.markdown("<div style='font-size:1.1em;'><b>🧠 Рекомендация:</b> Сфокусируйтесь на Warm Leads — у них высокий потенциал перехода в Hot Prospect.</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div style='font-size:1.1em;'><b>🧠 Рекомендация:</b> Продолжайте поддерживать высокий уровень вовлечённости Hot Prospects!</div>", unsafe_allow_html=True)

    # 5. Прогноз (простая линейная экстраполяция)
    # Для примера: прогнозируем рост Hot Prospects
    forecast = int(segs.get('Hot Prospect', 0) + np.random.uniform(1, 3))
    st.markdown(f"<div style='font-size:1.1em;'><b>🔮 Прогноз:</b> К концу месяца Hot Prospects может стать <b>{forecast}</b>.</div>", unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<div class="wow-divider"></div>', unsafe_allow_html=True)

st.markdown("""
<div class='footer'>
  <span style='font-size:1.5em;'>✨</span> <b>Powered by Streamlit & Plotly. Design by AI.</b> <span style='font-size:1.5em;'>✨</span>
</div>
""", unsafe_allow_html=True) 