import sys
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
import csv
#  Update the users in this list.
#  Each tuple represents the username, password, and email of a user.
def create_users(path):
    User = get_user_model()

    users = []
    with open(path, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        first_row=True
        for row in reader:

            username,password = row
            users.append((username,password))

    for username, password in users:
        try:
            print 'Creating user {0}.'.format(username)
            user = User.objects.create_user(username=username)
            user.set_password(password)
            user.save()

            assert authenticate(username=username, password=password)
            print 'User {0} successfully created.'.format(username)

        except:
            print 'There was a problem creating the user: {0}.  Error: {1}.' \
                .format(username, sys.exc_info()[1])
