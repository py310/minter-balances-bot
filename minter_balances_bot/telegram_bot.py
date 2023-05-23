import configparser
from telebot import TeleBot, types
from api_requests import MinterApi, ExchangeRates

# Define constants
CONFIG_FILE = 'config.ini'

# Read the configuration file
config = configparser.ConfigParser()
config.read(CONFIG_FILE)

# Access values from the configuration file
bot_token = config['credentials']['bot_token']
wallets = config['credentials']['wallets'].split(',')

# Create telegram bot
bot = TeleBot(config.bot_token)
markup = types.ReplyKeyboardMarkup()
markup.row('/btc', '/bip')

# Create instances of MinterApi and ExchangeRates
minter = MinterApi()
rates = ExchangeRates()

# Action when starting
@bot.message_handler(commands=["start"])
def answer_start_message(message):
    bot.send_message(message.chat.id, 'Choose your button', reply_markup=markup)

# Action when receiving command "/btc"
@bot.message_handler(commands=["btc"])
def get_btc_price(message):
    try:
        price = rates.get_binance_rate('BTCUSDT')
        bot.send_message(message.chat.id, price, reply_markup=markup)
    except Exception as e:
        bot.send_message(message.chat.id, f'Some error occurred: {str(e)}', reply_markup=markup)

# Action when receiving command "/bip"
@bot.message_handler(commands=["bip"])
def get_balances(message):
    try:
        # Fetch BIP price
        price = rates.get_bithumb_rate('BIP-USDT')

        # Initialize message text
        msg_text = f'Current BIP price: *{price}*\n=============================\n'

        # Calculate total balance and build message text
        total_balance = 0
        for i, wallet in enumerate(config.wallets):
            wallet_delegations = minter.get_delegations(wallet)
            wallet_balance     = minter.get_current_balance(wallet)
            wallet_unbonds     = minter.get_unbonds(wallet)
            wallet_total       = wallet_delegations + wallet_balance + wallet_unbonds
            total_balance     += wallet_total

            # Add wallet details to message text
            msg_text += f'*Wallet {i+1}*\nDelegations: {wallet_delegations}\nBalance: {wallet_balance}\nUnbonds: {wallet_unbonds}\n*Total:* {wallet_total}\n=============================\n'
        
        # Add total balance to message text
        msg_text += f'Total BIP: {round(total_balance,2)}\nTotal USD: {round(total_balance*price, 2)}'
        
        # Send the message
        bot.send_message(message.chat.id, msg_text, reply_markup=markup, parse_mode='Markdown')
    except Exception as e:
        bot.send_message(message.chat.id, f'Some error occurred: {str(e)}', reply_markup=markup)

# Start the Telegram bot and keep it running
if __name__ == '__main__':
     bot.infinity_polling()