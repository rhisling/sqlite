import uuid
import sqlite3
import datetime
import random
import hashlib
from flask_restful import Resource, Api
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort


class Transaction(Resource):
    txn_args = {
        'from_wallet': fields.Str(required=True),
        'to_wallet': fields.Str(required=True),
        'amount': fields.Int(required=True)
    }

    def __init__(self, from_wallet="1", to_wallet="2", amount=34):
        status = ["pending", "complete", "In-progress"]
        self.from_wallet = from_wallet
        self.to_wallet = to_wallet
        self.amount = amount
        self.time_stamp = str(datetime.datetime.now())
        self.txn_hash = hashlib.sha1(
            from_wallet.encode() + to_wallet.encode() + str(self.time_stamp).encode()).hexdigest()
        self.status = status[random.randint(0, 2)]

    @staticmethod
    def create_transaction(from_wallet, to_wallet, amount):
        try:
            connection = sqlite3.connect("crypto.db")
            cursor = connection.cursor()

            select_query = "SELECT * from wallet where id = ?"
            result = cursor.execute(select_query, (from_wallet,))
            from_wallet_row = result.fetchone()

            select_query = "SELECT * from wallet where id = ?"
            result = cursor.execute(select_query, (to_wallet,))
            to_wallet_row = result.fetchone()

            update_query = "Update wallet set balance = ? WHERE id = ? "

            if from_wallet_row and to_wallet_row:
                wallet_amount = from_wallet_row[1]
                if wallet_amount > amount:
                    transaction = Transaction(from_wallet, to_wallet, amount)
                    new_balance = wallet_amount - amount
                    transaction_tuple = (
                        transaction.from_wallet, transaction.to_wallet, transaction.amount, transaction.time_stamp,
                        transaction.txn_hash, transaction.status)
                    insert_query = "INSERT INTO txns VALUES (?,?,?,?,?,?)"
                    cursor.execute(update_query, (new_balance, from_wallet))
                    cursor.execute(insert_query, transaction_tuple)
                    connection.commit()
                    connection.close()
                    return [transaction.from_wallet, transaction.to_wallet, transaction.amount, transaction.time_stamp,
                            transaction.txn_hash]
                else:
                    connection.close()
                    return ["Amount not sufficient"]
            else:
                connection.close()
                return ["Wallet doesn't exist"]
        except sqlite3.IntegrityError:
            connection.close()
            return None

    def get(self):
        pass

    @use_kwargs(txn_args)
    def post(self, from_wallet, to_wallet, amount):
        try:
            result = Transaction.create_transaction(from_wallet,
                                                    to_wallet, amount)
            if len(result) > 1:
                from_wallet, to_wallet, amount, time_stamp, txn_hash = result
                return {'from_wallet': from_wallet, 'to_wallet': to_wallet, 'amount': amount, 'time_stamp': time_stamp,
                        'txn_hash': txn_hash}
            else:
                print("result" + result[0])
                if "Amount" in result[0]:
                    return {"message": "Insufficient balance"}, 400
                else:
                    return {"message": "Wallet doesn't exist"}, 400
        except TypeError as err:
            print(err)
            return {"message": "Transaction failure"}, 400
        except ValueError:
            {"message": "wallet not available"}, 400


class TransactionById(Resource):
    def get(self, id):
        connection = sqlite3.connect("crypto.db")
        cursor = connection.cursor()
        select_query = "SELECT * from txns where txn_hash = ?"
        result = cursor.execute(select_query, (id,))
        row = result.fetchone()
        connection.close()
        if row:
            return {'from_wallet': row[0], 'to_wallet': row[1], 'amount': row[2], 'time_stamp': row[3],
                    'txn_hash': row[4], 'status': row[5]}
        return {'message': 'Transaction not available'}, 400
