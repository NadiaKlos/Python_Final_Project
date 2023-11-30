import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns

st.set_option('deprecation.showPyplotGlobalUse', False)

st.header("Inside the hospitals")

diabetic_data=pd.read_csv('diabetic_data.csv')
diabetic_data.replace('?', np.nan, inplace=True)
#on fitre sur les colonnes qui contiennent moins de 50000 données manquantes
moins_de_50_mille=diabetic_data.isna().sum()[(diabetic_data.isna().sum() < 50000) & (diabetic_data.isna().sum()>0)]
#on les supprime
diabetic_data = diabetic_data.dropna(subset=moins_de_50_mille.index)
# on remplace les intervalles de la colonne age par par la moyenne en integer
age_mapping = {'[70-80)': 75, '[60-70)': 65, '[50-60)': 55, '[80-90)': 85, '[40-50)': 45, '[30-40)': 35, '[90-100)': 95, '[20-30)': 25, '[10-20)': 15, '[0-10)': 5}

diabetic_data['age'] = diabetic_data['age'].replace(age_mapping)

#on remplace les intervalles de la colonne weight par des nombres
weight_mapping = {'[75-100)': (75+100)//2, '[50-75)': (50+75)//2, '[100-125)': (100 + 125) // 2, '[125-150)': (125 + 150) // 2, '[25-50)': (25 + 50) // 2, '[0-25)': (0 + 25) // 2, '[150-175)': (150 + 175) // 2, '[175-200)': (175 + 200) // 2}

diabetic_data['weight'] = diabetic_data['weight'].replace(weight_mapping)

# Convertir les valeurs de la colonne 'weight' en nombres
diabetic_data['weight'] = pd.to_numeric(diabetic_data['weight'], errors='coerce')

# Remplacer les valeurs manquantes par la moyenne
diabetic_data['weight'].fillna(diabetic_data['weight'].mean(), inplace=True)
#on supprime les colonnes max_glu-result et A1Cresult
diabetic_data=diabetic_data.drop(['max_glu_serum','A1Cresult'],axis=1)
    

medicines_data = diabetic_data.columns[24:45]

# Filtrer les données pour exclure les valeurs 'No'
filtered_data = diabetic_data[medicines_data][(diabetic_data[medicines_data] == 'Down') | (diabetic_data[medicines_data] == 'Steady') | (diabetic_data[medicines_data] == 'Up')]

# Créer le graphique
plt.figure(figsize=(15, 8))
sns.countplot(data=pd.melt(filtered_data), x='value', hue='variable')
plt.title('Medicines')
plt.xlabel('Level')
plt.legend(title='Colonnes', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot()