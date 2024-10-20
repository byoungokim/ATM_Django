from django.test import TestCase
from atm_app.controller.atm_controller import AtmController, AtmState, AtmError

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
    self.assertEqual(result, AtmState.WAITING)
