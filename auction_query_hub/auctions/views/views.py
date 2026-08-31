from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render
from ..forms import AuctionForm
from ..models import AuctionItem
from ..services import get_all_auction_details_with_seller

def auction_list(request: HttpRequest) -> HttpResponse:
    auctions: list[dict] = AuctionItem.objects.filter(seller__status=True)      # display those auctions whose seller's status is true/active
    return render(request, "auctions/auction_list.html", { "auctions": auctions })


def create_auction(request: HttpRequest) -> JsonResponse:
    # Render the form with input fields in the templates
    if request.method == "GET":
        form: AuctionForm = AuctionForm()
        return render(request, "auctions/auction_form.html", { "form": form })

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