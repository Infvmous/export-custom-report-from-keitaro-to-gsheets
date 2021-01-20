import os


def get_gsheets_client_secret_key():
    return os.getenv('GSHEETS_CLIENT_SECRET')