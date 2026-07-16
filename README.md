# Smart Campus Hostel Grievance Redressal System

An AI-powered web-based grievance management system designed for smart campus environments. This platform helps students submit hostel-related complaints, automatically analyzes complaints using Artificial Intelligence, detects priority levels, and enables administrators and staff to efficiently manage and resolve issues.

## Project Objective

The main objective of this project is to build a smart grievance redressal platform that reduces manual complaint handling. The system uses AI to categorize complaints, identify urgency, generate summaries, and improve the communication between students, staff, and administrators.

## Features

- Student complaint submission
- AI-based complaint categorization
- Automatic priority detection (Low, Medium, High)
- AI-generated complaint summary
- Student, Staff, and Admin role-based access
- Complaint status tracking
- Staff assignment for complaint resolution
- Feedback system after resolution
- Admin dashboard for monitoring complaints
- Complaint analytics and management

## AI Integration

The system integrates Google Gemini AI to analyze submitted complaints and generate useful insights:

- Complaint category detection:
  - Electrical
  - Plumbing
  - Internet
  - Cleanliness
  - Food
  - Maintenance
  - Other

- Priority identification:
  - Low
  - Medium
  - High

- Automatic complaint summary generation

## Technology Stack

### Frontend
- HTML
- CSS
- Bootstrap
- Jinja2 Templates

### Backend
- Python
- Flask

### Database
- SQLite / PostgreSQL

### AI Technology
- Google Gemini API

### Tools Used
- VS Code
- GitHub
- Postman

## Project Structure

```

grievance-system/
│
├── app.py
├── config.py
├── models/
├── routes/
├── services/
├── templates/
├── static/
├── requirements.txt
└── README.md

```

## How to Run the Project

### 1. Clone the Repository

```

git clone <repository-url>

```

### 2. Install Required Dependencies

```

pip install -r requirements.txt

```

### 3. Configure Environment Variables

Create a `.env` file and add required API keys and configuration details.

### 4. Run the Application

```

python app.py

```

### 5. Open in Browser

```

[http://127.0.0.1:5000/](http://127.0.0.1:5000/)

```

## System Roles

### Student
- Register and login
- Submit complaints
- Track complaint status
- Provide feedback after resolution

### Staff
- View assigned complaints
- Update complaint progress
- Mark issues as resolved

### Admin
- Manage users
- Assign complaints to staff
- Monitor complaints
- View analytics

## Future Enhancements

- Mobile application support
- Email and SMS notifications
- Image-based complaint analysis
- Cloud deployment
- Advanced analytics and reporting

## Author

Vaishnavi Shetty


