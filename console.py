#!/usr/bin/python3
#from typing import Optional, List
#from near_sdk import borsh, collections, Promise, env, near_bindgen, serde
#from near_sdk import AccountId

# Function to assign the value of a near coin to a u128 bit value
def _one_near() -> int:
    return int("1000000000000000000000000")

# Public struct representing a product
#@serde.serialize
#@serde.deserialize
class Product:
    def __init__(self, name: str, cost: int, quantity: int):
        self.name = name
        self.cost = cost
        self.quantity = quantity

# Public struct representing sales
#@serde.serialize
#@serde.deserialize
class Sales:
    def __init__(self, product_name: str, quantity: int):
        self.product_name = product_name
        self.quantity = quantity

# Public struct representing Pharmacy
#@near_bindgen
class Pharmacy:
    def __init__(self):
        self.sales_history = collections.LookupMap[AccountId, List[Sales]]()
        self.products = collections.Vector[Product]()

    def get_products(self) -> List[Product]:
        return self.products.to_list()

    def get_sale_history(self) -> Optional[List[Sales]]:
        return self.sales_history.get(env.current_account_id())

    def add_drug(self, name: str, cost: int, quantity: int):
        pr = Product(name, cost, quantity)
        self.products.push(pr)

    #@Promise
    def sale_drug(self, name: str, quantity: int):
        index_drug = None

        for index, drug in enumerate(self.products):
            if drug.name == name:
                if drug.quantity < quantity:
                    f = f"We cannot sell you this quantity {quantity} as we have {drug.quantity}"
                    env.log_str(f)
                else:
                    total_cost = drug.cost * quantity

                    if total_cost > env.attached_deposit():
                        env.panic_str("You have insufficient funds ")
                    else:
                        index_drug = index

        if index_drug is not None:
            product = self.products.get(index_drug)
            product.quantity -= quantity

            total_cost = product.cost * quantity

            self.products.replace(index_drug, product)
            Promise(env.current_account_id()).transfer(total_cost)

            user_history = self.sales_history.get(env.current_account_id())

            sale = Sales(name, quantity)

            if user_history is not None:
                user_history.append(sale)
                self.sales_history.insert(env.current_account_id(), user_history)
            else:
                drugs = [Sales("sample", 122)]
                self.sales_history.insert(env.current_account_id(), drugs)

# Unit tests
def add_pharmacy():
    pham = Pharmacy()
    pham.add_drug("insulin", 200, 10)
    assert len(pham.products) == 1

def sell_drug():
    user = AccountId("erastus.testnet")
    context = get_context(user)
    bal = _one_near() * 2
    context.attached_deposit(bal)
    context.account_balance(bal)

    testing_env(context.build())

    pham = Pharmacy()
    pham.add_drug("insulin", _one_near(), 10)
    pham.sale_drug("insulin", 1)

    for x in pham.products:
        if x.name == "insulin":
            assert x.quantity == 9
            break