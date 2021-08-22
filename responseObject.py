import dbObject

class ResultRegister:
    def __init__(self, user_id, first_name, last_name, phone_number, address, created_date):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.address = address
        self.created_date = created_date
        
    @property    
    def serialize(self):
      #return object
      return {
          'user_id' : self.user_id,
          'first_name' : self.first_name,
          'last_name' : self.last_name,
          'phone_number' : self.phone_number,
          'address' : self.address,
          'created_date' : self.created_date
          }
    
    
class RegisterResponse:
    def __init__(self, status, user_id, first_name, last_name, phone_number,
                   address,created_date):
        self.status = status
        self.result = ResultRegister(user_id, first_name, last_name, phone_number, address, created_date)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
  
class ResultLogin:
    def __init__(self, access_token, refresh_token):
        self.access_token = access_token
        self.refresh_token = refresh_token
        
    @property    
    def serialize(self):
      #return object
      return {
          'access_token' : self.access_token,
          'refresh_token' : self.refresh_token
          }
    
    
class LoginResponse:
    def __init__(self, status, access_token, refresh_token):
        self.status = status
        self.result = ResultLogin(access_token, refresh_token)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
          
class ResultTopup:
    def __init__(self, top_up_id, amount_top_up, balance_before, balance_after, created_date):
        self.top_up_id = top_up_id
        self.amount_top_up = amount_top_up
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.created_date = created_date
        
    @property    
    def serialize(self):
      #return object
      return {
          'top_up_id' : self.top_up_id,
          'amount_top_up' : self.amount_top_up,
          'balance_before' : self.balance_before,
          'balance_after' : self.balance_after,
          'created_date' : self.created_date
          }
    
    
class TopupResponse:
    def __init__(self, status, top_up_id, amount_top_up, balance_before, balance_after, created_date):
        self.status = status
        self.result = ResultTopup(top_up_id, amount_top_up, balance_before, balance_after, created_date)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
          
class ResultPay:
    def __init__(self, payment_id, amount, remarks, balance_before, balance_after, created_date):
        self.payment_id = payment_id
        self.amount = amount
        self.remarks = remarks
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.created_date = created_date
        
    @property    
    def serialize(self):
      #return object
      return {
          'payment_id' : self.payment_id,
          'amount' : self.amount,
          'remarks' : self.remarks,
          'balance_before' : self.balance_before,
          'balance_after' : self.balance_after,
          'created_date' : self.created_date
          }
    
    
class PayResponse:
    def __init__(self, status, payment_id, amount, remarks, balance_before, balance_after, created_date):
        self.status = status
        self.result = ResultPay(payment_id, amount, remarks, balance_before, balance_after, created_date)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
          
class ResultTransfer:
    def __init__(self, transfer_id, amount, remarks, balance_before, balance_after, created_date):
        self.transfer_id = transfer_id
        self.amount = amount
        self.remarks = remarks
        self.balance_before = balance_before
        self.balance_after = balance_after
        self.created_date = created_date
        
    @property    
    def serialize(self):
      #return object
      return {
          'transfer_id' : self.transfer_id,
          'amount' : self.amount,
          'remarks' : self.remarks,
          'balance_before' : self.balance_before,
          'balance_after' : self.balance_after,
          'created_date' : self.created_date
          }
    
    
class TransferResponse:
    def __init__(self, status, transfer_id, amount, remarks, balance_before, balance_after, created_date):
        self.status = status
        self.result = ResultTransfer(transfer_id, amount, remarks, balance_before, balance_after, created_date)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
          
class ResultTransaction:
    def __init__(self, topup_list, payment_list, transfer_list):
        self.topup_list = topup_list
        self.payment_list = payment_list
        self.transfer_list = transfer_list
        
    @property    
    def serialize(self):
      #return object
      serialize_list = []
      
      for transaction in self.topup_list:
           if transaction["top_up_id"] is not None:
                report = {
                    'top_up_id' : transaction["top_up_id"],
                    'status' : "SUCCESS",
                    'transaction_type' : "CREDIT",
                    'user_id' : transaction["user_id"],
                    'amount' : transaction["amount_top_up"],
                    'remarks' : "",
                    'balance_before' : transaction["balance_before"],
                    'balance_after' : transaction["balance_after"],
                    'created_date' : transaction["created_date"]
                    }
                serialize_list.append(report)
                
      for transaction in self.payment_list:
           if transaction["payment_id"] is not None:
                report = {
                     'payment_id' : transaction["payment_id"],
                     'status' : "SUCCESS",
                     'transaction_type' : "DEBIT",
                     'user_id' : transaction["user_id"],
                     'amount' : transaction["amount"],
                     'remarks' : transaction["remarks"],
                     'balance_before' : transaction["balance_before"],
                     'balance_after' : transaction["balance_after"],
                     'created_date' : transaction["created_date"]
                     }
                serialize_list.append(report)
                
      for transaction in self.transfer_list:
           if transaction["transfer_id"] is not None:
                report = {
                     'transfer_id' : transaction["transfer_id"],
                     'status' : "SUCCESS",
                     'transaction_type' : "DEBIT",
                     'user_id' : transaction["user_id"],
                     'amount' : transaction["amount"],
                     'remarks' : transaction["remarks"],
                     'balance_before' : transaction["balance_before"],
                     'balance_after' : transaction["balance_after"],
                     'created_date' : transaction["created_date"]
                     }
                serialize_list.append(report)
              
      return sorted(serialize_list, key=lambda x: x["created_date"], reverse=True)
    
    
class TransactionResponse:
    def __init__(self, status, topup_list, payment_list, transfer_list):
        self.status = status
        self.result = ResultTransaction(topup_list, payment_list, transfer_list)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
          
class ResultUpdate:
    def __init__(self, user_id, first_name, last_name, address, updated_date):
        self.user_id = user_id
        self.first_name = first_name
        self.last_name = last_name
        self.address = address
        self.updated_date = updated_date
        
    @property    
    def serialize(self):
      #return object
      return {
          'user_id' : self.user_id,
          'first_name' : self.first_name,
          'last_name' : self.last_name,
          'address' : self.address,
          'updated_date' : self.updated_date
          }
    
    
class UpdateResponse:
    def __init__(self, status, user_id, first_name, last_name, address, updated_date):
        self.status = status
        self.result = ResultUpdate(user_id, first_name, last_name, address, updated_date)
        
    @property    
    def serialize(self):
      #return object
      return {
          'status' : self.status,
          'result' : self.result.serialize
          }
      

