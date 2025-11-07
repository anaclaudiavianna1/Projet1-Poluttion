import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


st.set_page_config(page_title="Qualité de l’air – Projet Streamlit", layout="wide")
st.title("Étude de la Qualité de l’Air et de la Pollution")

# -----------------------------
# 1) Chargement des données
# -----------------------------
@st.cache_data
def charger_donnees(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

try:
    df = charger_donnees("data/pollution.csv")
except Exception:
    st.error("Erreur de lecture du fichier CSV (attendu : data/pollution.csv).")
    st.stop()


if "df_work" not in st.session_state:
    st.session_state["df_work"] = df.copy()

# -----------------------------
# Menu latéral
# -----------------------------
st.sidebar.title("Navigation")
section = st.sidebar.selectbox(
    "Aller à",
    ["Accueil (aperçu)", "Nettoyage des données", "Analyse descriptive",
     "Corrélations", "Visualisations", "Conclusions"]
)

# colonnes numériques
dfw = st.session_state["df_work"]
num_cols = dfw.select_dtypes(include=np.number).columns.tolist()

# -----------------------------
# ACCUEIL
# -----------------------------
if section == "Accueil (aperçu)":
    st.markdown("**Objectif :** explorer un jeu de données sur la qualité de l’air et présenter une analyse simple et claire.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Aperçu (5 premières lignes)")
        st.dataframe(df.head())
        st.subheader("Dimensions (lignes, colonnes)")
        st.write(df.shape)
    with col2:
        st.subheader("Types des données")
        st.dataframe(pd.DataFrame(df.dtypes, columns=["Type"]))
        st.subheader("Valeurs manquantes (par colonne)")
        st.dataframe(pd.DataFrame(df.isna().sum(), columns=["Valeurs manquantes"]))

# -----------------------------
# NETTOYAGE
# -----------------------------
elif section == "Nettoyage des données":
    st.subheader("Nettoyage des données")
    st.caption("Détection et traitement des valeurs **manquantes** et **aberrantes** (IQR).")

    st.markdown("**Valeurs manquantes (avant traitement)**")
    st.dataframe(pd.DataFrame(dfw.isna().sum(), columns=["Manquantes"]))

    # Imputation simple
    if st.checkbox("Remplacer les valeurs manquantes (numériques → médiane, catégorielles → mode)"):
        df_work = dfw.copy()

        num_all = df_work.select_dtypes(include=np.number).columns
        for c in num_all:
            df_work[c] = df_work[c].fillna(df_work[c].median())

        cat_all = [c for c in df_work.columns if c not in num_all]
        for c in cat_all:
            if df_work[c].isna().any():
                mode_val = df_work[c].mode(dropna=True)
                if not mode_val.empty:
                    df_work[c] = df_work[c].fillna(mode_val.iloc[0])

        st.session_state["df_work"] = df_work
        dfw = df_work
        num_cols = dfw.select_dtypes(include=np.number).columns.tolist()
        st.success("Imputation appliquée.")

    st.markdown("**Valeurs manquantes (après traitement)**")
    st.dataframe(pd.DataFrame(dfw.isna().sum(), columns=["Manquantes"]))

    st.markdown("---")
    st.markdown("**Détection d’aberrantes (IQR) sur une colonne numérique**")
    if num_cols:
        col_out = st.selectbox("Colonne :", num_cols)
        s = dfw[col_out].dropna()
        q1, q3 = s.quantile(0.25), s.quantile(0.75)
        iqr = q3 - q1
        bas, haut = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        n_out = int(((s < bas) | (s > haut)).sum())
        st.write(f"IQR = {iqr:.3f} | Limites : [{bas:.3f}, {haut:.3f}] | Outliers : **{n_out}**")

        fig, ax = plt.subplots()
        ax.boxplot(s, vert=True, labels=[col_out])
        ax.set_title("Boîte à moustaches")
        st.pyplot(fig)

# -----------------------------
# ANALYSE DESCRIPTIVE
# -----------------------------
elif section == "Analyse descriptive":
    st.subheader("Analyse descriptive (moyenne, médiane, écart-type, quartiles)")
    if num_cols:
        st.dataframe(dfw[num_cols].describe().T)

    # petite fonction pour trouver un nom de colonne par alias
    def trouver(noms_possibles):
        for c in dfw.columns:
            if c.strip().lower() in [n.lower() for n in noms_possibles]:
                return c
        return None

    # PM2.5 / PM10 
    pm25 = trouver(["pm2.5", "pm2_5", "pm25"])
    pm10 = trouver(["pm10", "pm_10"])
    if pm25 or pm10:
        st.markdown("**Statistiques PM2.5 / PM10**")
        lignes = []
        for nom in [pm25, pm10]:
            if nom:
                lignes.append({
                    "Mesure": nom,
                    "Moyenne": dfw[nom].mean(),
                    "Médiane": dfw[nom].median(),
                    "Écart-type": dfw[nom].std(),
                    "Q1": dfw[nom].quantile(0.25),
                    "Q3": dfw[nom].quantile(0.75),
                })
        st.dataframe(pd.DataFrame(lignes))

    # CO – quartiles 
    co_col = trouver(["co", "monoxyde_de_carbone"])
    if co_col:
        st.markdown("**Quartiles du CO**")
        q = dfw[co_col].quantile([0.25, 0.5, 0.75]).rename(
            index={0.25: "Q1", 0.5: "Médiane (Q2)", 0.75: "Q3"}
        )
        st.write(q)

# -----------------------------
# CORRÉLATIONS
# -----------------------------
elif section == "Corrélations":
    st.subheader("Corrélations entre variables")
    if len(num_cols) >= 2:
        # Pearson (numérique)
        st.markdown("**Matrice de corrélation (Pearson)**")
        corr = dfw[num_cols].corr()
        st.dataframe(corr)

        st.markdown("**Heatmap (Pearson)**")
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(corr, cmap="coolwarm", annot=True, fmt=".2f", ax=ax)
        st.pyplot(fig)

    # Densité de population × PM2.5
    dens_col = None
    for cand in ["densite_population", "densité_population", "population_density", "densite_de_population"]:
        for c in dfw.columns:
            if c.lower() == cand:
                dens_col = c
                break
        if dens_col:
            break

    pm25_col = None
    for cand in ["pm2.5", "pm2_5", "pm25"]:
        for c in dfw.columns:
            if c.lower() == cand:
                pm25_col = c
                break
        if pm25_col:
            break

    if dens_col and pm25_col:
        st.markdown("**Lien entre la densité de population et PM2.5**")
        r = dfw[[dens_col, pm25_col]].corr().iloc[0, 1]
        st.write(f"Corrélation (Pearson) = **{r:.2f}**")
        fig_sc, ax_sc = plt.subplots()
        ax_sc.scatter(dfw[dens_col], dfw[pm25_col], alpha=0.6)
        ax_sc.set_xlabel(dens_col)
        ax_sc.set_ylabel(pm25_col)
        st.pyplot(fig_sc)

    # Spearman avec la cible ordinale (si existe)
    cible = None
for cand in ["qualite_air", "qualité_air", "quality", "target", "airquality", "variable_cible"]:
    for c in dfw.columns:
        if c.lower() == cand:
            cible = c
            break
    if cible:
        break
    

if cible and cible in dfw.columns and len(num_cols) >= 1:
    st.markdown(f"**Corrélations Spearman avec la cible** : `{cible}`")
    cols_for_corr = list(dict.fromkeys(num_cols + [cible]))
    sp = dfw[cols_for_corr].corr(method="spearman")[cible].drop(cible)
    
    df_spear = sp.to_frame(name="Spearman").reset_index(names="Variable")
    st.dataframe(df_spear)

# -----------------------------
# VISUALISATIONS
# -----------------------------
elif section == "Visualisations":
    st.subheader("Histogramme")
    if num_cols:
        col_h = st.selectbox("Colonne numérique :", num_cols)
        bins = st.slider("Nombre de classes (bins)", 5, 60, 20)
        fig, ax = plt.subplots()
        ax.hist(dfw[col_h].dropna(), bins=bins, edgecolor="black")
        ax.set_xlabel(col_h)
        ax.set_ylabel("Fréquence")
        st.pyplot(fig)

    st.markdown("---")
    st.subheader("Boîtes à moustaches")
    if num_cols:
        mode_box = st.radio(
            "Mode d’affichage :",
            ["Un boxplot par variable (échelles indépendantes)",
             "Tous ensemble (échelle log)"],
            index=0
        )

        if mode_box == "Un boxplot par variable (échelles indépendantes)":
            for col in num_cols:
                fig_b, ax_b = plt.subplots()
                ax_b.boxplot(dfw[col].dropna(), vert=True, labels=[col])
                ax_b.set_title(f"Boxplot – {col}")
                st.pyplot(fig_b)
        else:
            fig2, ax2 = plt.subplots(figsize=(8, 4))
            dfw[num_cols].plot(kind="box", grid=True, ax=ax2, logy=True)
            ax2.set_title("Boxplots (toutes les variables, échelle logarithmique)")
            st.pyplot(fig2)

# -----------------------------
# CONCLUSIONS
# -----------------------------
elif section == "Conclusions":
    st.subheader("Conclusions et analyses (rapport bref)")

    # Taille du jeu de données et valeurs manquantes
    nb_lignes, nb_col = dfw.shape
    nb_nan = int(dfw.isna().sum().sum())
    st.markdown(
        f"- **Jeu de données :** {nb_lignes} lignes × {nb_col} colonnes.\n"
        f"- **Valeurs manquantes restantes :** {nb_nan}."
    )

    # Indicateur simple sur PM2.5 (si présent)
    pm25_col = None
    for cand in ["pm2.5", "pm2_5", "pm25"]:
        for c in dfw.columns:
            if c.lower() == cand:
                pm25_col = c
                break
        if pm25_col:
            break

    if pm25_col:
        st.markdown(
            f"- **PM2.5** moyenne : **{dfw[pm25_col].mean():.2f}**, "
            f"médiane : **{dfw[pm25_col].median():.2f}**."
        )

    # Top 3 facteurs les plus corrélés avec la cible (si existe)
    cible = None
    for cand in ["qualite_air", "quality", "airquality", "target", "variable_cible"]:
        for c in dfw.columns:
            if c.lower() == cand:
                cible = c
                break
        if cible:
            break

    if cible and cible in dfw.columns:
        num_cols = dfw.select_dtypes(include=np.number).columns.tolist()
        if cible in num_cols:
            corr_s = dfw[num_cols].corr()[cible].drop(cible).abs().sort_values(ascending=False).head(3)
            st.markdown("**Facteurs les plus corrélés avec la qualité de l’air :**")
            for nom, val in corr_s.items():
                st.markdown(f"- {nom} (|r| = {val:.2f})")

    # Conclusion écrite
    st.subheader("Conclusion générale")
    st.markdown("""
**Synthèse.** La qualité de l’air varie surtout avec **PM2.5**, **PM10**, **NO2** et **SO2**.
Les variables météorologiques (température, humidité) jouent un rôle plus modéré, tandis
que la densité de population et la proximité des zones industrielles peuvent accentuer
les concentrations de particules.

**Points saillants.**
- Les particules fines (**PM2.5**) et grossières (**PM10**) expliquent une grande part des variations.
- **NO2** et **SO2** sont des marqueurs pertinents d’activités urbaines/industrielles.
- Après nettoyage, le jeu de données reste cohérent pour l’analyse.

**Conclusion.** Globalement, la pollution est surtout influencée par les particules et certains gaz
d’origine anthropique. Il est conseillé de suivre régulièrement ces indicateurs et
de renforcer la prévention dans les zones les plus exposées.
""")
