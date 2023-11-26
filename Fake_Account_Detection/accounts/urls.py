from django.urls import path
from . import views

urlpatterns = [
    path('',views.home_page,name="home-page"),
    path('notebook/',views.get_jupyter_notebook,name="notebook"),
    path('explanation/',views.get_model_predicted_explanation,name="explanation"),
    path('signup/',views.user_registration,name="signup"),
    path('login/',views.user_login,name="login"),
    path('logout/',views.logout_user,name="logout"),
    path('prediction_form/',views.prediction_form,name="prediction_form"),
    path('clone_prediction_form/',views.clone_prediction_form,name="clone_prediction_form"),
    #automation url
    path('automate/',views.index,name="username_input_form"),
]
