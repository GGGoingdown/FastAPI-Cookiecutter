from tortoise import fields, models


class User(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=50)
    email = fields.CharField(max_length=50, unique=True, index=True)
    password_hash = fields.CharField(max_length=128)

    class Meta:
        table = "users"

    def __str__(self):
        return f"User(id={self.id}, name={self.name}"
