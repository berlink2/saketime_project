import sys, os
import pandas

os.environ.setdefault('DJANGO_SETTINGS_MODULE', "saketime_project.settings")

import django
django.setup()

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model

#python load_users.py main/data/users.csv

def save_user_from_row(user_row):
    user = get_user_model(email=user_row[1], username=user_row[2], id=user_row[0])



    user.save()



if __name__ == '__main__':
    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        users_df = pandas.read_csv(sys.argv[1])
        print(users_df)

        users_df.apply(
            save_user_from_row,
            axis=1
        )

        print("Users loaded")

    else:
        print("Provide filepath to user csv file")