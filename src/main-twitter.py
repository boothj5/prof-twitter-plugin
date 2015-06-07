import os
import json

from lib.twitter import UserClient
from lib.twitter import TwitterClientError
from lib.twitter import TwitterApiError
from lib.twitter import StreamClient

# app and twitter user authentication
CONSUMER_KEY = 'f9ZVaxUEphYfsuqNmnHFYEO7j'
CONSUMER_SECRET = 'mTofVPgv6NPklp8w5lMoAWTNZaamD63XKaOKf9fNc1zf9Bpbxd'
TOKEN_FILE_NAME = 'twitter_token.txt'

token = ''
access_token = ''
access_token_secret = ''
client = ''

# profanity will register and use
def authorize_app_for_twitter():
    global client
    global token
    global access_token
    global access_token_secret
    global CONSUMER_KEY
    global CONSUMER_SECRET

    try:
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET)
        token = client.get_authorize_token("oob")
    except TwitterClientError:
        print('Oops, this is embarrassing, cannot connect to twitter')
    else:
        _check_for_token()
        stream()


def tweet():

    userTweet = input('Type your tweet here: ')

    try:
        tweetApiResponse = client.api.statuses.update.post(status=str(userTweet))
    except TwitterApiError as error:
        print("Something went wrong in tweeting that")
        print("Please see error details below:")
        print("Status code for twitter api: "+ str(error.status_code) + "\n")
    else:
        print("Your tweet '" + userTweet + "' has flown away in the clouds")

def stream():
    try:
        #userFeed = client.userstream.user.get() #streaming api error, Unable to decode JSON response
        userFeed = client.api.statuses.home_timeline.get()
    except TwitterApiError as error:
        print("Something went wrong in getting your user feed")
        print("Please see error details below:")
        print("Status code for twitter api: "+ str(error.status_code) + "\n")
    else:
        for eachtweet in userFeed.data:
            print(eachtweet['text'])

# used only by this script (authentication of app and authorization of user)
def _check_for_token():
    global access_token
    global access_token_secret
    if os.path.isfile(TOKEN_FILE_NAME):
        _get_token_from_storage()
    else:
        access_token = token['oauth_token']
        access_token_secret = token['oauth_token_secret']
        _print_initial_message()
        _set_final_access_token()

def _get_token_from_storage():
    global access_token
    global access_token_secret
    global client

    try:
        file_object = open(TOKEN_FILE_NAME, 'r')
    except:
        print(TOKEN_FILE_NAME + ' file not found')
    else:
        access_token = file_object.readline().strip()
        access_token_secret = file_object.readline().strip()
        file_object.close()
        client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)

def _print_initial_message():
    global client
    global token

    if client and token:
        print('Birdy Twitter API Version: ' + client.api_version)
        print('Author: ManiacViper')
        print('Please click below to give your blessings to profanity:')
        print(token['auth_url'])

def _set_final_access_token():
    global client
    global token
    global OAUTH_VERIFIER
    global access_token
    global access_token_secret

    if _user_entered_pin_code():
        try:
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)
            token = client.get_access_token(OAUTH_VERIFIER)
        except TwitterApiError as e:
            print("getting final access token error: " + e.error_code)
        else:
            access_token = token['oauth_token']
            access_token_secret = token['oauth_token_secret']
            client = UserClient(CONSUMER_KEY, CONSUMER_SECRET,
                                access_token, access_token_secret)
            _save_token()

def _user_entered_pin_code():
    global OAUTH_VERIFIER
    OAUTH_VERIFIER = input('Enter the pin code here: ')
    return _is_number(OAUTH_VERIFIER)

def _save_token():
    try:
        file_object = open(TOKEN_FILE_NAME, 'w')
    except:
        print('Cannot create a new access token file for twitter')
    else:
        file_object.write(access_token + '\n')
        file_object.write(access_token_secret)
        file_object.close()

def _is_number(numberAsString):
    try:
        float(numberAsString)
        return True
    except ValueError:
        return False

# for development without profanity - temporary
def _quit_application():
    quit_keyword = 'quit'
    user_message = "Enter '" + quit_keyword + "' to quit the program: "
    user_entry = input(user_message).strip()

    if user_entry != quit_keyword:
        _quit_application()

# execute the program
authorize_app_for_twitter()
_quit_application()

