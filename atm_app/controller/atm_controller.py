from enum import Enum
from atm_app.bank_client.bank_api import BankAPI, ConnectionState, BankAPIResponse, BankAPIError

class AtmState(Enum):
  BOOTING = 1
  WAITING = 2
  WAITING_PIN = 3
  AUTHENTICATED = 4
  WAITING_ACTION = 5
  SHOWING_BALANCE = 6
  WAITING_FOR_DEPOSIT = 7
  WAITING_FOR_WITHDRAWAL = 8
  CASH_BIN_EMPTY = 20
  ERROR = 99

class AtmError(Enum):
  CARD_CANNOT_BE_INSERTED = 1
  BANK_IS_OFFLINE = 2
  INSUFFICIENT_BALANCE = 3

class AtmController():
  def __init__(self):
    self.atm_state = AtmState.BOOTING
    self.bank_api = BankAPI()
    self.bank_api.connect()

  def insert_card(self):
      """
      Inserts a card into the ATM.

      Returns:
          AtmError: If the ATM is in the BOOTING state, returns CARD_CANNOT_INSERTED.
      """
      if self.atm_state == AtmState.BOOTING:
        return AtmError.CARD_CANNOT_BE_INSERTED
      if self.atm_state == AtmState.WAITING:
        self.show_message('Please Input Your PIN Number')
        self.atm_state == AtmState.WAITING_PIN
      if self.atm_state == AtmState.WAITING_PIN:
        self.show_message('You should not insert the card again')
        return AtmError.CARD_CANNOT_BE_INSERTED
      return self.atm_state

  def check_pin(self, pin):
    """
    Checks the PIN entered by the user.

    Parameters:
    pin (str): The PIN entered by the user.

    Returns:
    AtmState: The state of the ATM after checking the PIN.
    """
    if self.atm_state == AtmState.WAITING_PIN:
      result, error = self.bank_api.check_pin(1, pin)
      if error == BankAPIError.BANK_IS_OFFLINE:
        self.show_message('Bank is offline')
        return AtmState.ERROR
      if result == BankAPIResponse.AUTHENTICATED:
        self.show_message('PIN is correct')
        self.atm_state = AtmState.AUTHENTICATED
      else:
        self.show_message('PIN is incorrect')

    return self.atm_state

  def list_accounts(self):
    """
    Lists the accounts available for the authenticated user.

    Returns:
    None
    """
    self.show_message('Listing accounts')
    self.show_message(self.bank_api.get_accounts().join("\\n"))

  def select_account(self, account):
    """
    Selects the account to be used for transactions.

    Parameters:
    account (str): The account selected by the user.

    Returns:
    None
    """
    if self.atm_state != AtmState.AUTHENTICATED:
      self.show_message('You are not authenticated')
      return AtmState.ERROR
    self.atm_state = AtmState.WAITING_ACTION
    self.show_message('Selected account: ' + account)
  
  def select_action(self, action):
    """
    Selects the action to be performed on the selected account.

    Parameters:
    action (str): The action selected by the user.

    Returns:
    None
    """
    if self.atm_state != AtmState.WAITING_ACTION:
      self.show_message('You should select an account first')
      return AtmState.ERROR
    if action == 'deposit':
      self.show_message('Selected action: deposit')
    elif action == 'withdraw':
      self.show_message('Selected action: withdraw')
    else:
      self.show_message('Invalid action')
      return AtmState.ERROR

  def see_balance(self, account):
    """
    Shows the balance of the selected account.

    Returns:
    None
    """
    if self.atm_state != AtmState.WAITING_ACTION:
      self.show_message('You should select an account first')
      return AtmState.ERROR
    result, error = self.bank_api.get_balance(account)
    if error == BankAPIError.BANK_IS_OFFLINE:
      self.show_message('Bank is offline')
      return AtmError.BANK_IS_OFFLINE
    else:
      if result:
        self.show_message('Balance: $' + str(result))
        self.atm_state = AtmState.SHOWING_BALANCE
        return result

  def deposit(self, account, amount):
    """
    Deposits an amount to the selected account.

    Parameters:
    account (str): The account selected by the user.
    amount (int): The amount to be deposited.

    Returns:
    None
    """
    if self.atm_state != AtmState.WAITING_ACTION:
      self.show_message('You should select an account first')
      return AtmState.ERROR
    result = self.bank_api.deposit(account, amount)
    if result == BankAPIError.BANK_IS_OFFLINE:
      self.show_message('Bank is offline')
      return AtmError.BANK_IS_OFFLINE
    else:
      self.show_message('Deposited $' + str(amount))

  def withdraw(self, account, amount):
    """
    Withdraws an amount from the selected account.

    Parameters:
    account (str): The account selected by the user.
    amount (int): The amount to be withdrawn.

    Returns:
    None
    """
    if self.atm_state != AtmState.WAITING_ACTION:
      self.show_message('You should select an account first')
      return AtmState.ERROR
    error = self.bank_api.withdraw(account, amount)
    if error == BankAPIError.BANK_IS_OFFLINE:
      self.show_message('Bank is offline')
      return AtmError.BANK_IS_OFFLINE
    elif error == BankAPIError.INSUFFICIENT_BALANCE:
      self.show_message('Insufficient balance')
      return AtmError.INSUFFICIENT_BALANCE
    else:
      self.show_message('Withdrawn $' + str(amount))
      return None

  def show_message(self, message):
    """
    Display a message on the standard output.

    Parameters:
    message (str): The message to be displayed.

    Returns:
    None
    """
    # Use the standard output to show a message before integrating with a frontend.
    print(message)
