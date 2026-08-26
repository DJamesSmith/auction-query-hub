/// Mirrors `users.serializers.UserSerializer`.
/// Note: `password` is write_only on the backend and is never returned,
/// so it is intentionally not part of this model.
class User {
  final int id;
  final String username;
  final String email;
  final String role;

  const User({
    required this.id,
    required this.username,
    required this.email,
    required this.role,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: _asInt(json['id']),
      username: json['username']?.toString() ?? '',
      email: json['email']?.toString() ?? '',
      role: json['role']?.toString() ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'username': username,
      'email': email,
      'role': role,
    };
  }

  static int _asInt(dynamic value) {
    if (value is int) return value;
    return int.tryParse('$value') ?? 0;
  }
}
