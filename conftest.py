from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env

pytest_plugins = ['fixtures.page', 'fixtures.user_auth']