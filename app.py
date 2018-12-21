from flask import Flask
from flask_restful import Resource, Api
import uuid
import random
from transactions import Transaction, TransactionById
import sqlite3
from wallet import Wallet, WalletById

app = Flask(__name__)
api = Api(app)


def init_wallet():
    connection = sqlite3.connect('crypto.db')
    cursor = connection.cursor()
    drop_table = "Drop table IF EXISTS wallet"
    create_table = "CREATE TABLE IF NOT EXISTS wallet (id text,balance int, coin_symbol text, PRIMARY KEY(id))"
    cursor.execute(drop_table)
    cursor.execute(create_table)
    connection.commit()
    connection.close()


def init_transaction():
    connection = sqlite3.connect('crypto.db')
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON;")
    drop_table = "Drop table IF EXISTS txns"
    create_table = "CREATE TABLE IF NOT EXISTS txns (from_wallet text,to_wallet text,amount INT, time_stamp text, txn_hash text, status text, FOREIGN KEY(from_wallet) REFERENCES wallet(id), FOREIGN KEY(to_wallet) REFERENCES wallet(id))"
    cursor.execute(drop_table)
    cursor.execute(create_table)
    connection.commit()
    connection.close()


api.add_resource(Wallet, '/wallets')
api.add_resource(WalletById, '/wallets/<string:id>')
api.add_resource(Transaction, '/txns')
api.add_resource(TransactionById, '/txns/<string:id>')

if __name__ == '__main__':
    init_wallet()
    init_transaction()
    app.run(debug=True)
