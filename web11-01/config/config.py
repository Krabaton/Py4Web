import pathlib
from dotenv import dotenv_values
BASE_DIR = pathlib.Path(__file__).parent.parent
config = dotenv_values('.env')


class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + str(BASE_DIR / "data" / "our_db.sqlite3")
    UPLOAD_FOLDER = str(BASE_DIR / 'uploads')
    SECRET_KEY = config['SECRET_KEY']