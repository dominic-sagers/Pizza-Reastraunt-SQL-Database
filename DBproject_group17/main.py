# Group 17: Database Pizza Project
# Sonya Ozhogina - i6280689
# Dominic Sagers - i6255473

# Class Description: This is our main class for running our software. The software/commandline-script comprises
# different modules in which one may choose whether to display items, order items, or get info on items. Each module
# is a bit chaotically coded but are separated based on the requirements of the project.

import gentlyaskingdb
import keyboard
from datetime import datetime

global allCustomersOrderList


def choose_module():
    isValid = False
    print("Choose a module:\n")
    while not isValid:
        inp = int(input("1: Display Menu\n2: Show Pizza Info\n3: Place an order\n4: I want to quit\n"))
        if inp == 1:
            return 1
        if inp == 2:
            return 2
        if inp == 3:
            return 3
        if inp == 4:
            print("We are sorry to hear it :( Tot ziens!")
            return 4
        else:
            print("\u0332".join("\nPlease choose a valid option >:(\n"))


def order_module():
    customer = 0
    run = True

    # Retrieve customer instance
    while run:
        repeat = str(input("Are you a repeat customer?: "))
        if repeat.lower() == "yes":
            first = str(input("Please enter your First Name: "))
            last = str(input("Please enter your Last Name: "))
            if gentlyaskingdb.customer_exists(first, last):
                customer = gentlyaskingdb.get_customer(first, last)
                run = False
            else:
                print(
                    "\nIt seems we cannot find an account with matching details, please continue to create an account.\n")
        else:
            postalCode = str(input(
                "Valid zip codes are: 6214TS, 6229EN, 6666TS, d, 2305SO, 4553UE, 3456GR, 4356RT, 34. \nPlease enter your zip code: "))
            while not gentlyaskingdb.valid_zipCode(postalCode):
                postalCode = str(input("\nPlease, enter a valid postal code. \n"))
            addressLine = str(input("Please enter your address: "))
            first = str(input("Please enter your First Name: "))
            last = str(input("Please enter your Last Name: "))
            phone = int(input("Please enter your phone number: "))
            customer = gentlyaskingdb.insert_customer(postalCode, addressLine, first, last, phone)
            run = False

    # Create Order
    orderComplete = False
    while not orderComplete:

        orderList = []
        cntNewPizza = 0
        firstPizza = True
        while firstPizza:
            start = str(input("Choose a pizza id of a pizza you want to order: "))
            if gentlyaskingdb.valid_pizza_id(start):
                orderList = orderList + [(gentlyaskingdb.get_pizza(start).name, round(gentlyaskingdb.pizza_price(start),
                                                                                      2))]
                cntNewPizza += 1
                repeat2 = str(input("Would you like to order more pizza? "))
                if repeat2.lower() == "no":
                    firstPizza = False
            else:
                print("The pizza you want to order does not exist. Please, input a valid pizza id.")

        nextStep = 0
        while nextStep != 3:
            nextStep = int(
                input("\nGreat, pal, you've chosen the pizza you want! Maybe some drinks or desserts? I heard "
                      "this gin is the best in town!\n\nIf you want me to display the dessert menu, press 1.\n"
                      "If you want me to display the drinks menu, press 2.\nIf you want to continue to checkout, "
                      "press 3.\n"))

            if nextStep == 1:
                gentlyaskingdb.display_desserts()
                des = int(input("\nIf you want a dessert, insert its id.\nIf you want to quit the menu, press 0.\n"))
                while des != 0:
                    if gentlyaskingdb.valid_dessert_id(des):
                        orderList = orderList + [
                            (gentlyaskingdb.get_dessert(des).name, gentlyaskingdb.get_dessert(des).price)]
                        des = int(
                            input("\nThis dessert was added to your order! If you want more dessert, insert its id.\n"
                                  "If you want to quit the menu, press 0.\n"))
                    else:
                        des = int(input("Please, enter a valid dessert id"))

            if nextStep == 2:
                gentlyaskingdb.display_drinks()
                dri = int(input("\nIf you want a drink, insert its id.\nIf you want to quit the menu, press 0.\n"))
                while dri != 0:
                    if gentlyaskingdb.valid_drink_id(dri):
                        orderList = orderList + [
                            (gentlyaskingdb.get_drink(dri).name, gentlyaskingdb.get_drink(dri).price)]
                        dri = int(input("\nThis drink was added to your order! If you want more drink, insert its id.\n"
                                        "If you want to quit the menu, press 0.\n"))
                    else:
                        dri = int(input("Please, enter a valid drink id."))

        print("You've successfully finished the order.\n")

        newPizzaCount = customer.pizza_count + cntNewPizza
        print("By the way, I've just added the pizzas you bought, in total you have ordered " + str(newPizzaCount) +
              " pizza(s).\n")

        applyDiscount = False

        if not customer.discount_used and customer.pizza_count >= 10:

            inpy = str(input("Would you like to use a discount code?: "))
            if inpy.lower() == "yes":
                finished = False
                while not finished:
                    inpy2 = str(input("Please enter your discount code: "))
                    if gentlyaskingdb.valid_discount_input(inpy2, customer.customer_id):
                        print("Discount will be applied, Woo Hoo!")
                        gentlyaskingdb.set_discount_used(customer)
                        applyDiscount = True
                        finished = True
                    else:
                        "Uuups...There might be a typo in your code. Reenter the discount code, please!\n"
            elif inpy.lower() == "no":
                print("\n Okay, maybe next time!")

        elif not customer.discount_used and newPizzaCount >= 10:
            code = gentlyaskingdb.generate_discount()
            print("Yoo-hoo! Someone's lucky today. By making this order, you've ordered more than 10 (or exactly 10) "
                  "pizzas! Enter the code you'll receive on your phone, when making the next order and entering "
                  "'" + code + "', and get a 10% discount on it!")
            gentlyaskingdb.insert_new_discount(code, customer.customer_id)

        elif newPizzaCount < 10:
            print("After ordering 10 pizzas in our restaurant, you'll get a 10% discount on a next order. You are "
                  "almost there, keep ordering our delicious pizza!")

        gentlyaskingdb.update_pizza_count(newPizzaCount, customer)

        # Send confirmation

        print("Great, you have completed the order! Here is the confirmation\nOrdered items:\n")

        orderSum = 0
        print("----------------------------------------------------------")
        for index, tUple in enumerate(orderList):
            name = tUple[0]
            price = tUple[1]
            orderSum += tUple[1]
            print("'" + name + "'", " $" + str(price))

        print("----------------------------------------------------------")
        if applyDiscount:
            orderSum *= 0.90
        orderSum *= 1.09
        print("Total price (including 9% VAT): " + str(round(orderSum, 2)))

        delivery_module(customer, datetime.now(), cntNewPizza)

        # END of ordering module
        orderComplete = True


def delivery_module(customer, time_ordered, newPizzaCount):
    deliveryInfo = gentlyaskingdb.assign_and_return_driver_and_return_delivery_time(customer.address_id, time_ordered)
    print("\nYour pizza will be delivered at " + str(deliveryInfo[1]))
    print("If you want to cancel your order type \"c\" within next 5 minutes. After 5 minutes the cancellation "
          "is impossible")
    order_not_cancelled = True
    while order_not_cancelled and (datetime.now().second - time_ordered.second) < 300:
        if keyboard.is_pressed('c'):
            gentlyaskingdb.cancel_order(customer, deliveryInfo[0], newPizzaCount)
            print("Your order has been cancelled.")
            order_not_cancelled = False

    if order_not_cancelled:
        print(
            "MWHAHAHAHA YOU HAVE LOST YOUR CHANCE TO CANCEL, OR YOU ACTUALLY WANTED A PIZZA! EITHER WAY, YOUR LOSS.\n")
        print("\nThank you for choosing our pizzeria! Hope to see you soon")


# Main
application_running = True

while application_running:

    mod = choose_module()
    if mod == 1:
        gentlyaskingdb.display_full_menu()
    if mod == 2:
        inp = str(input("Enter the id number of the pizza you wish to view: "))
        if gentlyaskingdb.valid_pizza_id(inp):
            gentlyaskingdb.display_pizza_ingredients(inp)
        else:
            print(inp + " is not a valid pizza id, please try again.")
    if mod == 3:
        order_module()
        gentlyaskingdb.set_busy_since_null()
    if mod == 4:
        application_running = False
