from enum import Enum

class ConnectionState(Enum):
    OFFLINE = 1
    CONNECTED = 2

class BankAPIResponse(Enum):
    AUTHENTICATED = 1
    WAITING = 2

class BankAPIError(Enum):
    BANK_IS_OFFLINE = 1
    AUTHENTICATION_FAILED = 2
    INSUFFICIENT_BALANCE = 3

class BankAPI:
    def __init__(self):
        self.connection_state = ConnectionState.OFFLINE
        print('Bank API initialized')

    def connect(self):
        print('Connected to bank')
        self.connection_state = ConnectionState.CONNECTED

    def check_pin(self, card_num, pin):
        if self.connection_state == ConnectionState.CONNECTED:
            if card_num == 1 and pin == '1234':
                print('PIN is correct')
                return BankAPIResponse.AUTHENTICATED, None
            else:
                print('PIN is incorrect')
                return None, BankAPIError.AUTHENTICATION_FAILED
        else:
            print('Bank is offline')
            return None, BankAPIError.BANK_IS_OFFLINE

    def get_accounts(self, card_num):
        if self.connection_state == ConnectionState.CONNECTED:
            if card_num == 1:
                print('Returning account list')
                return ['Account 1', 'Account 2', 'Account 3'], None
        else:
            print('Bank is offline')
            return None, BankAPIError.BANK_IS_OFFLINE

    def get_balance(self, account_num):
        if self.connection_state == ConnectionState.CONNECTED:
            if account_num == 1:
                print('Returning balance')
                return 1000, None
        else:
            print('Bank is offline')
            return None, BankAPIError.BANK_IS_OFFLINE
        
    def deposit(self, account_num, amount):
        if self.connection_state == ConnectionState.CONNECTED:
            if account_num == 1:
                print('Depositing amount')
                return None
        else:
            print('Bank is offline')
            return BankAPIError.BANK_IS_OFFLINE

    def withdraw(self, account_num, amount):
        if self.connection_state == ConnectionState.CONNECTED:
            if account_num == 1:
                if amount <= 1000:
                    print('Withdrawing amount')
                    return None
                else:
                    print('Insufficient balance')
                    return BankAPIError.INSUFFICIENT_BALANCE
        else:
            print('Bank is offline')
            return BankAPIError.BANK_IS_OFFLINE
