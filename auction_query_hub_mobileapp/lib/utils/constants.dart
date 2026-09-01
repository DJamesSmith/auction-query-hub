/// Centralized API configuration.
///
/// IMPORTANT: this is the ONLY place the base URL should be defined.
/// If your Mac's LAN IP changes, update it here only.
class ApiConstants {
  ApiConstants._();

  /// Django dev server address, reachable from the Android phone over Wi-Fi.
  /// Do NOT use 127.0.0.1 / localhost here — on the phone those resolve to
  /// the phone itself, not your Mac.
  static const String baseUrl = 'http://192.168.0.105:8000';

  static const String usersEndpoint = '$baseUrl/users/api/';
  static const String createUserEndpoint = '$baseUrl/users/api/create/';
  static const String auctionsEndpoint = '$baseUrl/auctions/api/';
  static const String createAuctionEndpoint = '$baseUrl/auctions/api/create/';
  static const String analyticsEndpoint = '$baseUrl/analytics/api/';

  /// Requests hang for at most this long before failing with a timeout error.
  static const Duration requestTimeout = Duration(seconds: 15);
}
