import streamlit as st
import pandas as pd
import plotly.express as px
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from datetime import datetime
from database import get_all_stories, get_latest_fetch_time, init_db
from fetch import update_data

st.set_page_config(page_title="Hacker News Trends", layout="wide")
st.title("📈 Hacker News Trends Dashboard")

init_db()

col1, col2 = st.columns([1, 3])
with col1:
    if st.button("🔄 Actualizar datos ahora"):
        with st.spinner("Descargando últimos posts..."):
            count = update_data()
            st.success(f"¡Actualizado! {count} posts nuevos.")
            st.rerun()

last_fetch = get_latest_fetch_time()
if last_fetch:
    st.caption(f"Última actualización: {last_fetch}")
else:
    st.info("Aún no hay datos. Haz clic en 'Actualizar datos ahora'.")

df = get_all_stories()
if df.empty:
    st.warning("No hay datos. Usa el botón para descargar.")
    st.stop()

total_posts = df['id'].nunique()
avg_score = df['score'].mean()
avg_comments = df['descendants'].mean()
col1, col2, col3 = st.columns(3)
col1.metric("Posts únicos", total_posts)
col2.metric("Puntuación media", f"{avg_score:.1f}")
col3.metric("Comentarios medios", f"{avg_comments:.1f}")

df['datetime'] = pd.to_datetime(df['time'], unit='s')
st.subheader("Evolución de puntuaciones")
fig = px.scatter(df, x='datetime', y='score', hover_data=['title'], title="Puntuación de posts a lo largo del tiempo")
st.plotly_chart(fig, use_container_width=True)

st.subheader("Top 10 posts más votados")
top10 = df.sort_values('score', ascending=False).head(10)[['title', 'score', 'descendants']]
st.dataframe(top10, use_container_width=True)

st.subheader("Nube de palabras (títulos)")
all_titles = " ".join(df['title'].dropna().tolist())
if all_titles:
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_titles)
    fig_wc, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig_wc)
else:
    st.info("No hay títulos para generar nube de palabras.")
