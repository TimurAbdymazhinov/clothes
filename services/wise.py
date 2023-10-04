import json
import uuid
from http.client import HTTPException
from pprint import pprint

import requests
from decouple import config


class WiseService:
    def __init__(self):
        self.main_url = config('WISE_URL')
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {config('WISE_TOKEN')}"
        }
        self.profile_id = self._get_profile_id()

    def _get_profile_id(self):
        url = f"{self.main_url}/v1/profiles"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()[0]["id"]
        raise HTTPException(response.status_code, "Payment response is not successful")

    def create_quote(self, amount):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/quotes"
        payload = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "targetAmount": amount,
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["id"]

        raise HTTPException(response.status_code, "Payment response is not successful")

    def create_recipient_account(self, full_name, iban):
        url = f"{self.main_url}/v1/accounts"
        payload = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "details": {
                "legalType": "PRIVATE",
                "iban": iban
            }
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if response.status_code == 200:
            return response.json()["id"]
        raise HTTPException(response.status_code, "Payment response is not successful")

    def create_transfer(self, target_account_id, quote_id):
        customer_transaction_id = str(uuid.uuid4())
        url = f"{self.main_url}/v1/transfers"
        payload = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
        }

        response = requests.post(url, headers=self.headers, data=json.dumps(payload))

        if response.status_code == 200:
            return response.json()["id"]

        raise HTTPException(response.status_code, "Payment response is not successful")

    def fund_transfer(self, transfer_id):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        payload = {
            "type": "BALANCE"
        }
        response = requests.post(url, headers=self.headers, data=json.dumps(payload))
        if not response.status_code == 201:
            raise HTTPException(response.status_code, "Payment response is not successful")

    def cancel_fund(self, transfer_id):
        url = f"{self.main_url}/v1/transfers/{transfer_id}/cancel"
        response = requests.put(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()["id"]
        raise HTTPException(response.status_code, "Payment response is not successful")
