import 'package:dio/dio.dart';

class ApiService {
  // Use 10.0.2.2 for Android Emulator connecting to local host.
  // For web or linux, localhost is fine.
  static const String baseUrl = 'http://127.0.0.1:8000';
  final Dio _dio = Dio(BaseOptions(baseUrl: baseUrl));

  String? _token;

  void setToken(String token) {
    _token = token;
    _dio.options.headers['Authorization'] = 'Bearer $_token';
  }

  Future<Map<String, dynamic>> login(String email, String password) async {
    final response = await _dio.post(
      '/token',
      data: FormData.fromMap({
        'username': email,
        'password': password,
      }),
    );
    return response.data;
  }

  Future<Map<String, dynamic>> register(String email, String fullName, String password) async {
    final response = await _dio.post(
      '/register',
      data: {
        'email': email,
        'full_name': fullName,
        'password': password,
      },
    );
    return response.data;
  }

  Future<List<dynamic>> getListings({String? search, String? category}) async {
    final Map<String, dynamic> queryParams = {};
    if (search != null) queryParams['search'] = search;
    if (category != null) queryParams['category'] = category;

    final response = await _dio.get('/listings', queryParameters: queryParams);
    return response.data;
  }

  Future<Map<String, dynamic>> createListing(Map<String, dynamic> data) async {
    final response = await _dio.post('/listings', data: data);
    return response.data;
  }

  Future<Map<String, dynamic>> createBooking(int listingId, DateTime start, DateTime end) async {
    final response = await _dio.post('/bookings', data: {
      'listing_id': listingId,
      'start_date': start.toIso8601String(),
      'end_date': end.toIso8601String()
    });
    return response.data;
  }

  Future<Map<String, dynamic>> payForBooking(int bookingId, double amount) async {
    final response = await _dio.post('/bookings/$bookingId/pay', data: {
      'amount': amount,
      'provider_token': 'test_token_${DateTime.now().millisecondsSinceEpoch}'
    });
    return response.data;
  }
}
final apiService = ApiService();
