from django.db import models

class User(models.Model):
    class Meta:
        db_table = "users"


    class Role(models.TextChoices):
        BUYER = ("Buyer", "Buyer",)                 # 1st value stored in the table and 2nd shown in dropdown to the users
        SELLER = ("Seller", "Seller",)
        ADMIN = ("Admin", "Admin",)

    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=Role.choices)
    status = models.BooleanField(default=True)      # True = active, False = soft-deleted
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username