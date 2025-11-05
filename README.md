#  Projet 1 – Qualité de l’Air et Pollution (Streamlit)
**Institut Teccart – 420-IAA-TT – Automne 2025**

##  Objectifs
- Explorer et comprendre la structure du dataset (taille, types, valeurs manquantes).
- Nettoyer les données (imputation: médiane pour numériques, mode pour catégorielles).
- Analyse descriptive: moyenne, médiane, écart-type, quartiles.
- Visualisations: histogrammes, densités, boxplots, scatter matrix, pairplot.
- Corrélations: Pearson/Spearman/Kendall + heatmap.
- Répondre aux 11 questions du sujet (voir section Résultats).

## Données
- Variables: Température, Humidité, PM2.5, PM10, NO2, SO2, CO, Proximité zones industrielles, Densité de population, **Qualité de l’air (cible 0–3)**.
- Fichier: `data/pollution.csv`.

##  Nettoyage
- Imputation opcional via UI (checkbox): médiane (num), mode (cat).
- Outliers: IQR reportado para PM2.5 et PM10.

##  Résultats (exemples)
- **Taille**: *N* lignes × *M* colonnes.
- **Valeurs manquantes**: tabela por coluna; opção de substituição aplicada.
- **Top 3 facteurs corrélés à la qualité de l’air**: … (listar a saída do app)
- **PM2.5/PM10**: médias, médianes, écarts-types; outliers detectados.
- **Humidité × Qualité**: rho Spearman = …
- **Densité × PM2.5**: r Pearson = …
- **Quartiles CO**: Q1=…, Médiane=…, Q3=…

