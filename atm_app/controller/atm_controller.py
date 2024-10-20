from enum import Enum
from atm_app.bank_client.bank_api import BankAPI, ConnectionState, BankAPIResponse, BankAPIError

class AtmState(Enum):
  BOOTING = 1
  WAITING = 2
  WAITING_PIN = 3
  AUTHENTICATED = 4
  CASH_BIN_EMPTY = 5
  ERROR = 6

class AtmError(Enum):
  CARD_CANNOT_BE_INSERTED = 1

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
