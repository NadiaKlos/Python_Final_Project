import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(
    page_title="Python Final Project",
    page_icon="📚",
)
st.sidebar.image("https://formation-continue.ehesp.fr/sites/default/files/styles/crop_actu_desktop_800x540/public/content/news/img/shutterstock_1917115745_0.jpg?h=4b45c30e&itok=UCzG6up_")
st.sidebar.markdown("## **Subject Area** :\n*__Health and Medicine__*")
st.sidebar.markdown("## **Dataset Characteristics** :\n*__Multivariate__*")
st.sidebar.markdown("## **Feature Type** :\n*__Categorical, Integer__*")
with st.sidebar:
    openai_api_key = "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"
    "[View the source of the dataset](https://archive.ics.uci.edu/dataset/296/diabetes+130-us+hospitals+for+years+1999-2008)"
    "[View the source code (GitHub)](https://github.com/NadiaKlos/Python_Final_Project)"

st.header("About the patients 💊")
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

progress_message = st.empty()

# Affiche un spinner pendant le chargement
with st.spinner("Chargement en cours..."):
    # Simulation d'une tâche prenant du temps
    for percent_complete in range(0, 101, 10):
        time.sleep(0.5)
        
        progress_message.text(f"Wait a moment please😴... : {percent_complete}%")
st.title("Gender repartition")       
plt.figure(figsize=(15, 8))
sns.countplot(y='gender', data=diabetic_data, palette='husl')
plt.title('Répartition des Genres')
plt.ylabel('Genre')
plt.xlabel('Nombre de Patients')
st.pyplot()
st.write("We can note that the elderly and women were the most affected by diabetes between 1999 and 2008 in US hospitals.")

st.title("Patients age repartition")
plt.figure(figsize=(15, 8))
sns.histplot(diabetic_data['age'], bins=20, kde=True)
plt.title("Suivi de l'age des diabétiques")
plt.xlabel('Âge')
plt.ylabel('Fréquence')
st.pyplot()

st.title("Races repartition")
race_counts = diabetic_data['race'].value_counts()
plt.subplots(figsize=(15, 8))
colors = sns.color_palette('pastel')[0:len(race_counts)]
labels = race_counts.index
explode = [0.1]* len(race_counts)   # on sépare légèrement chaque tranche pour les mettre en évidence
plt.pie(race_counts, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140, explode=explode)
plt.title('Répartition des races')
st.pyplot()
st.write("We note that the Caucasian population is largely represented among diabetics treated in the 130 American hospitals between 1999 and 2008. But this distribution must be put into perspective since it illustrates the state of the American population.")



