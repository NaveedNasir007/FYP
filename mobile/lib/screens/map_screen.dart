import 'package:flutter/material.dart';
import 'package:flutter_map/flutter_map.dart';
import 'package:latlong2/latlong.dart';

class MapScreen extends StatelessWidget {
  final List<dynamic> listings;
  const MapScreen({super.key, required this.listings});

  @override
  Widget build(BuildContext context) {
    // Defaulting to Gujrat center for the demo
    final center = const LatLng(32.5711, 74.0713);

    return Scaffold(
      appBar: AppBar(title: const Text('Discover Nearby')),
      body: FlutterMap(
        options: MapOptions(
          initialCenter: center,
          initialZoom: 13.0,
        ),
        children: [
          TileLayer(
            urlTemplate: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png',
            userAgentPackageName: 'com.example.rentease',
          ),
          MarkerLayer(
            markers: listings.map((item) {
              // Note: Since we are using mock text locations like "Gujrat City" in this sandbox,
              // we mock a random coordinate near the center for visual map purposes.
              // In production with PostGIS, backend will return exact lat/long.
              final lat = 32.5711 + (item['id'] * 0.002);
              final lng = 74.0713 + (item['id'] * 0.002);
              return Marker(
                point: LatLng(lat, lng),
                width: 40,
                height: 40,
                child: const Icon(
                  Icons.location_on,
                  color: Colors.red,
                  size: 40,
                ),
              );
            }).toList().cast<Marker>(),
          ),
        ],
      ),
    );
  }
}
