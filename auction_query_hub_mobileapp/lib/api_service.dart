import 'dart:async';
import 'dart:convert';
import 'dart:io';

import 'package:flutter/foundation.dart';
import 'package:http/http.dart' as http;

import 'models/auction.dart';
import 'models/user.dart';
import 'utils/constants.dart';

/// A clean, user-facing error.
///
/// - [message] is a short summary suitable for a SnackBar
///   (e.g. "User creation failed.").
/// - [fieldErrors] maps backend field names (e.g. "username", "seller")
///   to a single readable message for that field, so forms can show
///   errors inline next to the relevant input instead of duplicating
///   validation logic client-side.
class ApiException implements Exception {
  final String message;
  final Map<String, String> fieldErrors;

  const ApiException(this.message, {this.fieldErrors = const {}});

  @override
  String toString() => message;
}

class ApiService {
  void _log(String message) {
    // Debug-only logging — stripped out of release builds automatically.
    if (kDebugMode) {
      // ignore: avoid_print
      print('[ApiService] $message');
    }
  }

  Future<http.Response> _send(Future<http.Response> Function() request, String method, String url) async {
    _log('$method $url');
    try {
      final response = await request().timeout(ApiConstants.requestTimeout);
      _log('$method $url -> ${response.statusCode}');
      return response;
    } on TimeoutException {
      throw const ApiException(
        'The request timed out. Make sure the Django server is running and reachable.',
      );
    } on SocketException {
      throw const ApiException(
        'Unable to connect to the server.\n'
        'Make sure the Django server is running and your phone is connected to the same Wi-Fi.',
      );
    } on http.ClientException {
      throw const ApiException(
        'Unable to connect to the server.\n'
        'Make sure the Django server is running and your phone is connected to the same Wi-Fi.',
      );
    } on HandshakeException {
      throw const ApiException('A secure connection could not be established.');
    } catch (e) {
      _log('$method $url -> unexpected error: $e');
      throw const ApiException('Something went wrong while contacting the server.');
    }
  }

  /// Flattens a DRF-style error value (String, List<String>, or nested Map)
  /// into a single readable string. Used as a fallback summary message.
  String _formatErrors(dynamic errors) {
    final messages = <String>[];

    void collect(dynamic value) {
      if (value is String) {
        messages.add(value);
      } else if (value is List) {
        for (final item in value) {
          collect(item);
        }
      } else if (value is Map) {
        value.forEach((key, val) => collect(val));
      }
    }

    collect(errors);
    return messages.join('\n');
  }

  /// Converts DRF's `{"field": ["msg1", "msg2"], ...}` shape into a flat
  /// `{"field": "msg1 msg2"}` map, so UI code can look up a single string
  /// per field via `fieldErrors['field']`. Nested maps are flattened too
  /// (their messages joined), which keeps this robust even if a field's
  /// error value isn't a plain list.
  Map<String, String> _extractFieldErrors(dynamic errors) {
    final result = <String, String>{};

    if (errors is Map) {
      errors.forEach((key, value) {
        final formatted = _formatErrors(value);
        if (formatted.isNotEmpty) {
          result[key.toString()] = formatted;
        }
      });
    }

    return result;
  }

  /// Decodes the response body and translates non-2xx status codes into
  /// friendly [ApiException]s.
  dynamic _handleResponse(http.Response response) {
    final status = response.statusCode;

    if (status == 200 || status == 201) {
      if (response.body.isEmpty) return null;
      try {
        return jsonDecode(response.body);
      } catch (_) {
        throw const ApiException('The server returned an unexpected response.');
      }
    }

    // Try to surface the backend's own "message" (summary) and "errors"
    // (per-field) content when present.
    String serverMessage = '';
    Map<String, String> fieldErrors = {};

    try {
      final decoded = jsonDecode(response.body);
      if (decoded is Map) {
        if (decoded['errors'] != null) {
          fieldErrors = _extractFieldErrors(decoded['errors']);
        }

        if (decoded['message'] != null) {
          serverMessage = decoded['message'].toString();
        } else if (fieldErrors.isNotEmpty) {
          serverMessage = fieldErrors.values.join('\n');
        }
      }
    } catch (_) {
      // Body wasn't JSON — fall back to a generic message below.
    }

    switch (status) {
      case 400:
        throw ApiException(
          serverMessage.isNotEmpty ? serverMessage : 'Bad request. Please check the submitted data.',
          fieldErrors: fieldErrors,
        );
      case 401:
        throw const ApiException('You are not authorized to perform this action.');
      case 403:
        throw const ApiException('You do not have permission to perform this action.');
      case 404:
        throw const ApiException('Requested resource was not found.');
      case 500:
        throw const ApiException('Server error. Please try again later.');
      default:
        throw ApiException(
          serverMessage.isNotEmpty ? serverMessage : 'Unexpected error (HTTP $status).',
          fieldErrors: fieldErrors,
        );
    }
  }

  Future<dynamic> _get(String url) async {
    final response = await _send(() => http.get(Uri.parse(url)), 'GET', url);
    return _handleResponse(response);
  }

  Future<dynamic> _post(String url, Map<String, dynamic> body) async {
    final response = await _send(
      () => http.post(
        Uri.parse(url),
        headers: {'Content-Type': 'application/json'},
        body: jsonEncode(body),
      ),
      'POST',
      url,
    );
    return _handleResponse(response);
  }

  /// This backend always wraps list responses as
  /// `{"status", "message", "count", "data": [...]}`. Unwrap `data`,
  /// falling back to treating the payload itself as the list if the shape
  /// ever changes.
  List<dynamic> _extractList(dynamic decoded) {
    if (decoded is List) return decoded;
    if (decoded is Map && decoded['data'] is List) {
      return decoded['data'] as List<dynamic>;
    }
    return [];
  }

  Map<String, dynamic>? _extractObject(dynamic decoded) {
    if (decoded is Map && decoded['data'] is Map<String, dynamic>) {
      return decoded['data'] as Map<String, dynamic>;
    }
    if (decoded is Map<String, dynamic>) return decoded;
    return null;
  }

  // ---- Users ----

  Future<List<User>> getUsers() async {
    final decoded = await _get(ApiConstants.usersEndpoint);
    return _extractList(decoded)
        .whereType<Map<String, dynamic>>()
        .map(User.fromJson)
        .toList();
  }

  Future<User> createUser({
    required String username,
    required String email,
    required String password,
    required String role,
  }) async {
    final decoded = await _post(ApiConstants.createUserEndpoint, {
      'username': username,
      'email': email,
      'password': password,
      'role': role,
    });

    final obj = _extractObject(decoded);
    if (obj == null) {
      throw const ApiException('The server returned an unexpected response.');
    }
    return User.fromJson(obj);
  }

  // ---- Auctions ----

  Future<List<Auction>> getAuctions() async {
    final decoded = await _get(ApiConstants.auctionsEndpoint);
    return _extractList(decoded)
        .whereType<Map<String, dynamic>>()
        .map(Auction.fromJson)
        .toList();
  }

  Future<Auction> createAuction({
    required String title,
    required String description,
    required double basePrice,
    required double currentPrice,
    required String startTime,
    required String endTime,
    required int sellerId,
  }) async {
    final decoded = await _post(ApiConstants.createAuctionEndpoint, {
      'title': title,
      'description': description,
      'base_price': basePrice,
      'current_price': currentPrice,
      'start_time': startTime,
      'end_time': endTime,
      // Must be "seller" to match AuctionSerializer.Meta.fields — the
      // backend has no "seller_id" field.
      'seller': sellerId,
    });

    final obj = _extractObject(decoded);
    if (obj == null) {
      throw const ApiException('The server returned an unexpected response.');
    }
    return Auction.fromJson(obj);
  }

  // ---- Analytics ----

  /// Analytics payload shape varies a lot (many nested groupings), so it is
  /// returned as a raw map rather than a typed model.
  Future<Map<String, dynamic>> getAnalytics() async {
    final decoded = await _get(ApiConstants.analyticsEndpoint);
    return _extractObject(decoded) ?? {};
  }
}