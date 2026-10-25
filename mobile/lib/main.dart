import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'screens/auth_screen.dart';

void main() {
  runApp(
    const ProviderScope(
      child: RentEaseApp(),
    ),
  );
}

class RentEaseApp extends StatelessWidget {
  const RentEaseApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'RentEase',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const AuthScreen(),
    );
  }
}
