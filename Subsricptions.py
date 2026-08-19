print("Hello from gamershub!")
print("Welcome to the Gamers Hub subscription service.")

print("Please choose a subscription plan:")
print("1. Basic Plan - $5/month")
print("2. Premium Plan - $10/month")n 
print("3. Elite Plan - $15/month")

print("These plans offer different benefits and features. Please select the plan that best suits your gaming needs.")
user_choice = input("Enter the number of your chosen plan (1, 2, or 3): ")
if user_choice == "1":
    print("You have selected the Basic Plan. Enjoy your gaming experience!")
    print("Enter your payment details to complete the subscription.")
    user_choice = input("Enter your payment details: ")
    print("Payment successful! You are now subscribed to the Basic Plan.")

elif user_choice == "2":
    print("You have selected the Premium Plan. Enjoy your enhanced gaming experience!")
    print("Enter your payment details to complete the subscription.")
    user_choice = input("Enter your payment details: ")
    print("Payment successful! You are now subscribed to the Premium Plan.")

elif user_choice == "3":
    print("You have selected the Elite Plan. Enjoy the ultimate gaming experience!")
    print("Enter your payment details to complete the subscription.")
    user_choice = input("Enter your payment details: ")
    print("Payment successful! You are now subscribed to the Elite Plan.")

else:
    print("Invalid choice. Please restart the program and select a valid subscription plan.")   