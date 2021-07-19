from django.core.management.utils import get_random_secret_key
import dotenv
import os
import re


def check_for_existing_django_secret_key_and_create_new_one_if_needed():
    new_secret_key = get_random_secret_key()
    
    try:
        dotenv.load_dotenv()
        secret_key = os.environ['DJANGO_SECRET_KEY']
        match = re.match(r'^\S{50}$', secret_key)
        if not match:
            secret_key = new_secret_key                     
    except KeyError:
        secret_key = new_secret_key

    print( f"DJANGO_SECRET_KEY={secret_key}")


if __name__=="__main__":
    check_for_existing_django_secret_key_and_create_new_one_if_needed()
