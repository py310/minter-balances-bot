"""
Minter API Documentation: https://app.swaggerhub.com/apis-docs/GrKamil/minter-explorer_api/2.3.0
"""
import requests

class MinterApi:
    MINTER_API_ENDPOINT = "https://explorer-api.minter.network/api/v2"

    @staticmethod
    def get_json_response(url: str) -> dict:
        response = requests.get(url)
        return response.json()

    # Find out the number of BIP coins in the delegations by wallet
    def get_delegations(self, wallet: str) -> float:
        url = f"{self.MINTER_API_ENDPOINT}/addresses/{wallet}/delegations"
        json_response = self.get_json_response(url)
        bip_value = json_response["meta"]["additional"].get("total_delegated_bip_value", 0)
        return round(float(bip_value), 2)

    # Find out the number of BIP coins in unbonds by wallet
    def get_unbonds(self, wallet: str) -> float:
        url = f"{self.MINTER_API_ENDPOINT}/addresses/{wallet}/events/unbonds"
        json_response = self.get_json_response(url)
        unbonds_data = json_response.get("data", [])
        unbonds = sum(float(d.get("value", 0)) for d in unbonds_data)
        return round(unbonds, 2)

    # Find out the number of BIP coins in wallet
    def get_current_balance(self, wallet: str) -> float:
        url = f"{self.MINTER_API_ENDPOINT}/addresses/{wallet}"
        json_response = self.get_json_response(url)
        balances_data = json_response["data"].get("balances", [])
        balance = sum(float(d.get("bip_amount", 0)) for d in balances_data)
        return round(balance, 2)        

class ExchangeRates:
    BINANCE_ENDPOINT = "https://api2.binance.com/api/v3"
    BITHUMB_ENDPOINT = "https://global-openapi.bithumb.pro/openapi/v1"

    @staticmethod
    def get_json_response(url: str, params: dict = None) -> dict:
        response = requests.get(url, params=params)
        return response.json()

    # Find out the BTC-USDT exchange rate on Binance
    def get_binance_rate(self, symbol: str) -> float:
        url = f"{self.BINANCE_ENDPOINT}/ticker/price"
        params = {"symbol":symbol}
        json_response = self.get_json_response(url, params=params)
        price = json_response.get("price", 0)
        return float(price)

    # Find out the BIP-USDT exchange rate on Bithumb
    def get_bithumb_rate(self, symbol: str) -> float:
        url = f"{self.BITHUMB_ENDPOINT}/spot/ticker"
        params = {"symbol":symbol}
        json_response = self.get_json_response(url, params=params)
        data = json_response.get("data", [])
        price = data[0].get("c", 0) if data else 0
        return float(price)