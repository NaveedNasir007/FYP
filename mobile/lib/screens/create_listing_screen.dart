import 'package:flutter/material.dart';
import '../services/api_service.dart';

class CreateListingScreen extends StatefulWidget {
  const CreateListingScreen({super.key});

  @override
  State<CreateListingScreen> createState() => _CreateListingScreenState();
}

class _CreateListingScreenState extends State<CreateListingScreen> {
  final _formKey = GlobalKey<FormState>();
  String _title = '';
  String _description = '';
  String _category = 'Tools';
  String _condition = 'Good';
  double _dailyRate = 0.0;
  double _deposit = 0.0;
  String _pickupLocation = '';

  void _submit() async {
    if (_formKey.currentState!.validate()) {
      _formKey.currentState!.save();
      try {
        await apiService.createListing({
          'title': _title,
          'description': _description,
          'category': _category,
          'condition': _condition,
          'daily_rate': _dailyRate,
          'deposit': _deposit,
          'pickup_location': _pickupLocation,
        });
        if (mounted) {
          Navigator.of(context).pop();
        }
      } catch (e) {
        if (mounted) {
          ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to create listing: $e')));
        }
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('List an Item')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Form(
          key: _formKey,
          child: ListView(
            children: [
              TextFormField(
                decoration: const InputDecoration(labelText: 'Title'),
                onSaved: (val) => _title = val ?? '',
                validator: (val) => val == null || val.isEmpty ? 'Required' : null,
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Description'),
                maxLines: 3,
                onSaved: (val) => _description = val ?? '',
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Category (e.g. Tools, Electronics)'),
                initialValue: _category,
                onSaved: (val) => _category = val ?? '',
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Daily Rate (\$)'),
                keyboardType: TextInputType.number,
                onSaved: (val) => _dailyRate = double.tryParse(val ?? '0') ?? 0,
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Deposit (\$)'),
                keyboardType: TextInputType.number,
                onSaved: (val) => _deposit = double.tryParse(val ?? '0') ?? 0,
              ),
              TextFormField(
                decoration: const InputDecoration(labelText: 'Pickup Location'),
                onSaved: (val) => _pickupLocation = val ?? '',
              ),
              const SizedBox(height: 20),
              ElevatedButton(
                onPressed: _submit,
                child: const Text('Create Listing'),
              )
            ],
          ),
        ),
      ),
    );
  }
}
