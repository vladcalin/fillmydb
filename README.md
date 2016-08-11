# fillmydb
Fill your database with mocked instances.


## Usage

```python

wrapper = ModelWrapper(MyModel)

wrapper.username = FieldSpec(Fields.username)
wrapper.email = FieldSpec(Fields.email)
wrapper.ip_addr = FieldSpec(Fields.ipv4, private=True)
wrapper.real_name = FieldSpec(Fields.full_name)

wrapper.generate(100)

```


```python

wrapper_group = ModelWrapperGroup(
    Users, Comments, Pictures
)

wrapper_group.Users.username = FieldSpec(Fields.username)
wrapper_group.Users.email = FieldSpec(Fields.email)

wrapper_group.Comments.text = FieldSpec(Fields.lorem, phrases=2)
wrapper_group.Comments.posted = FieldSpec(Fields.datetime)

wrapper_group.Pictures.src = FieldSpec(Fields.avatar)
wrapper_group.Pictures.description = FieldSpec(Fields.lorem, words=20)

wrapper_group.generate(100, 200, 320)
```