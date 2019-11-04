import requests


def get_auth_url():
    weibo_auth_url = "https://api.weibo.com/oauth2/authorize"
    redirect_url = "http://192.168.1.5:8000/weibo/"
    auth_url = weibo_auth_url + "?client_id={client_id}&redirect_url={redirect_url}".format(client_id="2326635018",
                                                                                            redirect_url=redirect_url)
    return auth_url


def get_access_token(code):
    weibo_access_token_url = "https://api.weibo.com/oauth2/access_token"
    redirect_url = "http://192.168.1.5:8000/weibo/"

    re_url = requests.post(weibo_access_token_url, data={
        "client_id": "2326635018",
        "client_secret": "eb310df011e1830e807e492b5ba9deb9",
        "code": code,
        "redirect_url": redirect_url,
    })


