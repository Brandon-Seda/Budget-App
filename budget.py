
import math



class Category:

  def __init__(self, name):
    self.ledger = list()
    self.name = name

  def __str__(self):
    header = str(self.name).center(30,"*") + "\n"
    total_balance = 0
    transactions = ""
    for content in self.ledger:
      left_content = "{:<23}".format(content["description"])
      right_content = "{:>7.2f}".format(content["amount"])

      transactions += "{}{}\n".format(left_content[:23], right_content[:7])

      total_balance += content['amount']
    total_balance = "{:.2f}".format(total_balance)
  
    output = header + transactions + "Total: " + str(total_balance)
    return output

  def deposit(self, amount, description = ""):
    self.ledger.append({"amount" : amount, "description" : description})

  def withdraw(self, amount, description = ""):
    if self.check_funds(amount):
      self.ledger.append({"amount" : -amount, "description" : description})
      return True
    return False

  def get_balance(self):
    total_balance = 0
    for amounts in self.ledger:
      total_balance += amounts["amount"]
    return total_balance

  def transfer(self, amount, category):
    if self.check_funds(amount):
      self.withdraw(amount, "Transfer to " + category.name)
      category.deposit(amount, "Transfer from " + self.name)
      return True
    return False
  

  def check_funds(self, amount):    
    if self.get_balance() >= amount:
      return True 
    else:
      return False

    return False
      

  def get_withdraw(self):
    withdraw_list = list()
    balance = 0
    prefix  = ""
    for item in self.ledger:
      prefix = item['description'].startswith("Transfer to")
      if item['amount'] < 0 and item['description'] != prefix: 
        if item['amount'] not in withdraw_list:
          withdraw_list.append(abs(item['amount']))
         
    
    for i in withdraw_list:
      balance += i
    return balance


def create_spend_chart(categories):
  header = "Percentage spent by category\n"
  total_balance = 0
  percentage = list()
  for i in categories:
    category_balance = abs(Category.get_withdraw(i)) 
    total_balance = total_balance + category_balance
  #gets rounded withdraw percentages
  for i in categories:
    amount = 0
    category_balance = abs(Category.get_withdraw(i))
    amount_unrounded = (category_balance/total_balance) * 100
    amount = math.floor(amount_unrounded/10) *10
    percentage.append(amount)

  x = 100
  y = {100 : "100|", 90 : "90|", 80 : "80|", 70 : "70|", 60 : "60|", 50 : "50|", 40 : "40|",
        30 : "30|", 20 : "20|", 10 : "10|", 0 : "0|"}

  index = 100
  space = "   "
  mark = " o "
  chart = header

  for i in reversed(range(0, 101, 10)):
    chart += f"{y[i] :>4}"
    
    for j in range(len(percentage)):
      if percentage[j] >= i:
        chart += mark
      else:
        chart += space
    chart += " \n"
  
  footer = (space + " ") +"-" * ((3 * len(categories)) + 1) + "\n"

  chart += footer

  names = []
  for i in range(len(categories)):
    names.append(categories[i].name)
  
  longest_name = max(names, key=len)
  for i in range(len(categories)):
    while len(names[i]) < len(longest_name):
      names[i] += " "

  vert_names = []
  for i in range(len(longest_name)):
    for j in range(len(names)):

      vert_names.append(names[j][i])
  
  for i in range(len(vert_names)):
        if i %(len(names)) == 0:
            chart +=  "    {:^3}".format(vert_names[i])
        elif i%(len(names)) == len(names) -1:
            if i == len(vert_names) -1:
                chart += " {}  ".format(vert_names[i])
            else:
                chart += " {}  \n".format(vert_names[i])
        else:
            chart += "{:^3}".format(vert_names[i])


  return chart