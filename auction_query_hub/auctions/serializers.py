from rest_framework import serializers

from .models import AuctionItem
from users.models import User


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model: AuctionItem = AuctionItem
        fields: tuple[str, ...] = ("id", "title", "description", "base_price", "current_price", "start_time", "end_time", "seller",)


    def validate_title(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Auction title is required.")
        if len(value) < 3:
            raise serializers.ValidationError("Auction title must contain at least 3 characters.")
        return value


    def validate_description(self, value: str) -> str:
        if not value:
            raise serializers.ValidationError("Auction description is required.")
        return value


    def validate_base_price(self, value):
        if value is None:
            raise serializers.ValidationError("Base price is required.")
        if value <= 0:
            raise serializers.ValidationError("Base price must be greater than zero.")
        return value


    def validate_current_price(self, value):
        if value is None:
            raise serializers.ValidationError("Current price is required.")
        if value <= 0:
            raise serializers.ValidationError("Current price must be greater than zero.")
        return value


    def validate_start_time(self, value):
        if not value:
            raise serializers.ValidationError("Start time is required.")
        return value


    def validate_end_time(self, value):
        if not value:
            raise serializers.ValidationError("End time is required.")
        return value


    def validate_seller(self, value):
        if not value:
            raise serializers.ValidationError("Please select a seller.")
        if value.role != User.Role.SELLER:
            raise serializers.ValidationError("Selected user is not a seller.")
        return value


    def validate(self, attrs):
        base_price = attrs.get("base_price")
        current_price = attrs.get("current_price")

        if (base_price is not None and current_price is not None and current_price < base_price):
            raise serializers.ValidationError({ "current_price": "Current price cannot be lower than base price." })

        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if (start_time is not None and end_time is not None and end_time <= start_time):
            raise serializers.ValidationError({ "end_time": "End time must be later than start time."})
        return attrs