import 'package:flutter/material.dart';
import '../services/api_service.dart';
import 'create_listing_screen.dart';
import 'booking_screen.dart';
import 'map_screen.dart';

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  List<dynamic> _listings = [];
  bool _isLoading = true;

  @override
  void initState() {
    super.initState();
    _fetchListings();
  }

  Future<void> _fetchListings() async {
    setState(() => _isLoading = true);
    try {
      final listings = await apiService.getListings();
      setState(() {
        _listings = listings;
        _isLoading = false;
      });
    } catch (e) {
      setState(() => _isLoading = false);
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(SnackBar(content: Text('Failed to load listings')));
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('RentEase Explore'),
        actions: [
          IconButton(
            icon: const Icon(Icons.map),
            onPressed: () {
              Navigator.of(context).push(MaterialPageRoute(
                builder: (context) => MapScreen(listings: _listings),
              ));
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _fetchListings,
          )
        ],
      ),
      body: _isLoading
          ? const Center(child: CircularProgressIndicator())
          : _listings.isEmpty
              ? const Center(child: Text('No listings found. Be the first to list an item!'))
              : ListView.builder(
                  itemCount: _listings.length,
                  itemBuilder: (context, index) {
                    final item = _listings[index];
                    return Card(
                      margin: const EdgeInsets.all(8.0),
                      child: ListTile(
                        leading: const Icon(Icons.location_pin, color: Colors.teal),
                        title: Text(item['title']),
                        subtitle: Text('${item['category']} - \$${item['daily_rate']}/day\nLocation: ${item['pickup_location']}'),
                        trailing: ElevatedButton(
                          onPressed: () {
                            Navigator.of(context).push(MaterialPageRoute(
                              builder: (context) => BookingScreen(listing: item),
                            ));
                          },
                          child: const Text('Rent'),
                        ),
                      ),
                    );
                  },
                ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          Navigator.of(context).push(MaterialPageRoute(
            builder: (context) => const CreateListingScreen(),
          )).then((_) => _fetchListings());
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
