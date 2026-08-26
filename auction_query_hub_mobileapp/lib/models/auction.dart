/// Mirrors `auctions.serializers.AuctionSerializer`.
/// `seller` is a plain primary-key int on this endpoint (the serializer does
/// not nest the seller object), so it is stored here as [sellerId].
class Auction {
  final int id;
  final String title;
  final String description;
  final double basePrice;
  final double currentPrice;
  final String startTime;
  final String endTime;
  final int sellerId;

  const Auction({
    required this.id,
    required this.title,
    required this.description,
    required this.basePrice,
    required this.currentPrice,
    required this.startTime,
    required this.endTime,
    required this.sellerId,
  });

  factory Auction.fromJson(Map<String, dynamic> json) {
    return Auction(
      id: _asInt(json['id']),
      title: json['title']?.toString() ?? 'Untitled Auction',
      description: json['description']?.toString() ?? '',
      basePrice: _asDouble(json['base_price']),
      currentPrice: _asDouble(json['current_price']),
      startTime: json['start_time']?.toString() ?? '',
      endTime: json['end_time']?.toString() ?? '',
      sellerId: _asInt(json['seller']),
    );
  }

  /// Field name here MUST be `seller` (not `seller_id`) — that is what
  /// AuctionSerializer.Meta.fields declares on the Django side.
  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'base_price': basePrice,
      'current_price': currentPrice,
      'start_time': startTime,
      'end_time': endTime,
      'seller': sellerId,
    };
  }

  static int _asInt(dynamic value) {
    if (value is int) return value;
    return int.tryParse('$value') ?? 0;
  }

  static double _asDouble(dynamic value) {
    if (value is num) return value.toDouble();
    return double.tryParse('$value') ?? 0.0;
  }
}
