import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models/auction.dart';
import 'models/user.dart';

/// A single row in the live search results — an auction paired with its
/// seller's username, built locally from the auctions + users lists so
/// filtering needs no extra network round-trip per keystroke.
class _SearchResult {
  final String auctionTitle;
  final String sellerUsername;
  final double currentPrice;

  const _SearchResult({
    required this.auctionTitle,
    required this.sellerUsername,
    required this.currentPrice,
  });
}

class Analytics extends StatefulWidget {
  const Analytics({super.key});

  @override
  State<Analytics> createState() => _AnalyticsState();
}

class _AnalyticsState extends State<Analytics> {
  final ApiService apiService = ApiService();
  final searchController = TextEditingController();

  /// The `data` object from GET /analytics/api/, i.e.
  /// { users, auctions, seller_analytics, auction_analytics }.
  Map<String, dynamic>? analyticsData;

  List<_SearchResult> searchIndex = [];
  List<_SearchResult> filteredResults = [];

  bool isLoading = true;
  String? error;

  @override
  void initState() {
    super.initState();
    searchController.addListener(_onSearchChanged);
    loadAnalytics();
  }

  @override
  void dispose() {
    searchController.removeListener(_onSearchChanged);
    searchController.dispose();
    super.dispose();
  }

  void _onSearchChanged() {
    final query = searchController.text.trim().toLowerCase();

    setState(() {
      filteredResults = query.isEmpty
          ? []
          : searchIndex
              .where(
                (r) =>
                    r.auctionTitle.toLowerCase().contains(query) ||
                    r.sellerUsername.toLowerCase().contains(query),
              )
              .toList();
    });
  }

  Future<void> loadAnalytics() async {
    setState(() {
      isLoading = true;
      error = null;
    });

    try {
      final futures = <Future<dynamic>>[
        apiService.getAnalytics(),
        apiService.getAuctions(),
        apiService.getUsers(),
      ];

      final results = await Future.wait(futures);

      final analytics = results[0] as Map<String, dynamic>;
      final auctions = results[1] as List<Auction>;
      final users = results[2] as List<User>;

      final usernameById = {for (final u in users) u.id: u.username};

      final index = auctions
          .map(
            (a) => _SearchResult(
              auctionTitle: a.title,
              sellerUsername: usernameById[a.sellerId] ?? 'Unknown seller',
              currentPrice: a.currentPrice,
            ),
          )
          .toList();

      setState(() {
        analyticsData = analytics;
        searchIndex = index;
        isLoading = false;
      });

      _onSearchChanged();
    } catch (e) {
      setState(() {
        error = e.toString();
        isLoading = false;
      });
    }
  }

  // ---- Small parsing helpers for the raw SQL-shaped analytics payload ----

  Map<String, dynamic> _section(String key) {
    final data = analyticsData;
    if (data == null) return {};
    final value = data[key];
    return value is Map<String, dynamic> ? value : {};
  }

  List<Map<String, dynamic>> _rows(Map<String, dynamic> section, String key) {
    final value = section[key];
    if (value is! List) return [];
    return value.whereType<Map<String, dynamic>>().toList();
  }

  String _asString(dynamic value) => value?.toString() ?? '-';

  double _asDouble(dynamic value) {
    if (value is num) return value.toDouble();
    return double.tryParse('$value') ?? 0.0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),

      appBar: AppBar(
        title: const Text(
          'Analytics',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
        actions: [
          IconButton(
            onPressed: loadAnalytics,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),

      body: _buildBody(),
    );
  }

  Widget _buildBody() {
    if (isLoading) {
      return const Center(child: CircularProgressIndicator());
    }

    if (error != null) {
      return _buildError();
    }

    if (analyticsData == null) {
      return const Center(child: Text('No analytics data available'));
    }

    final users = _section('users');
    final auctions = _section('auctions');
    final sellerAnalytics = _section('seller_analytics');
    final auctionAnalytics = _section('auction_analytics');

    return RefreshIndicator(
      onRefresh: loadAnalytics,
      child: SingleChildScrollView(
        physics: const AlwaysScrollableScrollPhysics(),
        padding: const EdgeInsets.all(20),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'Overview',
              style: TextStyle(fontSize: 26, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 6),
            const Text(
              'Key insights from your auction platform.',
              style: TextStyle(color: Colors.grey, fontSize: 14),
            ),

            const SizedBox(height: 20),

            _buildSearchSection(),

            const SizedBox(height: 28),

            _buildStatGrid(users, auctions),

            const SizedBox(height: 24),

            _buildTableCard(
              title: 'Users By Role',
              icon: Icons.people_outline,
              columns: const ['Role', 'Users'],
              rows: _rows(users, 'by_role')
                  .map((r) => [_asString(r['role']), _asString(r['total_users'])])
                  .toList(),
            ),

            const SizedBox(height: 16),

            _buildTableCard(
              title: 'Auction Count Per Seller',
              icon: Icons.gavel_outlined,
              columns: const ['Seller', 'Auctions'],
              rows: _rows(sellerAnalytics, 'auction_count_per_seller')
                  .map((r) => [_asString(r['username']), _asString(r['total_auctions'])])
                  .toList(),
            ),

            const SizedBox(height: 16),

            _buildTableCard(
              title: 'Sellers With Multiple Auctions',
              icon: Icons.groups_outlined,
              columns: const ['Seller', 'Auctions'],
              rows: _rows(sellerAnalytics, 'multiple_auction_sellers')
                  .map((r) => [_asString(r['username']), _asString(r['total_auctions'])])
                  .toList(),
            ),

            const SizedBox(height: 16),

            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: _buildHighlightCard(
                    title: 'Top Seller',
                    icon: Icons.emoji_events_outlined,
                    rows: _rows(sellerAnalytics, 'top_seller'),
                    primaryKey: 'username',
                    secondaryBuilder: (r) => '${_asString(r['total_auctions'])} auctions',
                  ),
                ),
                const SizedBox(width: 12),
                Expanded(
                  child: _buildHighlightCard(
                    title: 'Highest Auction',
                    icon: Icons.trending_up,
                    rows: _rows(auctionAnalytics, 'highest_auction'),
                    primaryKey: 'title',
                    primaryPrefix: '₹',
                    primaryValueKey: 'current_price',
                    secondaryBuilder: (r) => 'Seller: ${_asString(r['username'])}',
                  ),
                ),
              ],
            ),

            const SizedBox(height: 12),

            _buildHighlightCard(
              title: 'Latest Auction',
              icon: Icons.schedule_outlined,
              rows: _rows(auctionAnalytics, 'latest_auction'),
              primaryKey: 'title',
              secondaryBuilder: (r) =>
                  'Seller: ${_asString(r['username'])}  •  ${_asString(r['start_time'])}',
            ),

            const SizedBox(height: 16),

            _buildTableCard(
              title: 'Active Auctions',
              icon: Icons.bolt_outlined,
              columns: const ['Seller', 'Auction'],
              rows: _rows(auctionAnalytics, 'active_auctions')
                  .map((r) => [_asString(r['username']), _asString(r['title'])])
                  .toList(),
              emptyLabel: 'No active auctions.',
            ),

            const SizedBox(height: 16),

            _buildTableCard(
              title: 'Total Auction Value Per Seller',
              icon: Icons.currency_rupee,
              columns: const ['Seller', 'Total Value'],
              rows: _rows(sellerAnalytics, 'auction_value_per_seller')
                  .map((r) => [
                        _asString(r['username']),
                        '₹${_asDouble(r['total_auction_value']).toStringAsFixed(2)}',
                      ])
                  .toList(),
            ),

            const SizedBox(height: 16),

            _buildTableCard(
              title: 'High-Value Sellers',
              icon: Icons.stars_outlined,
              columns: const ['Seller', 'Total Value'],
              rows: _rows(sellerAnalytics, 'high_value_sellers')
                  .map((r) => [
                        _asString(r['username']),
                        '₹${_asDouble(r['total_auction_value']).toStringAsFixed(2)}',
                      ])
                  .toList(),
            ),

            const SizedBox(height: 16),

            _buildTableCard(
              title: 'Inactive Sellers',
              icon: Icons.person_off_outlined,
              columns: const ['ID', 'Username'],
              rows: _rows(sellerAnalytics, 'inactive_sellers')
                  .map((r) => [_asString(r['id']), _asString(r['username'])])
                  .toList(),
            ),

            const SizedBox(height: 24),
          ],
        ),
      ),
    );
  }

  Widget _buildSearchSection() {
    final hasQuery = searchController.text.trim().isNotEmpty;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
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
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(Icons.search, color: Theme.of(context).colorScheme.primary),
              const SizedBox(width: 10),
              const Text(
                'Search Auctions & Sellers',
                style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ],
          ),

          const SizedBox(height: 12),

          TextField(
            controller: searchController,
            decoration: InputDecoration(
              hintText: 'Search by auction title or seller username',
              prefixIcon: const Icon(Icons.travel_explore),
              suffixIcon: hasQuery
                  ? IconButton(
                      icon: const Icon(Icons.close),
                      onPressed: searchController.clear,
                    )
                  : null,
              filled: true,
              fillColor: const Color(0xFFF5F7FA),
              border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(14),
                borderSide: BorderSide.none,
              ),
            ),
          ),

          if (hasQuery) ...[
            const SizedBox(height: 14),
            if (filteredResults.isEmpty)
              const Padding(
                padding: EdgeInsets.symmetric(vertical: 12),
                child: Text(
                  'No matching auctions or sellers.',
                  style: TextStyle(color: Colors.grey),
                ),
              )
            else
              ...filteredResults.map(
                (r) => Padding(
                  padding: const EdgeInsets.symmetric(vertical: 8),
                  child: Row(
                    children: [
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              r.auctionTitle,
                              style: const TextStyle(fontWeight: FontWeight.w600),
                            ),
                            const SizedBox(height: 2),
                            Text(
                              'Seller: ${r.sellerUsername}',
                              style: const TextStyle(fontSize: 12, color: Colors.grey),
                            ),
                          ],
                        ),
                      ),
                      Text(
                        '₹${r.currentPrice.toStringAsFixed(2)}',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                    ],
                  ),
                ),
              ),
          ],
        ],
      ),
    );
  }

  Widget _buildStatGrid(Map<String, dynamic> users, Map<String, dynamic> auctions) {
    final stats = <(String, String, IconData)>[
      ('Total Users', _asString(users['total']), Icons.people_outline),
      ('Buyers', _asString(users['buyers']), Icons.shopping_bag_outlined),
      ('Sellers', _asString(users['sellers']), Icons.storefront_outlined),
      ('Total Auctions', _asString(auctions['total']), Icons.gavel_outlined),
      ('Active Auctions', _asString(auctions['active']), Icons.bolt_outlined),
      (
        'Total Value',
        '₹${_asDouble(auctions['total_value']).toStringAsFixed(2)}',
        Icons.currency_rupee,
      ),
    ];

    return GridView.builder(
      shrinkWrap: true,
      physics: const NeverScrollableScrollPhysics(),
      itemCount: stats.length,
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.5,
      ),
      itemBuilder: (context, index) {
        final (title, value, icon) = stats[index];
        return _MetricCard(title: title, value: value, icon: icon);
      },
    );
  }

  Widget _buildTableCard({
    required String title,
    required IconData icon,
    required List<String> columns,
    required List<List<String>> rows,
    String emptyLabel = 'No records found.',
  }) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(20),
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
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Container(
                padding: const EdgeInsets.all(10),
                decoration: BoxDecoration(
                  color: Theme.of(context).colorScheme.primary.withOpacity(0.1),
                  borderRadius: BorderRadius.circular(10),
                ),
                child: Icon(icon, color: Theme.of(context).colorScheme.primary),
              ),
              const SizedBox(width: 12),
              Text(
                title,
                style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
              ),
            ],
          ),

          const SizedBox(height: 16),

          if (rows.isEmpty)
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 8),
              child: Text(emptyLabel, style: const TextStyle(color: Colors.grey)),
            )
          else ...[
            Row(
              children: [
                Expanded(
                  child: Text(
                    columns[0],
                    style: const TextStyle(
                      fontSize: 12,
                      color: Colors.grey,
                      fontWeight: FontWeight.w600,
                    ),
                  ),
                ),
                Text(
                  columns[1],
                  style: const TextStyle(
                    fontSize: 12,
                    color: Colors.grey,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ],
            ),
            const Divider(height: 20),
            ...rows.map(
              (row) => Padding(
                padding: const EdgeInsets.symmetric(vertical: 8),
                child: Row(
                  children: [
                    Expanded(
                      child: Text(row[0], style: const TextStyle(fontWeight: FontWeight.w500)),
                    ),
                    Text(row[1], style: const TextStyle(fontWeight: FontWeight.w600)),
                  ],
                ),
              ),
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildHighlightCard({
    required String title,
    required IconData icon,
    required List<Map<String, dynamic>> rows,
    required String primaryKey,
    required String Function(Map<String, dynamic>) secondaryBuilder,
    String? primaryPrefix,
    String? primaryValueKey,
  }) {
    final row = rows.isNotEmpty ? rows.first : null;

    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(18),
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
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            children: [
              Icon(icon, size: 18, color: Colors.grey),
              const SizedBox(width: 8),
              Text(
                title,
                style: const TextStyle(fontSize: 13, color: Colors.grey, fontWeight: FontWeight.w600),
              ),
            ],
          ),

          const SizedBox(height: 10),

          if (row == null)
            const Text('No data available', style: TextStyle(color: Colors.grey))
          else ...[
            Text(
              primaryValueKey != null
                  ? '${primaryPrefix ?? ''}${_asDouble(row[primaryValueKey]).toStringAsFixed(2)}'
                  : _asString(row[primaryKey]),
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            if (primaryValueKey != null) ...[
              const SizedBox(height: 2),
              Text(
                _asString(row[primaryKey]),
                style: const TextStyle(fontSize: 14, fontWeight: FontWeight.w600),
              ),
            ],
            const SizedBox(height: 4),
            Text(
              secondaryBuilder(row),
              style: const TextStyle(fontSize: 13, color: Colors.grey),
            ),
          ],
        ],
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
            const Icon(Icons.analytics_outlined, size: 70, color: Colors.redAccent),
            const SizedBox(height: 20),
            const Text(
              'Unable to load analytics',
              style: TextStyle(fontSize: 20, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 10),
            Text(
              error!,
              textAlign: TextAlign.center,
              style: const TextStyle(color: Colors.grey),
            ),
            const SizedBox(height: 20),
            ElevatedButton.icon(
              onPressed: loadAnalytics,
              icon: const Icon(Icons.refresh),
              label: const Text('Try Again'),
            ),
          ],
        ),
      ),
    );
  }
}

class _MetricCard extends StatelessWidget {
  final String title;
  final String value;
  final IconData icon;

  const _MetricCard({
    required this.title,
    required this.value,
    required this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(18),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withOpacity(0.04),
            blurRadius: 10,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Icon(icon, color: Theme.of(context).colorScheme.primary, size: 24),
          const Spacer(),
          Text(
            value,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 4),
          Text(
            title,
            maxLines: 1,
            overflow: TextOverflow.ellipsis,
            style: const TextStyle(fontSize: 12, color: Colors.grey),
          ),
        ],
      ),
    );
  }
}
