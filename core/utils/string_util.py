import re

password_regex = re.compile(
    r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[!@#\$&*~<>()`~]).{6,}$')
email_regex = re.compile(r'[\w\.\-_]+@[\w\.\-_]+')
phone_regex = re.compile(r'[0-9+][0-9 \-()+\.]{4,}[0-9]')