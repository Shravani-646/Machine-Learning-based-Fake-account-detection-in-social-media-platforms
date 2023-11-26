from .twitter import twitter_user_profile
from .pinterest import pinterest_user_profile
from .quora import quora_user_profile
def get_profile_data(profile_url):
    profile_details = []
    if "twitter.com" in profile_url:
        profile_details.append(twitter_user_profile(profile_url))
    elif "pinterest.com" in profile_url:
        profile_details.append(pinterest_user_profile(profile_url))                
    elif "quora.com" in profile_url:
        # print(quora_user_profile(profile_url))
        profile_details.append(quora_user_profile(profile_url))        
    return profile_details