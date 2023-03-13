import requests
from colorama import Fore
import json

#Made by Yokozuna | Zuna

class Log:
    log_file = open("log.txt", "w")  # open log file in write mode

    @classmethod
    def info(cls, message):
        print(message)
        cls.log_file.write(f"{message}\n")  # write message to log file

    @classmethod
    def close(cls):
        cls.log_file.close()  # close log file

def check_token(token):
    headers = {
        "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
        "Authorization": f"OAuth {token}"
    }

    json = [{"operationName": "BitsCard_Bits", "variables": {}, "extensions": {"persistedQuery": {"version": 1,
                                                                                                  "sha256Hash": "fe1052e19ce99f10b5bd9ab63c5de15405ce87a1644527498f0fc1aadeff89f2"}}},
            {"operationName": "BitsCard_MainCard",
             "variables": {"name": "679087745", "withCheerBombEventEnabled": False}, "extensions": {
                "persistedQuery": {"version": 1,
                                   "sha256Hash": "88cb043070400a165104f9ce491f02f26c0b571a23b1abc03ef54025f6437848"}}}]

    response = requests.post("https://gql.twitch.tv/gql", headers=headers, json=json)

    if response.status_code == 200:
        return True
    else:
        return False

class TokenChecker:
    def __init__(self, tokens_file_path):
        with open(tokens_file_path, "r") as f:
            self.tokens = [line.strip() for line in f]
        self.valid = 0
        self.invalid = 0

    def check(self):
        valid_tokens = []
        invalid_tokens = []

        for token in self.tokens:
            if check_token(token):
                valid_tokens.append(token)
            else:
                invalid_tokens.append(token)

        for token in invalid_tokens:
            Log.info(f"Invalid token {token}")
            self.invalid += 1

        for token in valid_tokens:
            headers = {
                "Client-ID": "kimne78kx3ncx6brgo4mv6wki5h1ko",
                "Authorization": f"OAuth {token}"
            }

            json = [{"operationName": "BitsCard_Bits", "variables": {}, "extensions": {"persistedQuery": {"version": 1,
                                                                                                          "sha256Hash": "fe1052e19ce99f10b5bd9ab63c5de15405ce87a1644527498f0fc1aadeff89f2"}}},
                    {"operationName": "BitsCard_MainCard",
                     "variables": {"name": "679087745", "withCheerBombEventEnabled": False}, "extensions": {
                        "persistedQuery": {"version": 1,
                                           "sha256Hash": "88cb043070400a165104f9ce491f02f26c0b571a23b1abc03ef54025f6437848"}}}]

            response = requests.post("https://gql.twitch.tv/gql", headers=headers, json=json)

            if response.status_code == 200:
                data = response.json()[0]["data"]["currentUser"]
                username = data["login"]
                Log.info(f"{Fore.GREEN}[ + ] Validated {token} | {username}")
                self.valid += 1
            else:
                Log.info(f"{Fore.RED}Error with token {token}: {response.status_code} - {response.text}")
                self.invalid += 1

        Log.close()  # close log file at the end

tokens_file_path = "tokens.txt"
checker = TokenChecker(tokens_file_path)
checker.check()
