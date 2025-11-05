🪄 DreamScape – Event Management System
📖 About the Project

DreamScape is a Django-based Event Management System designed to simplify the process of planning and managing events such as weddings, engagements, parties, and corporate gatherings.
It allows users to browse events, book services, make payments, and manage bookings — all through an elegant and responsive web interface.

Admins can monitor bookings, manage users, view statistics, and generate reports through a fully functional dashboard.

✨ Key Features
👥 User Side

Browse and view event packages (weddings, parties, engagements, etc.)

Book events with details and preferences

Multiple payment options (💳 Card, 💸 UPI, 🏦 Net Banking, 🅿️ Paytm)

Booking confirmation with email notification

Contact form to send inquiries

🧑‍💼 Admin Side (Dashboard)

Dynamic dashboard with charts and analytics

Stats cards showing users, bookings, events, and total revenue

Bookings table (view, update, delete)

Notifications dropdown

Exportable reports (CSV/Excel)

Dark Mode and responsive UI

Profile management and sidebar navigation

🧩 Tech Stack
Category	Technologies Used
Frontend	HTML5, CSS3, Bootstrap, JavaScript
Backend	Django (Python)
Database	SQLite / MySQL
Charts	Chart.js / Recharts
Payments	Paytm Integration (Demo)
Admin Dashboard	Custom Django templates + dynamic data rendering
🛠️ Installation & Setup
1. Clone the repository
git clone https://github.com/<your-username>/DreamScape.git
cd DreamScape

2. Create and activate a virtual environment
python -m venv env
env\Scripts\activate     # On Windows
source env/bin/activate  # On macOS/Linux

3. Install dependencies
pip install -r requirements.txt

4. Apply migrations
python manage.py makemigrations
python manage.py migrate

5. Create a superuser
python manage.py createsuperuser

6. Run the development server
python manage.py runserver


Then open your browser at http://127.0.0.1:8000/
 🎉

📊 Dashboard Preview (Admin Panel)

Add your screenshots here (after running the project):

/DreamScape/static/screenshots/dashboard.png
/DreamScape/static/screenshots/bookings.png


Example section:

![Dashboard Screenshot](static/screenshots/dashboard.png)
![Bookings Page](static/screenshots/bookings.png)

🧠 Project Structure
event_project/
│
├── DreamScape/
│   ├── templates/
│   ├── static/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   └── forms.py
│
├── event_project/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── manage.py
└── requirements.txt

💰 Payment Integration

Dummy payment gateway using multiple forms:

UPI, Card, Netbanking, Paytm

Stores transaction details in Payment model

Displays a success message after payment

📬 Contact Form

Stores messages in the database

Displays submissions in the admin dashboard

Sends user confirmation message after submission

🧾 Reports & Analytics

Export data to CSV

View most booked events

Bar and pie charts for bookings and revenue stats

👩‍💻 Developed By

Saniya Shaikh
💼 Final Year Project
💌 [Add your email or LinkedIn link here]

⭐ If you like this project, don’t forget to star the repo!
