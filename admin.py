from flask import Flask, request
app = Flask(__name__)

import sqlite3
from time import sleep
con = sqlite3.connect("bank.db", check_same_thread=False)
cur = con.cursor()

MAX_AMOUNT_OF_TOKEN = 5000

def f(fetched):
	f1 = fetched[0]
	f2 = f1[0]
	return f2

def find_last_id():
	cur.execute("SELECT id FROM accounts;")
	con.commit()
	rows = cur.fetchall()
	lrow = rows[len(rows)-1]
	return lrow[0]

def new_account(username,password):
	if username != "" and username != " " and username != "root":
		id = find_last_id() + 1
		cur.execute(f'select username from accounts where username = "{username}"')
		h = cur.fetchall()
		try:
			h = h[0]
			h = h[0]
			return 0
		except:
			pass
		cur.execute(f"INSERT INTO accounts VALUES({id},'{username}','{password}',0);")
		con.commit()
		print(f"*\nnew account has been created.\nusername: {username}\npassword: {password}\n*")
		return id
	else:
		return 0

def transaction(sid,rid,spassword,amount):
	#UPDATE accounts SET balance -= amount where id = sid
	try:
		print(f"*\na new transaction!\nsender id: {sid}\nreceiver id: {rid}\namount: {amount}\n*")
		cur.execute(f"SELECT password FROM accounts where id = {sid};")
		realspassword = cur.fetchall()
		realspassword = f(realspassword)
		cur.execute(f"select balance from accounts where id = {sid};")
		bofs = cur.fetchall()
		bofs = f(bofs)
		if spassword == realspassword:
			if amount <= bofs:
				cur.execute(f"SELECT balance FROM accounts where id = {sid}")
				current_balanceofs = cur.fetchall()
				current_balanceofs = f(current_balanceofs)
				cur.execute(f'UPDATE accounts SET balance = {current_balanceofs - int(amount)} where id = {sid};')
				cur.execute(f"SELECT balance FROM accounts where id = {rid}")
				current_balanceofr = cur.fetchall()
				current_balanceofr = f(current_balanceofr)
				cur.execute(f'UPDATE accounts SET balance = {amount+current_balanceofr} where id = {rid};')
				con.commit()
				print("*transaction has been sucsfully.*")
				return 0
			else:
				print("*transaction has been unsuscfully. because sender haves lower amount of token*")
				return 1
		else:
			print("*transaction has been unsuscfully. becuase password is wrong!*")
			return 1
	except:
		return 1

def check_balance(id):
	cur.execute(f"select balance from accounts where id = {id}")
	balance = cur.fetchall()
	balance = f(balance)
	return balance
#security------------------------------------------------------
def find_cheater():
	cur.execute(f"select id FROM accounts where balance > {MAX_AMOUNT_OF_TOKEN};")
	x = cur.fetchall()
	try:
		x = f(x)
		cur.execute(f"DELETE FROM accounts where id = {x};")
		print(f"*\na cheater has been banned.\nid = {x}\n*")
		con.commit()
	except:
		pass

def check_network():
	cur.execute("SELECT balance from accounts")
	rows = cur.fetchall()
	#---
	z = 0
	for row in rows:
		z += row[0]
	#---
	print(f"***The Networth is {z} Tokens***")

def idle():
	while True:
		sleep(30)
		find_cheater()
		check_network()
#----------------------------flask---------------------------------

@app.route('/')
def index():
	return '0'

@app.route('/new_account', methods=['get'])
def na():
	username = request.args['username']
	password = request.args['password']
	idu = new_account(username, password)
	if idu == 0:
		return "failed."
	else:
		return f"Account Created Sucsfully.\nID: {idu}"
@app.route('/transaction', methods=['get'])
def trx():
	senderid = request.args['sender_id']
	receiverid = request.args['receiver_id']
	senderpassword = str(request.args['sender_password'])
	amount = int(request.args['amount'])
	status = transaction(senderid,receiverid,senderpassword,amount)
	if status == 0:
		return "Transaction has been Sucsfull."
	if status == 1:
		return "Transaction has been UnSucsfull."
@app.route('/check_balance', methods=['get'])
def cb():
	id = int(request.args['id'])
	b = check_balance(id)
	return f"{b}"


if __name__ == "__main__":
	app.run(port=443)
