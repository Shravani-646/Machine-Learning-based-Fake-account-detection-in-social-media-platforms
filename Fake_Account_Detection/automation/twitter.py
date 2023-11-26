try:
    import requests
    import langid
    import argparse
    from fake_headers import Headers
    import json
    import re
    from accounts.ml_model import LANGUAGE_DICTIONARY
except ModuleNotFoundError:
    print("Please download dependencies from requirement.txt")
except Exception as ex:
    print(ex)

AUTHORIZATION_KEY = 'Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA'


class Twitter:

    @staticmethod
    def find_x_guest_token():
        try:
            headers = {
                'authorization': AUTHORIZATION_KEY,
            }
            response = requests.post(
                'https://api.twitter.com/1.1/guest/activate.json', headers=headers)
            return response.json()['guest_token']
        except Exception as ex:
            print("Error at find_x_guest_token: {}".format(ex))

    @staticmethod
    def make_http_request(URL, headers):
        try:
            response = requests.get(URL, headers=headers)
            if response and response.status_code == 200:
                return response.json()
        except Exception as ex:
            print("Error at make_http_request: {}".format(ex))

    @staticmethod
    def build_headers(x_guest_token, authorization_key):
        headers = {
            'authority': 'twitter.com',
            'accept': '*/*',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': authorization_key,
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': Headers().generate()['User-Agent'],
            'x-guest-token': x_guest_token,
            'x-twitter-active-user': 'yes',
            'x-twitter-client-language': 'en',
        }
        return headers

    @staticmethod
    def scrap(username):
        try:
            # generating URL according to the username
            guest_token = Twitter.find_x_guest_token()
            headers = Twitter.build_headers(guest_token, AUTHORIZATION_KEY)
            response = Twitter.make_http_request(
                "https://api.twitter.com/1.1/users/show.json?screen_name={}".format(username),
                headers=headers)
            if response:
              return json.dumps(response)
            else:
              print("Failed to make Request!")
        except Exception as ex:
            print(ex)

def twitter_user_profile(profile_url):
    x = re.findall("^https?:\/\/(?:www\.)?twitter\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?$", profile_url)
    return twitter_username_arg(x[0])

def twitter_username_arg(username):
    profile_details = Twitter.scrap(username)
    if profile_details is not None:
        profile_details = json.loads(profile_details)
        # print(profile_details)
    return get_feature_attributes(profile_details)

def get_feature_attributes(details):
    account_details = []
    account_details.append(details["statuses_count"] if details["statuses_count"] is not None else 0)
    account_details.append(details["followers_count"]if details["followers_count"] is not None else 0)
    account_details.append(details["friends_count"] if details["friends_count"] is not None else 0)
    account_details.append(details["favourites_count"] if details["favourites_count"] is not None else 0)
    account_details.append(details["listed_count"] if details["listed_count"] is not None else 0)
    if details["geo_enabled"]:
        account_details.append(1)
    else:
        account_details.append(0)
    
    if(details["profile_background_image_url"] is not None and len(details["profile_background_image_url"])!=0):
        account_details.append(1)
    else:
        account_details.append(0)
    description = re.sub(r"[^0-9a-bA-z ]",'',details["description"])
    language = langid.classify(description)
    if len(language[0]) != 0:
        if(language[0] in LANGUAGE_DICTIONARY):
            account_details.append(LANGUAGE_DICTIONARY[language[0]])
        else:
            account_details.append(1)
    else:
         account_details.append(1)
    return account_details

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username to search")

    args = parser.parse_args()
    print(Twitter.scrap(args.username))

