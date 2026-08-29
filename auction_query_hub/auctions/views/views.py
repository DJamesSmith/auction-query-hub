from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from ..forms import AuctionForm
from ..models import AuctionItem
from ..services import get_all_auction_details_with_seller

def auction_list(request: HttpRequest) -> HttpResponse:
    auctions: list[dict] = get_all_auction_details_with_seller()
    context: dict = {
        "auctions": auctions, 
    }
    return render(request, "auctions/auction_list.html", context)


def create_auction(request: HttpRequest) -> JsonResponse:
    if request.method == "GET":
        form: AuctionForm = AuctionForm()
        context: dict = {
            "form": form,
        }
        return render(request, "auctions/auction_form.html", context)

    if request.method == "POST":
        form: AuctionForm = AuctionForm(request.POST)
        print(f"form: {form}")

        if form.is_valid():
            auction: AuctionItem = form.save()
            print(f"auction: {auction}")

            return JsonResponse({
                    "success": True,
                    "message": "Auction created successfully.",
                    "auction": {
                        "id": auction.id,
                        "title": auction.title,
                        "seller": auction.seller.username,
                    },
                }, status=201)

        return JsonResponse({
                "success": False,
                "errors": form.errors.get_json_data(),
            }, status=400)

    return JsonResponse({
            "success": False,
            "message": "Invalid request method.",
        }, status=405)