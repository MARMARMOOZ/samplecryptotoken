import requests
from os import system
url = "http://127.0.0.1:5000/"

def mainmenu():
	system("clear")
	print('''----WeToken-Menu----
	1) Create an Account
	2) Send an amount
	3) Your Balance
	''')
	return input("-->")

def new_account(username,password):
	r = requests.get(f"{url}new_account?username={username}&password={password}")
	return r.text
def send(sender_ID, receiver_ID, sender_password, amount):
	r = requests.get(f"{url}transaction?sender_id={sender_ID}&receiver_id={receiver_ID}&sender_password={sender_password}&amount={amount}")
	return r.text
def check_balance(id):
	r = requests.get(f"{url}check_balance?id={id}")
	return r.text

def main():
	while True:
		service = mainmenu()
		if service == '1':
			username = input("username-->")
			password = input("password-->")
			print(new_account(username,password))
			input('Enter to countinue...')
		elif service == '2':
			sender_ID = input("SenderID-->")
			receiver_ID = input("ReceiverID-->")
			password = input("SenderPassword-->")
			amount = input("Amount-->")
			print(send(sender_ID,receiver_ID,password,amount))
			input('Enter to countinue...')
		elif service == '3':
			id = input("ID-->")
			print(str(check_balance(id)))
			input('Enter to countinue...')

if __name__ == "__main__":
	main()
