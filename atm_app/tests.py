from django.test import TestCase
from atm_app.controller.atm_controller import AtmController, AtmState, AtmError
from atm_app.bank_client.bank_api import BankAPI, ConnectionState, BankAPIResponse, BankAPIError

class TestAtmController(TestCase):
  def setUp(self):
    self.atm_controller = AtmController()

  def test_insert_card_booting_state(self):
    self.atm_controller.atm_state = AtmState.BOOTING
    result = self.atm_controller.insert_card()
    self.assertEqual(result, AtmError.CARD_CANNOT_BE_INSERTED)

  def test_insert_card_waiting_state(self):
    self.atm_controller.atm_state = AtmState.WAITING
    result = self.atm_controller.insert_card()
    self.assertEqual(result, AtmState.WAITING)

  def test_insert_card_waiting_pin_state(self):
    self.atm_controller.atm_state = AtmState.WAITING_PIN
    result = self.atm_controller.insert_card()
    self.assertEqual(result, AtmError.CARD_CANNOT_BE_INSERTED)

  def test_check_pin_correct(self):
    self.atm_controller.atm_state = AtmState.WAITING_PIN
    result = self.atm_controller.check_pin('1234')
    self.assertEqual(result, AtmState.AUTHENTICATED)

  def test_check_pin_incorrect(self):
    self.atm_controller.atm_state = AtmState.WAITING_PIN
    result = self.atm_controller.check_pin('4321')
    self.assertEqual(result, AtmState.WAITING_PIN)

class TestBankAPI(TestCase):
  def test_connect(self):
    bank_api = BankAPI()
    bank_api.connect()
    self.assertEqual(bank_api.connection_state, ConnectionState.CONNECTED)

  def test_check_pin_bank_offline(self):
    bank_api = BankAPI()
    _, result = bank_api.check_pin(1, '1234')
    self.assertEqual(result, BankAPIError.BANK_IS_OFFLINE)

  def test_check_pin_correct(self):
    bank_api = BankAPI()
    bank_api.connect()
    result, _ = bank_api.check_pin(1, '1234')
    self.assertEqual(result, BankAPIResponse.AUTHENTICATED)

  def test_check_pin_incorrect(self):
    bank_api = BankAPI()
    bank_api.connect()
    _, result = bank_api.check_pin(1, '4321')
    self.assertEqual(result, BankAPIError.AUTHENTICATION_FAILED)

  def test_get_accounts_bank_offline(self):
    bank_api = BankAPI()
    _, result = bank_api.get_accounts(1)
    self.assertEqual(result, BankAPIError.BANK_IS_OFFLINE)

  def test_get_accounts_correct(self):
    bank_api = BankAPI()
    bank_api.connect()
    result, _ = bank_api.get_accounts(1)
    self.assertEqual(result, ['Account 1', 'Account 2', 'Account 3'])
