# 🚛 Supply Chain Data Pipeline & SQL Optimization

![Python](https://img.shields.io/badge/Python-Pandas-3776AB?style=for-the-badge&logo=python&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Optimization-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![ETL](https://img.shields.io/badge/Data_Engineering-ETL-green?style=for-the-badge)

## 📋 Executive Summary
Ce projet vise à optimiser la logistique de **KNAUF Industries** en centralisant des données hétérogènes dispersées.

L'objectif était de construire une **Architecture Data Robuste** capable de traiter des milliers d'expéditions pour analyser les coûts de transport, les retards et l'empreinte carbone.

### 🎯 Résultats Clés
* **Qualité de Données :** Sauvetage de **100%** du dataset critique via des stratégies d'imputation avancées (Médiane/Logique métier).
* **Performance SQL :** Réduction du temps d'exécution des requêtes de **25%** (325ms $\to$ 244ms).
* **Sécurité :** Mise en place d'une gestion des accès (RBAC) conforme aux principes de moindre privilège.

---

## ⚙️ Architecture Technique

### 1. Ingestion & ETL (Extract, Transform, Load)
Le défi principal résidait dans l'hétérogénéité des sources de données :
* **Clients :** Format `JSON` (Semi-structuré).
* **Expéditions :** Format `CSV` (Plat).
* **Hubs Logistiques :** Format `Excel` (Propriétaire).

> **Solution :** Développement d'un script Python (`pandas`) pour normaliser ces flux, gérer les encodages et typer les données avant l'insertion en base.

### 2. Data Cleaning & Qualité
Les données brutes (JSON, CSV, Excel) contenaient des incohérences, notamment sur la localisation des clients.

| Colonne | Problème | Stratégie de Nettoyage (Code Python) |
| :--- | :--- | :--- |
| `city` (Client) | Valeurs manquantes (NULL) pour le transporteur "MedLog" | **Imputation Déductive** (Correction basée sur la logique métier : MedLog est basé à Marseille $\to$ `fillna`). |
| `Join Keys` | Données dispersées (Excel vs CSV) | **Unification des clés** (`client_id`, `hub`) pour garantir la cohérence avant l'export SQL. |

### 3. Modélisation & Base de Données (PostgreSQL)
Conception d'un schéma en étoile (Star Schema) pour faciliter les analyses BI :
* **Table de Fait :** `t_logistique` (Expéditions, Coûts, Délais).
* **Dimensions :** `t_clients`, `t_hubs`.

---

## 🚀 Optimisation & Performance SQL

L'analyse des plans d'exécution (`EXPLAIN ANALYZE`) a révélé des lenteurs sur les agrégations temporelles.

**Action :** Création d'index ciblés sur les colonnes de filtrage fréquent.

```sql
-- Création d'index pour accélérer les recherches par date et code postal
CREATE INDEX idx_date_expedition ON t_logistique(date_expedition);
CREATE INDEX idx_code_postal ON t_clients(code_postal);

```

## ⚡ Impact Mesuré
* Temps sans index : 325 ms
* Temps avec index : 244 ms
* Gain de performance : ~25%

## 🛡️ Sécurité & Gouvernance (Security-Aware)
* En application des bonnes pratiques de cybersécurité :

* Création d'utilisateurs spécifiques (analyst_logistique).

* Restriction des droits : Attribution stricte des privilèges SELECT uniquement sur les tables nécessaires, interdiction des commandes DROP ou ALTER pour les utilisateurs finaux.

```SQL
-- Exemple de gestion des privilèges (Principe du moindre privilège)
CREATE USER analyst_logistique WITH PASSWORD 'secure_pass';
GRANT CONNECT ON DATABASE knauf_db TO analyst_logistique;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO analyst_logistique; 
```

## 🛠️ Comment utiliser ce projet ?
Cloner le repo :
```Bash
git clone https://github.com/aml08/Supply-Chain-Data-Pipeline-Optimization.git
```

Installer les dépendances :
```Bash
pip install pandas sqlalchemy psycopg2

```

Lancer le pipeline ETL :
```Bash
python data_cleaning_pipeline.py 

```

Projet réalisé dans le cadre du Master Data - Validation des compétences d'Architecture de Données.
