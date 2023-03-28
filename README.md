# Crypto Trading Signal Assistant with Telegram Bot

This Python project provides a Telegram bot that helps cryptocurrency traders to stay updated on the latest trading signals. The bot analyzes the market using KD and MACD technical indicators and sends real-time notifications to subscribers when a buy or sell signal appears. Additionally, traders can query the bot at any time to check if a particular trading pair has a signal.

## Click the link below to try the bot
[@vincent_crypto_notifier_bot](https://t.me/vincent_crypto_notifier_bot)

## Features

- Provides real-time buy and sell signals using KD and MACD technical indicators
- Sends instant notifications to subscribers via Telegram bot when signals appear
- Allows traders to check for signals of specific trading pairs at any time
- Easy to customize and integrate with your own cryptocurrency trading strategy

## Getting Started

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Installation and Prerequisites

1. Clone this repository to your local machine.
1. Install the required packages with `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`.
1. In the `application_config.example` file, modify extension to `.py`, and replace all parameters enclosed in double curly braces like `{{parameter}}`.
1. In the [app/main/static](app/main/static) and [app/main/static/log_file](app/main/static/log_file) directory, rename the `.example` files to `.txt`. You can add the nofication reveivers in these files. [telegram_developers.txt](app/main/static/telegram_developers.example) file is for development and testing, while the [telegram_subscribers.txt](app/main/static/telegram_subscribers.example) file is for the production environment of subscriber list.

### Usage

1. To start the application, run `python3 main_app.py` after checkout to the directory of this project.

## Contributing

If you find a bug or have a suggestion for a new feature, please create an issue in the [GitHub repository](https://github.com/jerryliu208/Crypto-Trading-Signal-Notifier-with-Python/issues). Pull requests are also welcome!


## Author(s)
- [Vincent Liu](https://github.com/jerryliu208) 🇹🇼

## Last Update Date
- 2023-03-29