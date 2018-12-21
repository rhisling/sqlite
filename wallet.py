import uuid
import sqlite3
import random
from flask_restful import Resource, Api
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort


class Wallet(Resource):
    wallet_args = {
        'id': fields.Str(required=False),
        'balance': fields.Int(required=True),
        'coin_symbol': fields.Str(required=True)
    }

    def __init__(self, id="123456", balance=999, coin_symbol="xyz"):
        self.id = id
        self.balance = balance
        self.coin_symbol = coin_symbol

    @staticmethod
    def create_wallet(id, balance, coin_symbol):
        try:
            connection = sqlite3.connect("crypto.db")
            cursor = connection.cursor()
            wallet = Wallet(id, balance, coin_symbol)
            wallet_tuple = (wallet.id, wallet.balance, wallet.coin_symbol)
            insert_query = "INSERT INTO wallet VALUES (?,?,?)"
            cursor.execute(insert_query, wallet_tuple)
            connection.commit()
            connection.close()
            return wallet_tuple
        except sqlite3.IntegrityError:
            return None

    def get(self):
        pass

    @use_args(wallet_args)
    def post(self, wallet_args):
        try:
            id = wallet_args['id'] if 'id' in wallet_args else str(
                uuid.uuid4())
            balance = wallet_args['balance']
            coin_symbol = wallet_args['coin_symbol']
            id, balance, coin_symbol = Wallet.create_wallet(
                id, balance, coin_symbol)
            return {'id': id, 'balance': balance, 'coin_symbol': coin_symbol}
        except TypeError:
            return {"message": "ID already exits"}, 400


class WalletById(Resource):
    def get(self, id):
        connection = sqlite3.connect("crypto.db")
        cursor = connection.cursor()
        select_query = "SELECT * from wallet where id = ?"
        result = cursor.execute(select_query, (id,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'id': row[0], 'balance': row[1], 'coin_symbol': row[2]}
        return {'message': 'Wallet not available'}, 400

    def delete(self, id):
        connection = sqlite3.connect("crypto.db")
        cursor = connection.cursor()
        select_query = "DELETE from wallet where id = ?"
        cursor.execute(select_query, (id,))
        connection.commit()
        connection.close()
        return {'message': 'Deleted Successfully'}, 200
