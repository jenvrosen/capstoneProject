# import pyrebase

# # You can use this as a reference to utlize the firebaseAPI

# config = {  # This is the information needed to connect to the firebase server


#     'apiKey': "AIzaSyAaaVNdt8QoyJfRmxAc5ogd5IFncTXRuao",
#     'authDomain': "cse120-group323.firebaseapp.com",
#     'projectId': "cse120-group323",
#     'storageBucket': "cse120-group323.appspot.com",
#     'messagingSenderId': "356547945279",
#     'appId': "1:356547945279:web:f876baec35884f4fb0698a",
#     'measurementId': "G-F6LHBSHYYE",
#     'databaseURL':''


# }

# firebase = pyrebase.initialize_app(config) #Used to intialize firebase connection
# auth = firebase.auth()

# email = "TestEmail2@gmail.com" # Test Email
# password = "654321" # Test password

# user = auth.create_user_with_email_and_password(email, password) #Used to create new user
# print(user)

# user = auth.sign_in_with_email_and_password(email, password) # Used to send sign in request to firebase

# info = auth.get_account_info(user['idToken']) # Used to print user info in the console
# print(info)

# auth.send_email_verification(user['idToken']) # Used to send a verification email to person trying to login

# auth.send_password_reset_email(email) # Used to send a password reset email to user