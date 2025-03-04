# Test Cases (TZ - Technical Requirements)
# User Creation

# Create a user with valid details.
# Attempt to create a user with an invalid email (should raise ValueError).
# Bank Account Creation

# Create a bank account with a valid balance.
# Ensure negative balances are not allowed.
# Deposit & Withdraw Operations

# Deposit money and check balance updates correctly.
# Withdraw money ensuring insufficient funds raise an error.
# Transaction History

# Verify deposits and withdrawals are recorded.
# Account Linking

# Ensure a user can have multiple bank accounts.
# Ensure accounts are stored and retrieved properly.
# Money Transfer

# Test money transfer between accounts.
# Ensure balance updates correctly after transfer.


from pydantic import BaseModel
from typing import Optional
import uuid
import re


class User(BaseModel):
    id: Optional[str] = str(uuid.uuid4())
    name: Optional[str] = None
    accounts: Optional[list] = []
    __email: Optional[str] = None


    @property
    def email(self):
        return self.__email
    
    @email.setter
    def email(self, new_email):
        email_regex = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        try:
            if email_regex.match(new_email):
                self.__email = new_email
            else:
                raise ValueError("Email is not valid")
        except ValueError as e:
            print(e)

    def create_account(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Amount can't be negativ or 0")
            bank_account = BankAccount(user_id=self.id)
            bank_account.deposit(amount)
            self.accounts.append(bank_account)
            return bank_account
        except ValueError as e:
            print(e)



# ? Create a bank account with a valid balance.
# ? Ensure negative balances are not allowed.
# ? Deposit & Withdraw Operations

class BankAccount(BaseModel):
    id:Optional[str] = str(uuid.uuid4())
    user_id:Optional[str] = None
    __balance:int = 0
    _transactions:Optional[list] = []


    @property
    def balance(self):
        return self.__balance

    def get_transactions(self):
        return self._transactions

    def deposit(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Balance amount can't be negative")
            self.__balance += amount
        except ValueError as e:
            print(e)

        transaction_dict = {
            'Type': 'Deposit', 
            'User': self.user_id, 
            'Deposit Amount' : amount, 
            'Current Balance' : self.balance
        }
        self._transactions.append(transaction_dict)
    
    def withdraw(self, amount):
        try:
            if amount <= 0:
                raise ValueError("Balance amount can't be negative")
            elif amount > self.balance:
                raise ValueError("Not enough balance to withdraw in the account")
            self.__balance -= amount
        except ValueError as e:
            print(e)

        transaction_dict = {
            'Type': 'Withdraw', 
            'User': self.user_id, 
            'Withdraw Amount' : amount, 
            'Current Balance' : self.balance
        }
        self._transactions.append(transaction_dict)
    
    def transfer(self, receiver_account, amount):
        self.withdraw(amount)
        receiver_account.deposit(amount)
        transfer_dict = {
            'Type': 'Transfer', 
            'From': self.user_id,
            'Deposit Amount' : amount, 
            'Current Balance' : receiver_account.balance
        }
        receiver_account._transactions.append(transfer_dict)

user1 = User(name = 'Zilola')
user2 = User(name = 'Iroda')
user1.email = 'ic@gmail.com'
bank_account = user1.create_account(100)
bank_account_2 = user2.create_account(200)
print(bank_account) 
bank_account.deposit(200)
print(bank_account.balance)
bank_account.withdraw(200)
print(bank_account.balance)
bank_account.transfer(bank_account_2, 20)
print(bank_account.balance)
print(bank_account_2.balance)
print(bank_account.get_transactions())
