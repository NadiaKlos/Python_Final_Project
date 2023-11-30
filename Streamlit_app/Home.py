import streamlit as st 
import pandas as pd
import numpy as np

st.set_page_config(
    page_title="Python Final Project",
    page_icon="📚",
)

st.header("HOMEPAGE")
st.title("Welcome to you DataScience App !")
st.write("Here, you can see, interpret and modeling your data.")
st.image('https://cdn.rentechdigital.com/common_files/blogs/what-is-data-science-and-how-can-it-influence-decision-making-swipecart-blog-img-02-01-07-2022.gif')

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
    

st.markdown("The dataset represents ten years (1999-2008) of clinical care at 130 US hospitals and integrated delivery networks. Each row concerns hospital records of patients diagnosed with diabetes, who underwent laboratory, medications, and stayed up to 14 days.")
st.write("Your dataset : ",diabetic_data.head(30))
st.write("Some precisions about the dataset :")
st.write("Number of Lines : ", diabetic_data.shape[0])
st.write("Number of Columns : ", diabetic_data.shape[1])



