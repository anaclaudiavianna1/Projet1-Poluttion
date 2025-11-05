import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Étude des corrélations")

# 1) Lecture du CSV
try:
    df = pd.read_csv("data/pollution.csv")
except Exception:
    st.error("Erreur de lecture du fichier CSV.")
    st.stop()

# 2) Corrélation de Pearson 
st.subheader("Corrélation de Pearson (variables numériques)")
num_df = df.select_dtypes(include=np.number)
st.dataframe(num_df.corr())

st.subheader("Heatmap (Pearson)")
fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(num_df.corr(), cmap="coolwarm", annot=True, fmt=".2f", ax=ax)
st.pyplot(fig)

st.markdown("---")

# 3) Petites statistiques demandées (PM2.5 et PM10)
def trouve_col(noms_possibles):
    bas = [n.lower().strip() for n in noms_possibles]
    for c in df.columns:
        if c.lower().strip() in bas:
            return c
    return None

pm25 = trouve_col(["pm2.5", "pm2_5", "pm25"])
pm10 = trouve_col(["pm10", "pm_10"])

if pm25 and pm10:
    st.subheader("PM2.5 et PM10 : moyenne / médiane / écart-type")
    res = pd.DataFrame({
        "Mesure": ["Moyenne", "Médiane", "Écart-type"],
        "PM2.5": [df[pm25].mean(), df[pm25].median(), df[pm25].std()],
        "PM10":  [df[pm10].mean(), df[pm10].median(), df[pm10].std()]
    })
    st.dataframe(res)

    # Valeurs aberrantes (méthode IQR simple)
    def nb_outliers(s):
        s = s.dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        bas, haut = q1 - 1.5*iqr, q3 + 1.5*iqr
        return int(((s < bas) | (s > haut)).sum())

    st.subheader("Valeurs aberrantes (IQR)")
    st.write(f"PM2.5 : **{nb_outliers(df[pm25])}**  |  PM10 : **{nb_outliers(df[pm10])}**")

st.markdown("---")

# 4) Corrélation Humidité ↔ Qualité de l’air 
hum = trouve_col(["humidity", "humidité", "humidite"])
cible = trouve_col(["qualite_air", "airquality", "quality", "target", "variable_cible"])
if hum and cible:
    st.subheader("Corrélation Humidité × Qualité de l’air (Spearman)")
    rho = df[[hum, cible]].corr(method="spearman").iloc[0, 1]
    st.write(f"Spearman = **{rho:.3f}** (valeur proche de 0 = faible lien)")

# 5) Lien Densité de population ↔ PM2.5 
dens = trouve_col(["densite_population", "densite_de_population", "population_density", "densite(hab/km2)"])
if dens and pm25:
    st.subheader("Corrélation Densité de population × PM2.5 (Pearson)")
    r = df[[dens, pm25]].corr().iloc[0, 1]
    st.write(f"Pearson = **{r:.3f}**")

    fig2, ax2 = plt.subplots()
    ax2.scatter(df[dens], df[pm25], alpha=0.6)
    ax2.set_xlabel(dens)
    ax2.set_ylabel(pm25)
    ax2.set_title("Nuage de points : densité × PM2.5")
    st.pyplot(fig2)

# 6) Quartiles du CO
co = trouve_col(["co", "monoxyde_de_carbone"])
if co:
    st.subheader("Quartiles du CO")
    st.write(df[co].quantile([0.25, 0.5, 0.75]).rename(index={0.25: "Q1", 0.5: "Q2 (médiane)", 0.75: "Q3"}))
