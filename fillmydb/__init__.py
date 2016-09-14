from fillmydb.core import FieldSpec, ModelWrapper, initialize_django

try:
    import faker
except ImportError:
    faker = None

__all__ = [
    "FieldSpec",
    "ModelWrapper",
    "initialize_django"
]

__version__ = "0.1.0"
__author__ = "Vlad Calin"


class FieldSpecWrapper:

    def __init__(self, wrapped_callable, *args, **kwargs):
        self.wrapped_callable = wrapped_callable
        self.args = args
        self.kwargs = kwargs

    def __call__(self, *args, **kwargs):
        self.kwargs.update(kwargs)
        return FieldSpec(self.wrapped_callable, *(self.args + args), **self.kwargs)

if faker:
    factory = faker.Factory.create()

    Name = FieldSpecWrapper(factory.name)
    FirstName = FieldSpecWrapper(factory.first_name)
    LastName = FieldSpecWrapper(factory.last_name)

    Username = FieldSpecWrapper(factory.user_name)
    Ipv4 = FieldSpecWrapper(factory.ipv4)
    Ipv6 = FieldSpecWrapper(factory.ipv6)
    Mac = FieldSpecWrapper(factory.mac_address)
    CompanyEmail = FieldSpecWrapper(factory.company_email)
    Url = FieldSpecWrapper(factory.url)
    Uri = FieldSpecWrapper(factory.uri)

    UserAgent = FieldSpecWrapper(factory.user_agent)

    Sentence = FieldSpecWrapper(factory.sentence)       # nb_words
    Word = FieldSpecWrapper(factory.word)
    Paragraph = FieldSpecWrapper(factory.paragraph)     # nb_sentences

    Md5 = FieldSpecWrapper(factory.md5)                 # raw_output
    Sha1 = FieldSpecWrapper(factory.sha1)               # raw_output
    Sha256 = FieldSpecWrapper(factory.sha256)           # raw_output
    Uuid = FieldSpecWrapper(factory.uuid4)

    MimeType = FieldSpecWrapper(factory.mime_type)      # category
    FileName = FieldSpecWrapper(factory.file_name)          # category, extension

if __name__ == '__main__':
    factory = faker.Factory.create()
    # print(factory.paragraph(nb_sentences=5))
    print(FileName().resolve())