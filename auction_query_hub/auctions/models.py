from django.db import models
from users.models import User

class AuctionItem(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_price = models.DecimalField(max_digits=10, decimal_places=2)
    start_time = models.TimeField()             # When the auction becomes active
    end_time = models.TimeField()               # When the auction closes

    # seller field parameter: related_name is used for the invocation of view. Usually it's used for that purpose
    seller = models.ForeignKey(User, on_delete=models.CASCADE, db_column="seller_id", related_name="auctions") # Foreign Key: seller_id

    class Meta:
        db_table = "auction_items"

# related_name="auctions"
# This controls the reverse direction. With this we can do: "user.auctions.all()"