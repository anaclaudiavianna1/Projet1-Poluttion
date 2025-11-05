import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math
from pandas.plotting import scatter_matrix


st.title("Exploration des données")

# 1) Lecture du CSV
try:
    df = pd.read_csv("data/pollution.csv")
except Exception:
    st.error("Erreur de lecture du fichier CSV.")
    st.stop()

# 2) Aperçu des données
st.subheader("Aperçu (5 premières lignes)")
st.dataframe(df.head())

# 3) Statistiques
st.subheader("Statistiques descriptives")
st.write(df.describe())

# 4) Dimensions
st.subheader("Dimensions (lignes, colonnes)")
st.write(df.shape)

# 5) Types de données 
st.subheader("Types des données")
st.dataframe(pd.DataFrame(df.dtypes, columns=["Type"]))

# 6) Valeurs manquantes
st.subheader("Valeurs manquantes (par colonne)")
st.dataframe(pd.DataFrame(df.isna().sum(), columns=["Valeurs manquantes"]))

# 7) Histogramme d'une colonne numérique
st.subheader("Histogramme")
num_cols = df.select_dtypes(include=np.number).columns.tolist()
if num_cols:
    col_h = st.selectbox("Colonne numérique :", num_cols)
    bins = st.slider("Nombre de classes (bins)", 5, 60, 20)
    fig, ax = plt.subplots()
    ax.hist(df[col_h].dropna(), bins=bins, edgecolor="black")
    ax.set_xlabel(col_h)
    ax.set_ylabel("Fréquence")
    st.pyplot(fig)

# 8) Densité 
st.subheader("Graphes de densité")
if num_cols:
    n = len(num_cols)
    cols_grid = 3
    rows_grid = math.ceil(n / cols_grid)
    df[num_cols].plot(
        kind="density",
        subplots=True,
        layout=(rows_grid, cols_grid),
        sharex=False, sharey=False,
        figsize=(12, 4*rows_grid)
    )
    st.pyplot(plt.gcf())

# 9) Boîtes à moustaches
st.subheader("Boîtes à moustaches")
if num_cols:
    n = len(num_cols)
    cols_grid = 3
    rows_grid = math.ceil(n / cols_grid)
    df[num_cols].plot(
        kind="box",
        subplots=True,
        layout=(rows_grid, cols_grid),
        sharex=False, sharey=False,
        figsize=(12, 4*rows_grid)
    )
    st.pyplot(plt.gcf())


# 10) Matrice de dispersion
st.subheader("Diagramme de dispersion (scatter matrix)")
if num_cols:
    fig_scatter = plt.figure(figsize=(12, 12))
    scatter_matrix(df[num_cols], alpha=0.6, diagonal='kde', ax=fig_scatter.gca())
    st.pyplot(fig_scatter)

# 11) Pairplot (2 à 4 colonnes)
st.subheader("Pairplot (2 à 4 colonnes)")
if len(num_cols) >= 2:
    selected_cols = st.multiselect("Sélectionnez 2 à 4 colonnes numériques :", num_cols, default=num_cols[:2])
    if 2 <= len(selected_cols) <= 4:
        fig_pair = sns.pairplot(df[selected_cols].dropna())
        st.pyplot(fig_pair)
    else:
        st.warning("Veuillez sélectionner entre 2 et 4 colonnes.")


