import uuid
from datetime import datetime

class Register:
  def __init__(self, first_name, last_name, phone_number, address, pin, balance):
      self.user_id = str(uuid.uuid4())
      self.first_name = first_name
      self.last_name = last_name
      self.phone_number = phone_number
      self.address = address
      self.pin = pin
      self.balance = balance
      self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      self.updated_date = ""
      
  @property    
  def serialize(self):
      #return object
      return {
          'user_id' : self.user_id,
          'first_name' : self.first_name,
          'last_name' : self.last_name,
          'phone_number' : self.phone_number,
          'address' : self.address,
          'pin' : self.pin,
          'created_date' : self.created_date
          }

class Topup:
  def __init__(self, user_id, amount_top_up, balance_before, balance_after):
      self.top_up_id = str(uuid.uuid4())
      self.user_id = user_id
      self.amount_top_up = amount_top_up
      self.balance_before = balance_before
      self.balance_after = balance_after
      self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      
  @property    
  def serialize(self):
      #return object
      return {
          'top_up_id' : self.top_up_id,
          'user_id' : self.user_id,
          'amount_top_up' : self.amount_top_up,
          'balance_before' : self.balance_before,
          'balance_after' : self.balance_after,
          'created_date' : self.created_date
          }

class Pay:
  def __init__(self, user_id, amount, remarks, balance_before, balance_after):
      self.payment_id = str(uuid.uuid4())
      self.user_id = user_id
      self.amount = amount
      self.remarks = remarks
      self.balance_before = balance_before
      self.balance_after = balance_after
      self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      
  @property    
  def serialize(self):
      #return object
      return {
          'payment_id' : self.payment_id,
          'user_id' : self.user_id,
          'amount' : self.amount,
          'remarks' : self.remarks,
          'balance_before' : self.balance_before,
          'balance_after' : self.balance_after,
          'created_date' : self.created_date
          }
  
class Transfer:
  def __init__(self, user_id, target_user, amount, remarks, balance_before, balance_after):
      self.transfer_id = str(uuid.uuid4())
      self.user_id = user_id
      self.target_user = target_user
      self.amount = amount
      self.remarks = remarks
      self.balance_before = balance_before
      self.balance_after = balance_after
      self.created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      
  @property    
  def serialize(self):
      #return object
      return {
          'transfer_id' : self.transfer_id,
          'user_id' : self.user_id,
          'target_user' : self.target_user,
          'amount' : self.amount,
          'remarks' : self.remarks,
          'balance_before' : self.balance_before,
          'balance_after' : self.balance_after,
          'created_date' : self.created_date
          }