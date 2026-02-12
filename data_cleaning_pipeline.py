import pandas as pd

# Chargement
df_exp = pd.read_csv('expeditions_knaufindustries.csv')
df_cli = pd.read_json('clients_knaufindustries.json')
df_hubs = pd.read_excel('hubs_knaufindustries.xlsx')

# Fusion 
df_merge = pd.merge(df_exp, df_cli, on='client_id', how='left')
df_final = pd.merge(df_merge, df_hubs, left_on='hub', right_on='hub_name', how='left')

print("valeurs manquantes par variable")
identification = df_final.isnull().sum()
print(identification)

# Identification ciblée sur MedLog
print(df_final[df_final['company'] == 'MedLog'][['company', 'city', 'sector']])


# correction
# imputation déduite
df_final['city'] = df_final['city'].fillna('Marseille')

# vérification
print("Vérification")
apres = df_final['city'].isnull().sum()
print(f"Nombre de valeurs manquantes dans 'city' : {apres}")

# Aperçu 
print("\nAperçu des données MedLog:")
print(df_final[df_final['company'] == 'MedLog'][['company', 'city']].head(5))

nb_lignes_python = len(df_final)
print(f"nbre de ligne avant chargement : {nb_lignes_python} lignes")


from sqlalchemy import create_engine
#connexion à la base
engine = create_engine('postgresql://postgres:admin@localhost:5432/knauf_industries')

#chargement
# on charge le df dans une nouvelle table
df_final.to_sql('t_logistique_nettoyee', engine, if_exists='replace', index=False)

print("Données chargées avec succès!")
