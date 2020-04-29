import sys,os
import datetime
import pandas
os.environ.setdefault('DJANGO_SETTINGS_MODULE', "saketime_project.settings")

import django
django.setup()

from main.models import Review, UserProfile, Product

def save_review_from_row(review_row):
    review= Review()
    userprofile = UserProfile.objects.get(id=review_row[1])
    sake = Product.objects.get(id=review_row[2])

    review.id = review_row[0]
    review.user = userprofile
    review.sake = sake
    review.rating = review_row[3]
    review.content = review_row[4]
    review.date = datetime.datetime.now()
    review.save()



if __name__ == "__main__":

    if len(sys.argv) == 2:
        print("Reading from file " + str(sys.argv[1]))
        reviews_df = pandas.read_csv(sys.argv[1])
        print(reviews_df)

        reviews_df.apply(
            save_review_from_row,
            axis=1
        )

    else:
        print("Please, provide Reviews file path")