# Group 17: Database Pizza Project
# Sonya Ozhogina - i6280689
# Dominic Sagers - i6255473

# Class Description: This class is the ORM MySQL-Python sqlalchemy mapper which we used to create query-able
# classes to interact with our DBMS. Running this class once with correct credentials and assignments will set the
# connections necessary to communicate with the database.


import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Column, String, Float, ForeignKey, Boolean, DateTime

# The stars here have replaced a MySQL login.
engine = sqlalchemy.create_engine("mysql://****:*********@localhost/pizza",
                                  echo=False)
base = declarative_base()


class Pizza(base):
    __tablename__ = "pizza"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(20))


class Drink(base):
    __tablename__ = "drink"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(20))
    price = Column(Float)


class Dessert(base):
    __tablename__ = "dessert"
    product_id = Column(Integer, primary_key=True)
    name = Column(String(20))
    price = Column(Float)


class Ingredient(base):
    __tablename__ = "ingredient"
    ingredient_id = Column(Integer, primary_key=True)
    name = Column(String(20))
    price = Column(Float)  # not sure here #
    vegetarian = Column(Boolean)


class PizzaIngredient(base):
    __tablename__ = "pizza_ingredient"
    pizza_id = Column(Integer, ForeignKey("pizza.pizza_id"), primary_key=True)
    ingredient_id = Column(Integer, ForeignKey("ingredient.ingredient_id"), primary_key=True)


class PostalCode(base):
    __tablename__ = "postal_code"
    postal_code_id = Column(Integer, primary_key=True)
    postal_code = Column(String(20))


class Address(base):
    __tablename__ = "address"
    address_id = Column(Integer, primary_key=True)
    address_line = Column(String(20))
    postal_code_id = Column(Integer, ForeignKey("postal_code.postal_code_id"))


class Customer(base):
    __tablename__ = "customer"
    customer_id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    phone_number = Column(Integer)
    address_id = Column(Integer, ForeignKey("address.address_id"))
    pizza_count = Column(Integer)
    discount_used = Column(Boolean)


class DeliveryEmployee(base):
    __tablename__ = "delivery_employee"
    emp_id = Column(Integer, primary_key=True)
    first_name = Column(String(20))
    last_name = Column(String(20))
    postal_code_id = Column(Integer, ForeignKey("postal_code.postal_code_id"))
    busy_since = Column(DateTime)


class Discount(base):
    __tablename__ = "discount"
    code_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey("customer.customer_id"))
    code = Column(String(8))


base.metadata.create_all(engine)
