import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models/auction.dart';

class AuctionsList extends StatefulWidget {
  const AuctionsList({super.key});

  @override
  State<AuctionsList> createState() => _AuctionsListState();
}

class _AuctionsListState extends State<AuctionsList> {
  final ApiService apiService = ApiService();

  List<Auction> auctions = [];

  bool isLoading = true;
  String? error;

  @override
  void initState() {
    super.initState();

    loadAuctions();
  }

  Future<void> loadAuctions() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      final result = await apiService.getAuctions();

      setState(() {
        auctions = result;
        isLoading = false;
      });
    } catch (e) {
      setState(() {
        error = e.toString();
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),

      appBar: AppBar(
        title: const Text(
          'Auctions',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),

        actions: [
          IconButton(
            onPressed: loadAuctions,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),

      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (isLoading) {
      return const Center(
        child: CircularProgressIndicator(),
      );
    }

    if (error != null) {
      return _buildError();
    }

    if (auctions.isEmpty) {
      return _buildEmpty();
    }

    return RefreshIndicator(
      onRefresh: loadAuctions,

      child: ListView(
        padding: const EdgeInsets.all(20),

        children: [

          Row(
            children: [

              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,

                  children: [

                    const Text(
                      'Auction Items',
                      style: TextStyle(
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    const SizedBox(height: 6),

                    Text(
                      '${auctions.length} auctions found',
                      style: const TextStyle(
                        color: Colors.grey,
                      ),
                    ),
                  ],
                ),
              ),

              Container(
                padding: const EdgeInsets.all(12),

                decoration: BoxDecoration(
                  color: Theme.of(context)
                      .colorScheme
                      .primary
                      .withOpacity(0.1),
                  borderRadius: BorderRadius.circular(12),
                ),

                child: Icon(
                  Icons.gavel_outlined,
                  color: Theme.of(context).colorScheme.primary,
                ),
              ),
            ],
          ),

          const SizedBox(height: 20),

          ...auctions.map(
            (auction) => _buildAuctionCard(auction),
          ),
        ],
      ),
    );
  }

  Widget _buildAuctionCard(Auction auction) {
    final title = auction.title;
    final description = auction.description.isNotEmpty ? auction.description : 'No description';
    final basePrice = auction.basePrice.toStringAsFixed(2);
    final currentPrice = auction.currentPrice.toStringAsFixed(2);
    final startTime = auction.startTime.isNotEmpty ? auction.startTime : '--';
    final endTime = auction.endTime.isNotEmpty ? auction.endTime : '--';

    return Container(
      margin: const EdgeInsets.only(bottom: 16),

      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(20),

        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 12,
            offset: const Offset(0, 5),
          ),
        ],
      ),

      child: Padding(
        padding: const EdgeInsets.all(20),

        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,

          children: [

            Row(
              children: [

                Container(
                  padding: const EdgeInsets.all(11),

                  decoration: BoxDecoration(
                    color: Theme.of(context)
                        .colorScheme
                        .primary
                        .withOpacity(0.1),
                    borderRadius: BorderRadius.circular(12),
                  ),

                  child: Icon(
                    Icons.gavel,
                    color: Theme.of(context).colorScheme.primary,
                  ),
                ),

                const SizedBox(width: 14),

                Expanded(
                  child: Text(
                    title,
                    style: const TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                    ),
                  ),
                ),
              ],
            ),

            const SizedBox(height: 14),

            Text(
              description,
              maxLines: 3,
              overflow: TextOverflow.ellipsis,

              style: const TextStyle(
                color: Colors.grey,
                height: 1.4,
              ),
            ),

            const SizedBox(height: 20),

            Row(
              children: [

                Expanded(
                  child: _PriceItem(
                    label: 'Base Price',
                    value: '₹$basePrice',
                  ),
                ),

                Expanded(
                  child: _PriceItem(
                    label: 'Current Price',
                    value: '₹$currentPrice',
                    highlight: true,
                  ),
                ),
              ],
            ),

            const SizedBox(height: 18),

            const Divider(),

            const SizedBox(height: 12),

            Row(
              children: [

                Expanded(
                  child: _TimeItem(
                    icon: Icons.play_arrow_outlined,
                    label: 'Starts',
                    value: startTime,
                  ),
                ),

                Expanded(
                  child: _TimeItem(
                    icon: Icons.stop_outlined,
                    label: 'Ends',
                    value: endTime,
                  ),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildEmpty() {
    return const Center(
      child: Padding(
        padding: EdgeInsets.all(30),

        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,

          children: [

            Icon(
              Icons.gavel_outlined,
              size: 70,
              color: Colors.grey,
            ),

            SizedBox(height: 20),

            Text(
              'No auctions found',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),

            SizedBox(height: 8),

            Text(
              'There are currently no auction items available.',
              textAlign: TextAlign.center,
              style: TextStyle(
                color: Colors.grey,
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildError() {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(30),

        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,

          children: [

            const Icon(
              Icons.cloud_off_outlined,
              size: 70,
              color: Colors.redAccent,
            ),

            const SizedBox(height: 20),

            const Text(
              'Unable to load auctions',
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
              ),
            ),

            const SizedBox(height: 10),

            Text(
              error!,
              textAlign: TextAlign.center,
              style: const TextStyle(
                color: Colors.grey,
              ),
            ),

            const SizedBox(height: 20),

            ElevatedButton.icon(
              onPressed: loadAuctions,
              icon: const Icon(Icons.refresh),
              label: const Text('Try Again'),
            ),
          ],
        ),
      ),
    );
  }
}

class _PriceItem extends StatelessWidget {
  final String label;
  final String value;
  final bool highlight;

  const _PriceItem({
    required this.label,
    required this.value,
    this.highlight = false,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,

      children: [

        Text(
          label,
          style: const TextStyle(
            fontSize: 12,
            color: Colors.grey,
          ),
        ),

        const SizedBox(height: 5),

        Text(
          value,
          style: TextStyle(
            fontSize: 18,
            fontWeight: FontWeight.bold,
            color: highlight
                ? Theme.of(context).colorScheme.primary
                : Colors.black87,
          ),
        ),
      ],
    );
  }
}

class _TimeItem extends StatelessWidget {
  final IconData icon;
  final String label;
  final String value;

  const _TimeItem({
    required this.icon,
    required this.label,
    required this.value,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [

        Icon(
          icon,
          size: 20,
          color: Colors.grey,
        ),

        const SizedBox(width: 8),

        Column(
          crossAxisAlignment: CrossAxisAlignment.start,

          children: [

            Text(
              label,
              style: const TextStyle(
                fontSize: 11,
                color: Colors.grey,
              ),
            ),

            const SizedBox(height: 2),

            Text(
              value,
              style: const TextStyle(
                fontSize: 13,
                fontWeight: FontWeight.w600,
              ),
            ),
          ],
        ),
      ],
    );
  }
}
