try:
    import argparse
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options as ChromeOptions
    from selenium.webdriver.firefox.options import Options as FirefoxOptions
    from fake_headers import Headers
    from selenium.webdriver.support.ui import WebDriverWait
    from selenium.webdriver.support import expected_conditions as EC
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager
    import re
    import json
    import langid
    from accounts.ml_model import LANGUAGE_DICTIONARY
except ModuleNotFoundError:
    print("Please download dependencies from requirement.txt")

class Quora:
    @staticmethod
    def init_driver(browser_name:str):
        def set_properties(browser_option):
            ua = Headers().generate()      #fake user agent
            browser_option.add_argument('--headless')
            browser_option.add_argument('--disable-extensions')
            browser_option.add_argument('--incognito')
            browser_option.add_argument('--disable-gpu')
            browser_option.add_argument('--log-level=3')
            browser_option.add_argument(f'user-agent={ua}')
            browser_option.add_argument('--disable-notifications')
            browser_option.add_argument('--disable-popup-blocking')
            return browser_option
        try:
            browser_name = browser_name.strip().title()


            #automating and opening URL in headless browser
            if browser_name.lower() == "chrome":
                browser_option = ChromeOptions()
                browser_option = set_properties(browser_option)
                driver = webdriver.Chrome(ChromeDriverManager().install(),options=browser_option) #chromedriver's path in first argument
            elif browser_name.lower() == "firefox":
                browser_option = FirefoxOptions()
                browser_option = set_properties(browser_option)
                driver = webdriver.Firefox(executable_path=GeckoDriverManager().install(),options=browser_option)
            else:
                driver = "Browser Not Supported!"
            return driver
        except Exception as ex:
            print(ex)
    @staticmethod
    def scrap(username,browser_name):
        try:
            URL = 'https://quora.com/profile/{}'.format(username)
            try:

                driver = Quora.init_driver(browser_name)
                driver.get(URL)
            except AttributeError:
                print("Driver is not set")
                exit()



            wait = WebDriverWait(driver, 10)
            element = wait.until(EC.title_contains('Quora'))

            try:
              name = driver.find_element_by_css_selector("div.q-text.qu-bold")
            except Exception as ex:
              print(ex)
            name = name.text if type(name) is not str else ""

            try:
                profession = driver.find_element_by_css_selector(".q-text.qu-wordBreak--break-word")
            except:
                profession = ""
            profession = profession.text.strip() if type(profession) is not str else ""
            try:
                profile_image = driver.find_element_by_css_selector("img.q-image.qu-display--block")
            except:
                profile_image = ""
            try:
                driver.find_element_by_css_selector("div.qt_read_more").click()
            except Exception as ex:
                print(ex)
                pass

            try:
                details = driver.find_elements_by_css_selector('div.q-box.qu-overflowX--hidden.qu-whiteSpace--nowrap')
                details_text = details[0].text.split('\n')
                answers_count = [text.split(' ')[0] for text in details_text if "Answer" in text]
                answers_count = answers_count[0] if len(answers_count) > 0 else ""
                questions = [text.split(' ')[0] for text in details_text if "Question" in text ]
                questions = questions[0] if len(questions) > 0 else ""
                shares = [text.split(' ')[0]
                          for text in details_text if "share" in text ]
                shares = shares[0] if len(shares) > 0 else ""
                posts = [text.split(' ')[0] for text in details_text if "Posts" in text ]
                posts = posts[0] if len(posts) > 0 else ""
                follwing_follower_element = driver.find_element_by_css_selector(
                    '.q-flex.qu-flexDirection--column.qu-mt--tiny')
                elements = follwing_follower_element.find_elements_by_css_selector(
                    '.CssComponent-sc-1oskqb9-0.AbstractSeparatedItems___StyledCssComponent-sc-46kfvf-0')
                followers = [element.text.split(' ')[0] for element in elements if "follower" in element.text ]
                followers = followers[0] if len(followers) > 0 else ""

                followings = [element.text.split(' ')[0] for element in elements if "following" in element.text ]
                followings = followings[0] if len(followings) > 0 else ""
            except Exception as ex:
                print(ex)
                questions = shares = posts = followers = answers_count = ''

            bio_text = ""
            try:
                bio = driver.find_elements_by_css_selector("p.q-text")
                for p_tag in bio:
                  bio_text += p_tag.text
            except:
                bio = ""
            bio = bio_text if type(bio) is not str else ""
            profile_data = {
                'name'  :name,
                'profession' : profession,
                'profile_image' : profile_image.get_attribute("src"),
                'bio' : bio,
                'answers_count' : answers_count,
                'questions_count' : questions,
                'shares' : shares,
                'posts' : posts,
                'followers' : followers,
                'following' : followings,
            }
            driver.close()
            driver.quit()
            return json.dumps(profile_data)
        except Exception as ex:
            driver.close()
            driver.quit()
            print(ex)


def features_formate(features):
    def convert_str_to_number(x):
        total_stars = 0
        num_map = {'K':1000, 'M':1000000, 'B':1000000000}
        if x.isdigit():
            total_stars = int(x)
        else:
            if len(x) > 1:
                total_stars = float(x[:-1]) * num_map.get(x[-1].upper(), 1)
        return int(total_stars)
    for i in range(len(features)):
        features[i] = features[i].replace(",","")
        features[i] = features[i].replace(" ","")
        features[i] = convert_str_to_number(features[i]) 
    return features

def get_feature_attributes(details):
    account_details = []
    a = details["posts"] # statuses_count
    b = details["followers"] #followers
    c = details["following"] #following
    d = details["answers_count"] #fav count
    e = details["questions_count"]# listed count
    features = [a,b,c,d,e]
    account_details = features_formate(features)
    # there is no geo enabled feature is false
    account_details.append(0)
    #profile background
    if(details["profile_image"] is not None and len(details["profile_image"])!=0):
        account_details.append(1)
    else:
        account_details.append(0)
    #language
    description = re.sub(r"[^0-9a-bA-z ]",'',details["bio"])
    language = langid.classify(description)
    if len(language[0]) != 0:
        account_details.append(LANGUAGE_DICTIONARY[language[0]])
    else:
         account_details.append(1)
        
    return account_details

def quora_user_profile(profile_url):
    x = re.findall("^https?:\/\/(?:www\.)?quora\.com\/profile\/(?:#!\/)?@?([^/?#]*)(?:[?#].*)?\/?$", profile_url)
    return quora_username_details(x[0])


def quora_username_details(username):
    profile_details = Quora.scrap(username,"chrome")
    if profile_details is not None:
        profile_details = json.loads(profile_details)
    return get_feature_attributes(profile_details)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("username",help="username to search")
    parser.add_argument("--browser",help="What browser your PC have?")
    args = parser.parse_args()

    browser_name = args.browser if args.browser is not None else "chrome"
    print(Quora.scrap(args.username,browser_name))

