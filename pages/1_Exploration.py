import streamlit as st
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from pandas.plotting import scatter_matrix

st.title("Exploration des données")

# --- ler CSV ---
try:
    df = pd.read_csv("data/pollution.csv")
except Exception as e:
    st.error(f"Erreur de lecture du fichier CSV: {e}")
    st.stop()

# --- afficher les données ---
st.subheader("Afficher les données (5 premières lignes)")
st.dataframe(df.head())

st.subheader("Statistiques descriptives")
st.dataframe(df.describe())

st.subheader("Dimensions (lignes, colonnes)")
st.write(df.shape)

st.subheader("Types des données")
st.write(df.dtypes)

st.subheader("Valeurs manquantes (par colonne)")
st.write(df.isna().sum())

# --- Histogrammes  ---
st.subheader("Histogramme")
num_cols = df.select_dtypes(include=np.number).columns.tolist()
if num_cols:
    col_hist = st.selectbox("Choisir une colonne numérique :", num_cols)
    fig, ax = plt.subplots()
    ax.hist(df[col_hist].dropna(), bins=20, edgecolor='black')
    ax.set_xlabel(col_hist)
    ax.set_ylabel("Fréquence")
    st.pyplot(fig)

# --- Graphiques de densité  ---
st.subheader("Graphes de densité (toutes les colonnes numériques)")
if num_cols:
    fig = plt.figure(figsize=(12, 8))
    df[num_cols].plot(kind='density', subplots=True, layout=(min(3, len(num_cols)), -1), sharex=False, sharey=False, figsize=(15, 10))
    st.pyplot(plt.gcf())

# --- Boxplots (boîtes à moustaches) ---
st.subheader("Boîtes à moustaches (toutes les colonnes numériques)")
if num_cols:
    fig = plt.figure(figsize=(12, 8))
    df[num_cols].plot(kind='box', subplots=True, layout=(min(3, len(num_cols)), -1), sharex=False, sharey=False, figsize=(15, 10))
    st.pyplot(plt.gcf())

# --- Scatter matrix  ---
st.subheader("Diagramme de dispersion (scatter matrix)")
if num_cols:
    fig = plt.figure(figsize=(10, 10))
    scatter_matrix(df[num_cols].dropna(), figsize=(10, 10))
    st.pyplot(plt.gcf())

# --- Pairplot ---
st.subheader("Pairplot (sélection de 2 à 4 colonnes numériques)")
if num_cols:
    cols_escolhidas = st.multiselect("Choisissez 2 à 4 colonnes :", num_cols, default=num_cols[:3])
    if 2 <= len(cols_escolhidas) <= 4:
        g = sns.pairplot(df[cols_escolhidas].dropna())
        st.pyplot(g.fig)
