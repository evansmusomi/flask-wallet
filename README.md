
[![Build Status](https://travis-ci.org/evansmusomi/flask-wallet.svg?branch=master)](https://travis-ci.org/evansmusomi/flask-wallet)
[![Coverage Status](https://coveralls.io/repos/github/evansmusomi/flask-wallet/badge.svg?branch=develop)](https://coveralls.io/github/evansmusomi/flask-wallet?branch=develop)
[![Code Climate](https://codeclimate.com/github/evansmusomi/flask-wallet/badges/gpa.svg)](https://codeclimate.com/github/evansmusomi/flask-wallet)
# Flask Wallet

Spend or save? What should you do with the money you have left? The Flask Wallet personal finance app will help you make such decisions.


## .env Sample

SECRET_KEY = "SECRET"

## Setting Up

1. Clone this repo
2. Setup a virtual environment on your dev environment
3. Install requirements using pip
4. Setup your .env file
5. Navigate to app on Terminal
6. Start server using *python run.py*

## Testing

Run the `pytest` command in your terminal to see passing and failing tests.

For an indepth report, run:

`py.test --cov-report term-missing --cov app -v`

## Features

1. Create account
2. Log in
3. Add expense
4. Update expense
5. Delete expense
6. View profile
7. Top up wallet

Product Roadmap: [Pivotal Tracker Board](https://www.pivotaltracker.com/n/projects/2081915)