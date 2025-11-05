import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns

st.title("Étude de corrélation")

# --- lire le fichier CSV ---
try:
    df = pd.read_csv("data/pollution.csv")
except Exception as e:
    st.error(f"Erreur de lecture du fichier CSV: {e}")
    st.stop()

num_df = df.select_dtypes(include=np.number)

st.subheader("Corrélation de Pearson (numérique)")
pearson = num_df.corr(numeric_only=True)
st.dataframe(pearson)

st.subheader("Heatmap (Pearson)")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(pearson, cmap='coolwarm', annot=True, fmt='.3f', ax=ax)
st.pyplot(fig)

st.subheader("Corrélation de Spearman")
spearman = num_df.corr(method='spearman', numeric_only=True)
st.dataframe(spearman)

st.subheader("Corrélation de Kendall")
kendall = num_df.corr(method='kendall', numeric_only=True)
st.dataframe(kendall)

st.markdown("---")

# --- Statistiques demandées pour les PM2.5 et PM10 ---
# Ajustez ces noms si votre fichier CSV en utilise d'autres 
#(par exemple : « PM2.5 », « PM10 », « pm2_5 », « pm10 »)
# Tentative de recherche automatique des noms courants :
def find_col(possiveis):
    for c in df.columns:
        if c.strip().lower() in [p.strip().lower() for p in possiveis]:
            return c
    return None

pm25_col = find_col(["pm2.5", "pm2_5", "pm25"])
pm10_col = find_col(["pm10", "pm_10"])

if pm25_col and pm10_col:
    st.subheader("PM2.5 & PM10 : moyenne, médiane, écart-type")
    stats_df = pd.DataFrame({
        "mesure": ["moyenne", "médiane", "écart-type"],
        "PM2.5": [df[pm25_col].mean(), df[pm25_col].median(), df[pm25_col].std()],
        "PM10":  [df[pm10_col].mean(),  df[pm10_col].median(),  df[pm10_col].std()]
    })
    st.dataframe(stats_df)

   # Valeurs aberrantes via l'écart interquartile
    def outlier_iqr(s):
        s = s.dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        lower, upper = q1 - 1.5*iqr, q3 + 1.5*iqr
        return ((s < lower) | (s > upper)).sum(), lower, upper

    n25, l25, u25 = outlier_iqr(df[pm25_col])
    n10, l10, u10 = outlier_iqr(df[pm10_col])

    st.subheader("Valeurs aberrantes (IQR)")
    st.write(f"PM2.5: {n25} outliers | limites [{l25:.2f}, {u25:.2f}]")
    st.write(f"PM10 : {n10} outliers | limites [{l10:.2f}, {u10:.2f}]")

st.markdown("---")

# --- Corrélation Humidité ↔ Qualité de l'air (si elle existe) ---
humidity_col = find_col(["humidity", "humidité", "humidite", "hum"])
target_col   = find_col(["airquality", "qualite_de_l'air", "qualite_air", "quality", "variable_cible", "target"])

if humidity_col and target_col:
    st.subheader("Corrélation Humidité × Qualité de l’air")
    # Spearman gère au mieux l'algorithme si la variable cible est ordinale (0-3).
    rho = df[[humidity_col, target_col]].corr(method="spearman").iloc[0, 1]
    st.write(f"Corrélation (Spearman) entre {humidity_col} et {target_col} : **{rho:.3f}**")

st.markdown("---")

# --- Densité de population  (corrélation + dispersion) ---
density_col = find_col(["population_density", "densite_de_population", "densite(hab/km2)", "densite_hab_km2"])
if density_col and pm25_col:
    st.subheader("Lien entre densité de population et PM2.5")
    r = df[[density_col, pm25_col]].corr().iloc[0, 1]
    st.write(f"Corrélation (Pearson) entre {density_col} et {pm25_col} : **{r:.3f}**")

    fig2, ax2 = plt.subplots()
    ax2.scatter(df[density_col], df[pm25_col], alpha=0.6)
    ax2.set_xlabel(density_col)
    ax2.set_ylabel(pm25_col)
    ax2.set_title("Dispersion densité × PM2.5")
    st.pyplot(fig2)

# --- quartiles de CO (s'ils existent) ---
co_col = find_col(["co", "monoxyde_de_carbone"])
if co_col:
    st.subheader("Quartiles du CO (monoxyde de carbone)")
    q = df[co_col].quantile([0.25, 0.5, 0.75]).rename(index={0.25: "Q1", 0.5: "Q2 (médiane)", 0.75: "Q3"})
    st.write(q)
