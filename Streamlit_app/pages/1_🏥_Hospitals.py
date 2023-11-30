import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import time
st.set_page_config(
    page_title="Python Final Project",
    page_icon="📚",
)
st.set_option('deprecation.showPyplotGlobalUse', False)

st.header("Inside the hospitals ⛑️")

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
progress_message = st.empty()

# Affiche un spinner pendant le chargement
with st.spinner("Chargement en cours..."):
    # Simulation d'une tâche prenant du temps
    for percent_complete in range(0, 101, 10):
        time.sleep(0.5)
        
        progress_message.text(f"Wait a moment please😴... : {percent_complete}%")

# Créer le graphique
st.title("Les traitements utilisés")
plt.figure(figsize=(15, 8))
sns.countplot(data=pd.melt(filtered_data), x='value', hue='variable')
plt.title('Medicines')
plt.xlabel('Level')
plt.legend(title='Colonnes', bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot()
st.write("We note that insulin was the most used product in American hospitals between 1999 and 2008 to treat diabetes. This is still the case today.")

st.title("Distribution du temps à l\'hôpital")
plt.figure(figsize=(10, 6))
diabetic_data['time_in_hospital'].value_counts().sort_index().plot(kind='bar', color='green')
plt.title('Distribution du temps à l\'hôpital')
plt.xlabel('Temps à l\'hôpital (en jours)')
plt.ylabel('Nombre de patients')
st.pyplot()
st.write("This graph shows that in general, patients spend very little time in hospital, between 2 and 4 days, and no one spends more than 2 weeks. This shows that this pathology was quite easily treated in American hospitals, without major complications.")

st.title("État des Readmissions")

# Créez un graphique avec Matplotlib
fig, ax = plt.subplots(figsize=(8, 8))
sns.countplot(x='readmitted', data=diabetic_data, palette='viridis')
plt.title('État des Readmissions')
plt.xlabel('Readmission')
plt.ylabel('Nombre de patients')

# Affichez le graphique dans l'application Streamlit
st.pyplot(fig)
st.write("As a result, 56.64% of patients are not readmitted, 32.68% are readmitted more than 30 days after discharge, and only 10.68% less than 30 days later.")

