from flask import Config

from private import dev_db_url

class DevConfig(Config):
    debug = True
    SQLALCHEMY_DATABASE_URI = dev_db_url
    SECRET_KEY = b'\x7f\xd2\r\xfd\xddoq\xfd\x08O\xf6\xb9\xe6\xe9\xa7?\x885\xdfa\x993\xdePJ\x94\xac\xbeV\xc0#\xef\xec\x9a&\xcd"\xa5\x82~\x13\x8a\xa7\xf8\xb8\x12\x8d\xd3\x01\n\xaek!\x87\x96x\x10\xf3X\xc1\xf5D6\xa8'
