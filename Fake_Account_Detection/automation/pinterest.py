try:
    import argparse
    from fake_headers import Headers
    import requests
    import json
    import re
    import langid
    from accounts.ml_model import LANGUAGE_DICTIONARY
except ModuleNotFoundError:
    print("Please download dependencies from requirement.txt")
except Exception as ex:
    print(ex)


class Pinterest:
    '''This class scraps pinterest and returns a dict containing all user data'''
    @staticmethod
    def _generate_url(username):
        return "https://pinterest.com/resource/UserResource/get/?source_url=%25{}%2F&data=%7B%22options%22%3A%7B%22field_set_key%22%3A%22profile%22%2C%22username%22%3A%22{}%22%2C%22is_mobile_fork%22%3Atrue%7D%2C%22context%22%3A%7B%7D%7D&_=1640428319046".format(username, username)

    @staticmethod
    def _make_request(url):
        headers = Headers().generate()
        response = requests.get(url, headers=headers)
        return response

    @staticmethod
    def scrap(username):
        try:

            try:
                url = Pinterest._generate_url(username)
                response = Pinterest._make_request(url)
                if response.status_code == 200:
                    response = response.json()
                else:
                    print("Failed to get Data!")
                    exit()
            except Exception as ex:
                print("Error", ex)
                exit()

            json_data = response
            data = json_data['resource_response']['data']

            return json.dumps(data)
        except Exception as ex:
            print(ex)


def pinterest_user_profile(profile_url):
    x = re.findall("^https?:\/\/(?:www\.)?in.pinterest\.com\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?\/?$", profile_url)
    return pinterest_username_details(x[0].strip())

def pinterest_username_details(username):
    profile_details = Pinterest.scrap(username)
    if profile_details is not None:
        profile_details = json.loads(profile_details)
        
    return get_feature_attributes(profile_details)


def get_feature_attributes(details):
    account_details = []
    account_details.append(details["pin_count"] if details["pin_count"] is not None else 0)
    account_details.append(details["follower_count"]if details["follower_count"] is not None else 0)
    account_details.append(details["following_count"] if details["following_count"] is not None else 0)
    account_details.append(details["board_count"] if details["board_count"] is not None else 0)
    account_details.append(details["group_board_count"] if details["group_board_count"] is not None else 0)

    if("partner" is not None):
        if(details["partner"] is not None and "enable_profile_address" in details["partner"]):
            geo_enabled = details["partner"]["enable_profile_address"]
            if(geo_enabled):
                account_details.append(1)
            else:
                account_details.append(0)
        else:
            account_details.append(0)
    else:
        account_details.append(0)

    if(details["image_large_url"] is not None and len(details["image_large_url"])!=0):
        account_details.append(1)
    else:
        account_details.append(0)
    
    description = re.sub(r"[^0-9a-bA-z ]",'',details["seo_description"])
    language = langid.classify(description)
    if len(language[0]) != 0:
        account_details.append(LANGUAGE_DICTIONARY[language[0]])
    else:
         account_details.append(1)
        
    return account_details

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username", help="username to search")

    args = parser.parse_args()
    print(Pinterest.scrap(args.username))

