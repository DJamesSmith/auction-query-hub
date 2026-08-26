from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from django.db.models import QuerySet

from ..models import AuctionItem
from ..serializers import AuctionSerializer


@api_view(["GET"])
def api_auction_list(request: Request) -> Response:
    auctions: QuerySet[AuctionItem] = AuctionItem.objects.all().order_by("id")
    serializer: AuctionSerializer = AuctionSerializer(auctions, many=True)
    return Response({
            "status": "success",
            "message": "Auctions retrieved successfully.",
            "count": len(serializer.data),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


@api_view(["POST"])
def api_create_auction(request: Request) -> Response:
    serializer: AuctionSerializer = AuctionSerializer(data=request.data)

    if serializer.is_valid():
        auction: AuctionItem = serializer.save()
        print(f"WhatImsendingData: {auction}")

        return Response({
            "status": "success",
            "message": "Auction created successfully.",
            "data": AuctionSerializer(auction).data,
        }, status=status.HTTP_201_CREATED)

    return Response({
        "status": "error",
        "message": "Auction creation failed.",
        "errors": serializer.errors,
    }, status=status.HTTP_400_BAD_REQUEST)