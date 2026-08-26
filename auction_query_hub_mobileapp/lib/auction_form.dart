import 'package:flutter/material.dart';
import 'api_service.dart';
import 'models/user.dart';

class AuctionForm extends StatefulWidget {
  const AuctionForm({super.key});

  @override
  State<AuctionForm> createState() => _AuctionFormState();
}

class _AuctionFormState extends State<AuctionForm> {
  final ApiService apiService = ApiService();

  final titleController = TextEditingController();
  final descriptionController = TextEditingController();
  final basePriceController = TextEditingController();
  final currentPriceController = TextEditingController();

  /// Only users with role == "Seller" — this is who the auction form's
  /// dropdown should offer, since AuctionSerializer.validate_seller()
  /// rejects any non-seller on the backend.
  List<User> sellers = [];

  int? selectedSellerId;

  TimeOfDay? selectedStartTime;
  TimeOfDay? selectedEndTime;

  bool isLoadingUsers = true;
  bool isCreating = false;

  /// Per-field error messages returned by the backend, keyed by the field
  /// name as sent by Django (e.g. "title", "base_price", "seller",
  /// "start_time"). All validation lives on the server.
  Map<String, String> fieldErrors = {};

  @override
  void initState() {
    super.initState();
    loadSellers();
  }

  @override
  void dispose() {
    titleController.dispose();
    descriptionController.dispose();
    basePriceController.dispose();
    currentPriceController.dispose();
    super.dispose();
  }

  void clearFieldError(String field) {
    if (fieldErrors.containsKey(field)) {
      setState(() {
        fieldErrors.remove(field);
      });
    }
  }

  Future<void> loadSellers() async {
    try {
      // There's no seller-only endpoint on the backend, so fetch all
      // users and filter to sellers client-side.
      final result = await apiService.getUsers();
      final sellerOnly = result.where((user) => user.role == 'Seller').toList();

      setState(() {
        sellers = sellerOnly;
        isLoadingUsers = false;
      });
    } catch (e) {
      setState(() {
        isLoadingUsers = false;
      });

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to load sellers: $e'),
        ),
      );
    }
  }

  Future<void> selectStartTime() async {
    final time = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );

    if (time != null) {
      setState(() {
        selectedStartTime = time;
      });
      clearFieldError('start_time');
    }
  }

  Future<void> selectEndTime() async {
    final time = await showTimePicker(
      context: context,
      initialTime: TimeOfDay.now(),
    );

    if (time != null) {
      setState(() {
        selectedEndTime = time;
      });
      clearFieldError('end_time');
    }
  }

  String formatTime(TimeOfDay time) {
    final hour = time.hour.toString().padLeft(2, '0');
    final minute = time.minute.toString().padLeft(2, '0');

    return '$hour:$minute:00';
  }

  Future<void> createAuction() async {
    setState(() {
      isCreating = true;
      fieldErrors = {};
    });

    try {
      await apiService.createAuction(
        title: titleController.text.trim(),
        description: descriptionController.text.trim(),
        // If parsing fails (blank/invalid input) fall back to 0 so the
        // request still goes out and the backend's own "must be greater
        // than zero" validation message comes back for that field.
        basePrice: double.tryParse(basePriceController.text.trim()) ?? 0,
        currentPrice: double.tryParse(currentPriceController.text.trim()) ?? 0,
        // Same idea: an unset time is sent as an empty string so the
        // backend's "wrong format" message is what the user sees.
        startTime: selectedStartTime != null ? formatTime(selectedStartTime!) : '',
        endTime: selectedEndTime != null ? formatTime(selectedEndTime!) : '',
        // An unset seller is sent as 0 so the backend's "Invalid pk"
        // message is what the user sees.
        sellerId: selectedSellerId ?? 0,
      );

      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Auction created successfully'),
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
        ),
      );
    } catch (e) {
      if (!mounted) return;

      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Failed to create auction: $e'),
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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Create Auction'),
      ),

      body: SingleChildScrollView(
        padding: const EdgeInsets.all(20),

        child: Column(
          children: [

            TextField(
              controller: titleController,
              onChanged: (_) => clearFieldError('title'),
              decoration: InputDecoration(
                labelText: 'Auction Title',
                errorText: fieldErrors['title'],
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller: descriptionController,
              onChanged: (_) => clearFieldError('description'),
              maxLines: 3,
              decoration: InputDecoration(
                labelText: 'Description',
                errorText: fieldErrors['description'],
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller: basePriceController,
              onChanged: (_) => clearFieldError('base_price'),
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              decoration: InputDecoration(
                labelText: 'Base Price',
                errorText: fieldErrors['base_price'],
              ),
            ),

            const SizedBox(height: 16),

            TextField(
              controller: currentPriceController,
              onChanged: (_) => clearFieldError('current_price'),
              keyboardType: const TextInputType.numberWithOptions(decimal: true),
              decoration: InputDecoration(
                labelText: 'Current Price',
                errorText: fieldErrors['current_price'],
              ),
            ),

            const SizedBox(height: 16),

            isLoadingUsers
                ? const CircularProgressIndicator()
                : sellers.isEmpty
                    ? const Text(
                        'No sellers available. Add a user with the Seller role first.',
                        style: TextStyle(color: Colors.grey),
                      )
                    : DropdownButtonFormField<int>(
                        value: selectedSellerId,

                        decoration: InputDecoration(
                          labelText: 'Select Seller',
                          errorText: fieldErrors['seller'],
                        ),

                        items: sellers.map<DropdownMenuItem<int>>((seller) {
                          return DropdownMenuItem<int>(
                            value: seller.id,
                            child: Text(seller.username),
                          );
                        }).toList(),

                        onChanged: (value) {
                          setState(() {
                            selectedSellerId = value;
                          });
                          clearFieldError('seller');
                        },
                      ),

            const SizedBox(height: 20),

            ListTile(
              title: const Text('Start Time'),
              subtitle: Text(
                selectedStartTime == null
                    ? 'Select start time'
                    : selectedStartTime!.format(context),
              ),
              trailing: const Icon(Icons.access_time),
              onTap: selectStartTime,
            ),
            if (fieldErrors['start_time'] != null)
              Padding(
                padding: const EdgeInsets.only(left: 16, bottom: 8),
                child: Text(
                  fieldErrors['start_time']!,
                  style: TextStyle(
                    color: Theme.of(context).colorScheme.error,
                    fontSize: 12,
                  ),
                ),
              ),

            ListTile(
              title: const Text('End Time'),
              subtitle: Text(
                selectedEndTime == null
                    ? 'Select end time'
                    : selectedEndTime!.format(context),
              ),
              trailing: const Icon(Icons.access_time),
              onTap: selectEndTime,
            ),
            if (fieldErrors['end_time'] != null)
              Padding(
                padding: const EdgeInsets.only(left: 16, bottom: 8),
                child: Text(
                  fieldErrors['end_time']!,
                  style: TextStyle(
                    color: Theme.of(context).colorScheme.error,
                    fontSize: 12,
                  ),
                ),
              ),

            const SizedBox(height: 30),

            SizedBox(
              width: double.infinity,

              child: ElevatedButton(
                onPressed: isCreating ? null : createAuction,

                child: isCreating
                    ? const SizedBox(
                        height: 20,
                        width: 20,
                        child: CircularProgressIndicator(strokeWidth: 2),
                      )
                    : const Text('Create Auction'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}