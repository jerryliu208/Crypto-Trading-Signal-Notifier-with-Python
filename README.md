# Crypto Trading Signal Notifier with Python

This is a Python project that automatically uses KD and MACD technical indicators to determine whether there are buy or sell signals for cryptocurrencies. When a buy or sell signal appears, the program will automatically send an email to all subscribers notifying them that a signal has appeared.

## Features

- Uses KD and MACD technical indicators to determine buy or sell signals
- Automatically sends email notifications to subscribers when signals appear
- Easy to customize and integrate with your own cryptocurrency trading strategy

## Getting Started

### Prerequisites

- Python 3.9.7 or higher
- pip package manager
- Gmail account

### Installation and Prerequisites

1. Clone this repository to your local machine.
2. Install the required packages with `pip install -r requirements.txt` or `python3 -m pip install -r requirements.txt`.
3. Create a Gmail account specifically for the email sending to use.
4. In the `application_config.example` file, modify extension to `.py`, and replace all parameters enclosed in double curly braces like `{{parameter}}`.
5. In the [app/main/static](app/main/static) directory, rename the `.example` files to `.txt`. You can add the email reveivers in these files. `developers` file is for development and testing, while the `subscribers` file is for the production environment of subscriber list.

### Usage

1. To start the application, run `python3 main_app.py` after checkout to the directory of this project.
2. The bot will check for buy or sell signals every time it starts and will send email notifications to all subscribers if a signal appears.

## Contributing

If you find a bug or have a suggestion for a new feature, please create an issue in the [GitHub repository](https://github.com/your-username/crypto-trading-bot). Pull requests are also welcome!


## Author(s)
- [Vincent Liu](https://github.com/jerryliu208)🇹🇼

## Last Update Date
- 2023-03-26