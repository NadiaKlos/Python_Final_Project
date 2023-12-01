import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import time
from sklearn.preprocessing import OrdinalEncoder
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import cross_val_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier


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

st.header("Modeling 🧐")
st.write("The goal is to determine the early readmission of the patient within 30 days of discharge.")
st.title("Why is the column ‘readmitted’ our target ?")
st.write("Predicting readmission is crucial in the medical field. By identifying patients at high risk of readmission, healthcare professionals can take preventive measures, such as post-hospital follow-up, adjusting medications, or scheduling follow-up appointments, to reduce the risk of readmission.")
st.title("Why do we use classification models ?")
st.write("The use of classification models is appripriate here. The ‘readmitted’ column is categorical, indicating whether a patient is readmitted or not. Since we're looking to predict a specific class (readmitted or non-readmitted), classification is the appropriate task. ")
st.write("🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺🔺")
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
#with st.spinner("Chargement en cours..."):
    # Simulation d'une tâche prenant du temps
 #   for percent_complete in range(0, 101, 10):
  #      time.sleep(0.5)
        
   #     progress_message.text(f"Wait a moment please😴... : {percent_complete}%")
        
        

categorical_data = diabetic_data.select_dtypes(include=['object'])
numerical_data = diabetic_data.select_dtypes(include=['int64','float64'])

encoder = OrdinalEncoder().set_output(transform="pandas")
data_encoded = encoder.fit_transform(categorical_data)
diabetic_data_enc = pd.concat([numerical_data, data_encoded], axis=1)
target_name = "readmitted"
Y = diabetic_data_enc[target_name]
X = diabetic_data_enc.drop(columns=[target_name])
x_train, x_test, y_train, y_test = train_test_split(X,Y, test_size=0.2,random_state=42)
scaler = StandardScaler()
x_train_scaled = scaler.fit_transform(x_train)
x_test_scaled = scaler.transform(x_test)


#RANDOM FOREST
st.header("RandomForest")

st.markdown("The best hyperparameters are : **max_depth=20, min_samples_split=2, n_estimators= 200**")
st.markdown("With these hyperparameters we have **62.12  %** of accuracy \n But you can choose other values if you want to try :")

#on laisse la choix à l'utilisateur de choisir les paramètres qu'il veut tester
max_depth = st.slider('Max Depth', min_value=1, max_value=100, value=20)
min_samples_split = st.slider('Min Samples Split', min_value=2, max_value=10, value=2)
n_estimators = st.slider('Number of Estimators', min_value=1, max_value=500, value=200)
# Créer et entraîner le modèle avec les paramètres choisis par l'utilisateur
if st.button('Ok🟩'):
    with st.spinner('The model is running🏃🏃🏃...'):
        best_rf_model = RandomForestClassifier(max_depth=max_depth, min_samples_split=min_samples_split, n_estimators=n_estimators)
        best_rf_model.fit(x_train_scaled, y_train)
        y_pred_rf = best_rf_model.predict(x_test_scaled)
        accuracy_rf = accuracy_score(y_test, y_pred_rf)
        st.success('It is over 🎉!')
        st.write("With your selection we have ", np.round(accuracy_rf*100,2)," % of accuracy")

#KNN
st.header("K-Nearest Neighbors (KNN)")
st.markdown("The best hyperparameters are : **n_neighbors= 7, weights= 'distance'**")
st.markdown("With these hyperparameters we have **55.69  %** of accuracy \n But you can choose other values if you want to try :")

#on laisse la choix à l'utilisateur de choisir les paramètres qu'il veut tester
n_neighbors = st.slider('Nombre de voisins (K)', min_value=1, max_value=50, value=5)
weights = st.selectbox('Poids des voisins', ['uniform', 'distance'])
# Créer et entraîner le modèle avec les paramètres choisis par l'utilisateur
if st.button('Ok🟪'):
    with st.spinner('The model is running🏃🏃🏃...'):
        knn_model = KNeighborsClassifier(n_neighbors=n_neighbors, weights=weights)
        knn_model.fit(x_train_scaled, y_train)
        y_pred_knn = knn_model.predict(x_test_scaled)
        accuracy_knn = accuracy_score(y_test, y_pred_knn)
        st.success('It is over 🎉!')
        st.write("With your selection we have ", np.round(accuracy_knn*100,2)," % of accuracy")

#Decision Tree 
st.header("Decision Tree")

st.markdown("The best hyperparameters are : **criterion= 'gini', max_depth= 5, min_samples_leaf= 2, min_samples_split= 2**")
st.markdown("With these hyperparameters we have **60.25  %** of accuracy \n But you can choose other values if you want to try :")

#on laisse la choix à l'utilisateur de choisir les paramètres qu'il veut tester
max_depth_dt = st.slider('Max Depth', min_value=1, max_value=50, value=5)
criterion = st.selectbox('Criterion', ['gini', 'entropy'])
# Créer et entraîner le modèle avec les paramètres choisis par l'utilisateur
if st.button('Ok🟦'):
    with st.spinner('The model is running🏃🏃🏃...'):
        dt_model = DecisionTreeClassifier(max_depth=max_depth_dt, criterion=criterion)
        dt_model.fit(x_train, y_train)
        y_pred_dt = dt_model.predict(x_test_scaled)
        accuracy_dt = accuracy_score(y_test, y_pred_dt)
        st.success('It is over 🎉!')
        st.write("With your selection we have ", np.round(accuracy_dt*100,2)," % of accuracy")





