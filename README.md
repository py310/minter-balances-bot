# Telegram Bot for Minter

This is a Telegram bot that provides information about Minter cryptocurrency. It retrieves data from the Minter API and displays it in a Telegram chat.

## Features

- Get the current exchange rate of BTC-USDT on Binance.
- Get the current exchange rate of BIP-USDT on Bithumb.
- Calculate the total balance of BIP coins in multiple wallets, including delegations and unbonds.
- Display the total BIP balance in USD.

## Usage

- Clone the repository:
  ```shell
  git clone https://github.com/py310/telegram-minter-bot.git

- Install the required Python libraries:
  ```shell
  pip install -r requirements.txt

- Create a config.ini file and fill in the required credentials. Example:
  ```shell
  [credentials]
  bot_token = YOUR_TELEGRAM_BOT_TOKEN
  wallets = WALLET_ADDRESS_1, WALLET_ADDRESS_2, WALLET_ADDRESS_3

- Run the main script:
  ```shell
  python telegram_bot.py

## Documentation
Minter API Documentation: https://app.swaggerhub.com/apis-docs/GrKamil/minter-explorer_api/2.3.0

##  License
This project is licensed under the MIT License.
