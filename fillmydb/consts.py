class ModelType:
    PEEWEE = 'peewee'
    DJANGO = 'django'
    SQL_ALCHEMY = 'sqlalchemy'

class Provider:

    FAKE_FACTORY = "faker"


class Fields:
    name = 0
    name_female = 1
    name_male = 2
    last_name = 3

    state = 4
    city = 5
    address = 6
    country = 7

    color_name = 8
    hex_color = 9

    company = 10
    catch_phrase = 11

    currency_code = 12

    file_name = 13
    mime_type = 14
    file_extension = 15

    ipv4 = 16
    ipv6 = 17
    mac = 18
    domain = 19
    uri = 20
    username = 21
    email = 22
    company_email = 23

    job = 24

    lorem_sentence = 25
    lorem_word = 26

    md5 = 27
    sha1 = 28
    sha256 = 29
    uuid = 30

    phone_number = 31

    user_agent = 32
    windows_platform = 33
    linux_platform = 34


class FieldSpec:

    def __init__(self, func, *args, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs

    def __repr__(self):
        return "<FieldSpec func={} args={} kwargs={}>".format(self.func, self.args, self.kwargs)

    def call(self):
        return self.func(*self.args, **self.kwargs)
