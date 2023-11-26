import lime
import pandas as pd
import numpy as np
from lime import lime_tabular
from sklearn.model_selection import train_test_split
from sklearn.ensemble import AdaBoostClassifier
X = pd.read_csv("statics/feature_data.csv")
y = pd.read_csv("statics/class_data.csv")
FILE_NUMBER = 1
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)
ada = AdaBoostClassifier(n_estimators=100, random_state=0)
ada.fit(X_train, y_train)
from .ml_model import open_model
model = open_model('model.pkl')
interpreter = lime_tabular.LimeTabularExplainer(
        training_data=np.array(X_train),
        feature_names=X_train.columns,
        mode="classification"
)
def prediction_explain(input):
    input_series = pd.Series(data=input,
                             index=['statuses_count','followers_count','friends_count','favourites_count','listed_count','geo_enabled','profile_use_background_image','lang_num'],
                             dtype=float,name="input_data")
    
    exp = interpreter.explain_instance(data_row=input_series,predict_fn=ada.predict_proba)
    #exp.save_to_file("accounts/templates/accounts/explanation.html",labels=None,predict_proba=True,show_predicted_value=True)
    data = exp.as_html(labels=None,predict_proba=True,show_predicted_value=True)
    data = data.replace("* _.templateSettings.interpolate = /{{([\s\S]+?)}}/g;","")
    file_html = open("accounts/templates/accounts/explanation.html","w",encoding="utf-8")
    file_html.write(data)
    file_html.close()