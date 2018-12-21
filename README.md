## Assignment 2

### To run the application
#### JUST USE THE BELOW COMMAND SINCE THIS IS A RESTFUL FLASK APPLICATION AND YOU DONT NEED TO DO EXPORT FLASK_APP


`python app.py`

#### To create a wallet:

```sh
curl -X POST "http://127.0.0.1:5000/wallets?id=9790&balance=783&coin_symbol=Bit%20coin" -H "Content-Type: text/plain"
```

or

```
curl -X "POST" "http://127.0.0.1:5000/wallets?balance=783&coin_symbol=Bit%20coin"

```

or

```sh
curl -X "POST" "http://127.0.0.1:5000/wallets" \
     -H 'Content-Type: application/json; charset=utf-8' \
     -d $'{
  "id": "9786",
  "balance": 66,
  "coin_symbol": "lite coin"
}'
```

#### To get a wallet:

```sh
curl -X GET "http://127.0.0.1:5000/wallets/9786"
```

#### To delete a wallet:

```sh
curl -X DELETE "http://127.0.0.1:5000/wallets/9786"
```

#### To create a transaction:

```sh
curl -X POST "http://127.0.0.1:5000/txns?to_wallet=9790&amount=40&from_wallet=9786"
```

#### To get a transaction(Find the txn_hash from db or note the transaction hash down when creating the transaction):

```sh
curl -X GET "http://127.0.0.1:5000/txns/826e2989857ec28ae54285f75b7e086f71f3ca6"
```
