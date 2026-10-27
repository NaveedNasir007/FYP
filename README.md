Here is how you can run and test the RentEase platform on your local machine and your phone!

1. Run the Backend API (PC)
The backend powers both the mobile app and the admin dashboard.

Open a terminal and navigate to the project directory.
Navigate to the backend folder and activate the virtual environment:
cd backend
source venv/bin/activate
(If you are on Windows, the activation command is venv\Scripts\activate)
Run the server:
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
The server is now running at http://127.0.0.1:8000.
2. Run the Admin Dashboard (PC)
The admin dashboard is a web application.

Open a new terminal window.
Navigate to the admin folder:
cd admin
Start the development server:
npm run dev
You can view the dashboard by opening your browser to http://localhost:5173.
3. Run the Mobile App (Phone or Emulator)
To test the app, you will need Flutter installed on your PC.

If testing on a PC (Android Emulator or iOS Simulator):

Ensure the emulator is running.
Open a new terminal window and navigate to the mobile folder:
cd mobile
Run the app:
flutter run
(Note: If you use the Android Emulator, the backend URL in mobile/lib/services/api_service.dart is currently set to http://127.0.0.1:8000. You might need to change it to http://10.0.2.2:8000 for the emulator to successfully communicate with your PC's localhost).

If testing on a physical Android phone:

Connect your Android phone via USB and ensure Developer Options and USB Debugging are enabled.
Find your PC's local IP address on your Wi-Fi network (e.g., 192.168.1.5).
Update mobile/lib/services/api_service.dart so the baseUrl points to your PC's IP address:
static const String baseUrl = 'http://192.168.1.5:8000';
Run the app:
cd mobile
flutter run -d <your-device-id>
4. End-to-End Testing (Automated script)
If you want to quickly verify the backend logic without the UI, you can run the integration test script on your PC:

Ensure the backend server is running in one terminal.
In a new terminal:
cd backend
source venv/bin/activate
python test_integration.py
This will automatically register a test user, create a listing, search for it, book it, and simulate a sandbox payment!
