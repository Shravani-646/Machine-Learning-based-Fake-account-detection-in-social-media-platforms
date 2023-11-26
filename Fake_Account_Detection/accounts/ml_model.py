import pickle
import os
from django.conf import settings

FEATURE_SET = ['statuses_count','followers_count','friends_count','favourites_count','listed_count','geo_enabled','user_profile_background_image','language']
def open_model(file_name):
    models_folder = settings.BASE_DIR / 'model' 
    file_path = os.path.join(models_folder, os.path.basename(file_name))
    print(file_path)
    if os.path.exists(file_path):
        model_name = open(file_path, "rb")
        model = pickle.load(model_name)
        return model
    else:
        print('No model with this name, check this and retry')
        model = None
        return model
    
model = open_model('model.pkl')

LANGUAGE_DICTIONARY = {
    'de':0,
    'en':1,
    'es':2,
    'fr':3,
    'gl':4,
    'it':5,
    'nl':6,
    'tr':7
}



def predict(row_df):
    prediction = model.predict(row_df)
    result = []
    for i in prediction:
        if i == 1:
            result.append(f'Detected as Fraudulent Profile')
        else:
            result.append(f'Detected as Genuine Profile')

    return result

def get_values(param_dict):
    result_dictionary = {}
    for i in param_dict:
        if i=="geo_enabled" or i=="user_profile_background_image":
            result_dictionary[i] = 1
        elif i=="csrfmiddlewaretoken":
            pass
        elif i=="language":
            lang_num = LANGUAGE_DICTIONARY[param_dict[i]]
            result_dictionary[i] = lang_num
        else:
            result_dictionary[i] = int(param_dict[i])
    
    if 'geo_enabled' not in param_dict:
        result_dictionary['geo_enabled'] = 0
    if 'user_profile_background_image' not in param_dict:
        result_dictionary['user_profile_background_image'] = 0
    
    parameters = []
    for i in FEATURE_SET:
        if i in result_dictionary:
            parameters.append(result_dictionary[i])
        else:
            print("check request object again")  
    return parameters













# statuses_count = 2500
# followers_count = 1145
# friends_count = 534
# favourites_count = 1000
# listed_count = 2878
# geo_enabled = 1
# profile_use_background_image = 1
# lang_num = 1

# row_df = np.array([[text1,text2,text3,text4,text5]])
#     row_df  = row_df.reshape(1,-1)
#     print(row_df)

