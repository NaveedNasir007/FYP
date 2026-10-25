import 'package:flutter/material.dart';
import '../services/api_service.dart';

class BookingScreen extends StatefulWidget {
  final dynamic listing;
  const BookingScreen({super.key, required this.listing});

  @override
  State<BookingScreen> createState() => _BookingScreenState();
}

class _BookingScreenState extends State<BookingScreen> {
  DateTime? _startDate;
  DateTime? _endDate;
  bool _isProcessing = false;
  Map<String, dynamic>? _bookingData;
  Map<String, dynamic>? _paymentData;

  void _selectDates() async {
    final picked = await showDateRangePicker(
      context: context,
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (picked != null) {
      setState(() {
        _startDate = picked.start;
        _endDate = picked.end;
      });
    }
  }

  void _bookAndPay() async {
    if (_startDate == null || _endDate == null) return;
    setState(() => _isProcessing = true);
    try {
      final booking = await apiService.createBooking(widget.listing['id'], _startDate!, _endDate!);
      setState(() {
        _bookingData = booking;
      });
      final payment = await apiService.payForBooking(booking['id'], booking['total_amount']);
      setState(() {
        _paymentData = payment;
        _isProcessing = false;
      });
      if (mounted) {
        showDialog(
          context: context,
          builder: (ctx) => AlertDialog(
            title: const Text('Success'),
            content: Text('Booking confirmed and paid in sandbox!\nTotal: \$${booking['total_amount']}'),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.of(ctx).pop(); // dialog
                  Navigator.of(context).pop(); // screen
                },
                child: const Text('OK'),
              )
            ],
          )
        );
      }
    } catch (e) {
      setState(() => _isProcessing = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Error: $e')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Book ${widget.listing['title']}')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text('Rate: \$${widget.listing['daily_rate']} / day', style: const TextStyle(fontSize: 18)),
            Text('Deposit: \$${widget.listing['deposit']}', style: const TextStyle(fontSize: 18)),
            const SizedBox(height: 20),
            Row(
              children: [
                ElevatedButton(
                  onPressed: _selectDates,
                  child: const Text('Select Dates'),
                ),
                const SizedBox(width: 10),
                if (_startDate != null && _endDate != null)
                  Text('${_startDate.toString().split(' ')[0]} to ${_endDate.toString().split(' ')[0]}'),
              ],
            ),
            const Spacer(),
            if (_isProcessing) const Center(child: CircularProgressIndicator())
            else
              SizedBox(
                width: double.infinity,
                child: ElevatedButton(
                  onPressed: (_startDate == null || _endDate == null) ? null : _bookAndPay,
                  child: const Text('Confirm & Pay (Sandbox)'),
                ),
              )
          ],
        ),
      ),
    );
  }
}
