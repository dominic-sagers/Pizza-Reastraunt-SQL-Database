# Group 17: Database Pizza Project
# Sonya Ozhogina - i6280689
# Dominic Sagers - i6255473

# Class Description: This class contains all the Session object methods we used to communicate with our database.
# If a method needed to search for, insert, or retrieve something from the database, it was written here.

from datetime import timedelta
from random import randint
from sqlalchemy.orm import sessionmaker
import attempt3

Session = sessionmaker(bind=attempt3.engine)
session = Session()

# The pizza menu is inspired by THE BEST PIZZERIA in Maastricht - Bancale 61. The creators of this code highly
# recommend it!

trial = session.query(attempt3.Drink).all()
print(trial)


def is_vegetarian(product_id):
    for instance in session.query(attempt3.PizzaIngredient).filter_by(pizza_id=product_id):
        for instance2 in session.query(attempt3.Ingredient).filter_by(ingredient_id=instance.ingredient_id):
            if instance2.vegetarian != 1:
                return False
    return True


def pizza_price(product_id):
    summa = 0
    for instance in session.query(attempt3.PizzaIngredient).filter_by(pizza_id=product_id):
        for instance2 in session.query(attempt3.Ingredient).filter_by(ingredient_id=instance.ingredient_id):
            summa += instance2.price
    return summa * 1.4


def display_full_menu():
    print("Pizzas:\n")
    print("----------------------------------------------------------")
    for instance in session.query(attempt3.Pizza).all():
        print(instance.product_id, instance.name, "Vegetarian: " + str(is_vegetarian(instance.product_id)),
              round(pizza_price(instance.product_id), 2), sep=" | ")
    print("----------------------------------------------------------")
    print("\nDrinks: \n")
    print("----------------------------------------------------------")
    for instance in session.query(attempt3.Drink).all():
        print(instance.product_id, instance.name, sep=" | ")
    print("----------------------------------------------------------")
    print("\nDesserts:\n")
    print("----------------------------------------------------------")
    for instance in session.query(attempt3.Dessert).all():
        print(instance.product_id, instance.name, sep=" | ")
    print("----------------------------------------------------------")


def display_drinks():
    print("\nDrinks: \n")
    print("----------------------------------------------------------")
    for instance in session.query(attempt3.Drink).all():
        print(instance.product_id, instance.name, sep=" | ")
    print("----------------------------------------------------------")


def display_desserts():
    print("\nDesserts:\n")
    print("----------------------------------------------------------")
    for instance in session.query(attempt3.Dessert).all():
        print(instance.product_id, instance.name, sep=" | ")
    print("----------------------------------------------------------")


def display_pizza_ingredients(product_id):
    for instance in session.query(attempt3.Pizza).filter_by(product_id=product_id):
        if instance.product_id == product_id:
            print(instance.name + ":")
            print("----------------------------------")
    for instance in session.query(attempt3.PizzaIngredient).filter_by(pizza_id=product_id):
        for instance2 in session.query(attempt3.Ingredient).filter_by(ingredient_id=instance.ingredient_id):
            print(instance2.name, "Vegetarian: " + str(instance2.vegetarian), sep=" | ")
    print("----------------------------------")


def customer_exists(first, last):
    for instance in session.query(attempt3.Customer).filter_by(last_name=last, first_name=first):
        if instance.first_name == first and instance.last_name == last:
            return True
    return False


def generate_discount():
    strr = ""
    for i in range(1, 5):
        strr += str(randint(0, 10))
    return strr


def get_pizza(product_id):
    for instance in session.query(attempt3.Pizza).filter_by(product_id=product_id):
        return instance


def get_drink(product_id):
    for instance in session.query(attempt3.Drink).filter_by(product_id=product_id):
        return instance


def get_dessert(product_id):
    for instance in session.query(attempt3.Dessert).filter_by(product_id=product_id):
        return instance


def get_customer(first, last):
    for instance in session.query(attempt3.Customer).filter_by(last_name=last, first_name=first):
        return instance


def get_postal_code_id(postal_code):
    for instance in session.query(attempt3.PostalCode).filter_by(postal_code=postal_code.replace(" ", "")):
        return instance.postal_code_id


def valid_pizza_id(pizza_id):
    for instance in session.query(attempt3.Pizza).filter_by(product_id=pizza_id):
        return True
    return False


def valid_dessert_id(des_id):
    for instance in session.query(attempt3.Dessert):
        if instance.product_id == des_id:
            return True
    return False


def valid_drink_id(dri_id):
    for instance in session.query(attempt3.Drink):
        if instance.product_id == dri_id:
            return True
    return False


def valid_postal_code(postal_code):
    for instance in session.query(attempt3.PostalCode).filter_by(postal_code=postal_code.replace(" ", "")):
        return True
    return False


def valid_zipCode(zip):
    postal_codes = ["6214TS", "6229EN", "6666TS", "2305OS", "4553UE", "3456GR", "4356RT", "d", "34"]
    if (zip.replace(" ", "")) in postal_codes:
        return True
    False


def insert_new_discount(code, customer_id):
    newDiscount = attempt3.Discount(customer_id=customer_id, code=code)
    session.add(newDiscount)
    session.commit()


def valid_discount_input(code, customer_id):
    for instance in session.query(attempt3.Discount).filter_by(code=code, customer_id=customer_id):
        if instance.code == code and instance.customer_id == customer_id:
            return True
    return False


def set_discount_used(customer):
    s = session.query(attempt3.Customer).filter_by(customer_id=customer.customer_id)
    record = s.one()
    record.discount_used = True
    session.commit()


def update_pizza_count(newPizza, customer):
    s = session.query(attempt3.Customer).filter_by(customer_id=customer.customer_id)
    record = s.one()
    record.pizza_count = newPizza
    session.commit()


def set_busy_since(emp, time):
    s = session.query(attempt3.DeliveryEmployee).filter_by(emp_id=emp.emp_id)
    record = s.one()
    record.busy_since = time
    session.commit()


def set_busy_since_null():
    s = session.query(attempt3.DeliveryEmployee).all()
    for n in s:
        n.busy_since = None
    session.commit()


def get_postal_code_id(postalCode):
    for instance in session.query(attempt3.PostalCode).filter_by(postal_code=postalCode):
        return instance.postal_code_id


def cancel_order(customer, emp, number_of_pizzas):
    s1 = session.query(attempt3.Customer).filter_by(customer_id=customer.customer_id)
    for n in s1:
        n.pizza_count = n.pizza_count - number_of_pizzas

    s2 = session.query(attempt3.DeliveryEmployee).filter_by(emp_id=emp.emp_id)
    for n in s2:
        n.busy_since = None
    session.commit()


def assign_and_return_driver_and_return_delivery_time(address_id, time):
    deliveryEmps = []
    for instance in session.query(attempt3.Address).filter_by(address_id=address_id):
        addressRec = instance
    for instance in session.query(attempt3.DeliveryEmployee).filter_by(
            postal_code_id=addressRec.postal_code_id).order_by(attempt3.DeliveryEmployee.busy_since):
        deliveryEmps.append((instance, instance.busy_since))

    # 0 index = deliveryEmployee object , 1 index = delivery time
    deliveryInfo = []

    set_busy_since(deliveryEmps[0][0], time)

    deliveryInfo.append(deliveryEmps[0][0])
    deliveryInfo.append(get_delivery_time(time, deliveryEmps[0][1]))
    return deliveryInfo


def get_delivery_time(currentTime, busy_since):
    if busy_since is None:
        return currentTime + timedelta(minutes=25)
    return max(currentTime + timedelta(minutes=25), busy_since + timedelta(minutes=45))


def insert_customer(zip, addressLine, first, last, phone):
    # Order of queries:
    # 1. Check if zip code exists
    # if it does retrieve the postal_code_id
    # if not, insert it and retrieve the postal_code_id
    if valid_postal_code(zip):
        postal_id = get_postal_code_id(zip)
    else:
        newZip = attempt3.PostalCode(postal_code=zip.replace(" ", ""))
        session.add(newZip)
        session.commit()

        postal_id = get_postal_code_id(zip.replace(" ", ""))
    # 2. Using the postal code id, insert a new address record with it and addressLine and save the address_line_id
    newAddy = attempt3.Address(address_line=addressLine, postal_code_id=postal_id)
    session.add(newAddy)
    session.commit()

    for instance in session.query(attempt3.Address).filter_by(address_line=addressLine):
        addressId = instance.address_id
    # 3. Finally, insert a customer entry using the first, last, phone, and address_line_id values and set the other
    # fields to default
    newCust = attempt3.Customer(first_name=first, last_name=last, phone_number=phone, address_id=addressId,
                                pizza_count=0, discount_used=False)
    session.add(newCust)
    session.commit()
    return newCust
