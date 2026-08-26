import 'package:flutter/material.dart';
import 'api_service.dart';

class AddUser extends StatefulWidget {
  const AddUser({super.key});

  @override
  State<AddUser> createState() => _AddUserState();
}

class _AddUserState extends State<AddUser> {
  final ApiService apiService = ApiService();

  final usernameController = TextEditingController();
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  String selectedRole = 'Buyer';

  bool isCreating = false;
  bool obscurePassword = true;

  /// Per-field error messages returned by the backend, keyed by the field
  /// name as sent by Django (e.g. "username", "email", "password", "role").
  /// All validation lives on the server — this map is just where those
  /// messages land so they can be shown next to the relevant input.
  Map<String, String> fieldErrors = {};

  @override
  void dispose() {
    usernameController.dispose();
    emailController.dispose();
    passwordController.dispose();

    super.dispose();
  }

  void clearFieldError(String field) {
    if (fieldErrors.containsKey(field)) {
      setState(() {
        fieldErrors.remove(field);
      });
    }
  }

  Future<void> createUser() async {
    setState(() {
      isCreating = true;
      fieldErrors = {};
    });

    try {
      await apiService.createUser(
        username: usernameController.text.trim(),
        email: emailController.text.trim(),
        password: passwordController.text,
        role: selectedRole,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('User created successfully'),
          behavior: SnackBarBehavior.floating,
        ),
      );

      Navigator.pop(context, true);
    } on ApiException catch (e) {
      if (!mounted) return;

      setState(() {
        fieldErrors = e.fieldErrors;
      });

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(e.message),
          behavior: SnackBarBehavior.floating,
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to create user\n$e'),
          behavior: SnackBarBehavior.floating,
        ),
      );
    } finally {
      if (mounted) {
        setState(() {
          isCreating = false;
        });
      }
    }
  }

  InputDecoration inputDecoration({
    required String label,
    required IconData icon,
    String? hint,
    String? errorText,
    Widget? suffixIcon,
  }) {
    return InputDecoration(
      labelText: label,
      hintText: hint,
      errorText: errorText,
      errorMaxLines: 3,
      prefixIcon: Icon(icon),
      suffixIcon: suffixIcon,
      border: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
      ),
      enabledBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: BorderSide(
          color: Colors.grey.shade300,
        ),
      ),
      focusedBorder: OutlineInputBorder(
        borderRadius: BorderRadius.circular(14),
        borderSide: BorderSide(
          color: Theme.of(context).colorScheme.primary,
          width: 2,
        ),
      ),
      filled: true,
      fillColor: Colors.white,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF5F7FA),

      appBar: AppBar(
        title: const Text(
          'Add User',
          style: TextStyle(
            fontWeight: FontWeight.bold,
          ),
        ),
      ),

      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),

          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [

              Container(
                width: double.infinity,
                padding: const EdgeInsets.all(24),

                decoration: BoxDecoration(
                  color: Theme.of(context)
                      .colorScheme
                      .primary,
                  borderRadius: BorderRadius.circular(20),
                ),

                child: const Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [

                    Icon(
                      Icons.person_add_alt_1,
                      color: Colors.white,
                      size: 36,
                    ),

                    SizedBox(height: 16),

                    Text(
                      'Create a new user',
                      style: TextStyle(
                        color: Colors.white,
                        fontSize: 24,
                        fontWeight: FontWeight.bold,
                      ),
                    ),

                    SizedBox(height: 8),

                    Text(
                      'Add a user to the Auction Query Hub system.',
                      style: TextStyle(
                        color: Colors.white70,
                        fontSize: 14,
                        height: 1.4,
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: 28),

              const Text(
                'User Information',
                style: TextStyle(
                  fontSize: 20,
                  fontWeight: FontWeight.bold,
                ),
              ),

              const SizedBox(height: 18),

              TextField(
                controller: usernameController,
                onChanged: (_) => clearFieldError('username'),

                decoration: inputDecoration(
                  label: 'Username',
                  hint: 'Enter username',
                  icon: Icons.person_outline,
                  errorText: fieldErrors['username'],
                ),
              ),

              const SizedBox(height: 16),

              TextField(
                controller: emailController,
                onChanged: (_) => clearFieldError('email'),

                keyboardType: TextInputType.emailAddress,

                decoration: inputDecoration(
                  label: 'Email',
                  hint: 'Enter email address',
                  icon: Icons.email_outlined,
                  errorText: fieldErrors['email'],
                ),
              ),

              const SizedBox(height: 16),

              TextField(
                controller: passwordController,
                onChanged: (_) => clearFieldError('password'),

                obscureText: obscurePassword,

                decoration: inputDecoration(
                  label: 'Password',
                  hint: 'Enter password',
                  icon: Icons.lock_outline,
                  errorText: fieldErrors['password'],

                  suffixIcon: IconButton(
                    icon: Icon(
                      obscurePassword
                          ? Icons.visibility_outlined
                          : Icons.visibility_off_outlined,
                    ),

                    onPressed: () {
                      setState(() {
                        obscurePassword = !obscurePassword;
                      });
                    },
                  ),
                ),
              ),

              const SizedBox(height: 16),

              DropdownButtonFormField<String>(
                value: selectedRole,

                decoration: inputDecoration(
                  label: 'Role',
                  icon: Icons.badge_outlined,
                  errorText: fieldErrors['role'],
                ),

                items: const [
                  DropdownMenuItem(
                    value: 'Buyer',
                    child: Text('Buyer'),
                  ),
                  DropdownMenuItem(
                    value: 'Seller',
                    child: Text('Seller'),
                  ),
                  DropdownMenuItem(
                    value: 'Admin',
                    child: Text('Admin'),
                  ),
                ],

                onChanged: (value) {
                  if (value == null) return;

                  setState(() {
                    selectedRole = value;
                  });
                  clearFieldError('role');
                },
              ),

              const SizedBox(height: 32),

              SizedBox(
                width: double.infinity,
                height: 54,

                child: ElevatedButton.icon(
                  onPressed: isCreating ? null : createUser,

                  icon: isCreating
                      ? const SizedBox(
                          width: 20,
                          height: 20,
                          child: CircularProgressIndicator(
                            strokeWidth: 2,
                          ),
                        )
                      : const Icon(Icons.person_add),

                  label: Text(
                    isCreating
                        ? 'Creating User...'
                        : 'Create User',
                  ),

                  style: ElevatedButton.styleFrom(
                    shape: RoundedRectangleBorder(
                      borderRadius: BorderRadius.circular(14),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}