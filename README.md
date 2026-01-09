# Myopia Study Portal

A comprehensive web application for managing myopia research studies, built with Django REST Framework backend and modern HTML/CSS/JavaScript frontend.

## Features

- **User Management**: Registration, authentication, and role-based access (Admin, Clinician, Student)
- **Clinical Data Collection**: Structured forms for collecting myopia progression data
- **Dashboard Analytics**: Real-time insights and data visualization
- **Student Management**: Track and manage study participants
- **Form Validation**: Client-side and server-side validation for data integrity
- **Responsive Design**: Mobile-friendly interface using Bootstrap 5

## Tech Stack

### Backend
- **Django 4.x** - Web framework
- **Django REST Framework** - API development
- **Simple JWT** - Token-based authentication
- **SQLite/PostgreSQL** - Database
- **Django CORS Headers** - Cross-origin resource sharing

### Frontend
- **HTML5/CSS3** - Structure and styling
- **Bootstrap 5** - UI framework
- **JavaScript (ES6+)** - Client-side logic
- **Font Awesome/Bootstrap Icons** - Icon library

## Quick Start

### Prerequisites
- Python 3.8+
- Node.js (for package management, optional)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Myopia_Analysis
   ```

2. **Set up Python virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start the Django development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Frontend: Open `frontend/login.html` in your browser
   - Admin panel: http://127.0.0.1:8000/admin/
   - API endpoints: http://127.0.0.1:8000/api/

## Project Structure

```
Myopia_Analysis/
├── Myopia_Project/          # Django project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── Myopia_Study/            # Main Django app
│   ├── models.py            # Database models
│   ├── views.py             # API views
│   ├── serializers.py       # Data serialization
│   ├── authentication.py    # Custom JWT auth
│   └── api_urls.py          # API routing
├── frontend/                # Frontend assets
│   ├── *.html               # Page templates
│   ├── static/
│   │   ├── css/             # Stylesheets
│   │   └── js/              # JavaScript files
│   └── login.html           # Entry point
├── manage.py                # Django management script
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## API Endpoints

### Authentication
- `POST /api/login/` - User login
- `POST /api/signup/` - User registration
- `POST /api/logout/` - User logout

### Students
- `GET /api/students/` - List all students
- `POST /api/students/` - Create new student
- `GET /api/students/{id}/` - Get student details
- `PUT /api/students/{id}/` - Update student
- `DELETE /api/students/{id}/` - Delete student

### Forms & Reports
- `GET /api/forms/` - List submitted forms
- `POST /api/forms/` - Submit new form
- `GET /api/forms/{id}/` - Get form details

## Usage Guide

### For Administrators
1. Log in with admin credentials
2. Access the dashboard to view study progress
3. Manage users and students
4. Review and validate submitted forms
5. Export data for analysis

### For Clinicians
1. Register/Login to the system
2. Access patient management
3. Fill out clinical assessment forms
4. View follow-up schedules

### For Students/Parents
1. Register/Login to the system
2. Complete lifestyle questionnaires
3. View personal health data
4. Schedule follow-up appointments

## Development

### Running Tests
```bash
python manage.py test
```

### Code Style
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings to functions and classes
- Keep functions small and focused

### Frontend Development
- Place HTML files in `frontend/` directory
- CSS files in `frontend/static/css/`
- JavaScript files in `frontend/static/js/`
- Use Bootstrap classes for consistent styling

## Deployment

### Environment Variables
Create a `.env` file in the project root:
```
DEBUG=False
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://user:password@localhost:5432/myopia_db
ALLOWED_HOSTS=your-domain.com
```

### Production Server
```bash
pip install gunicorn
gunicorn Myopia_Project.wsgi:application --bind 0.0.0.0:8000
```

### Static Files
```bash
python manage.py collectstatic
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Troubleshooting

### Common Issues

**API Connection Errors**
- Ensure Django server is running on port 8000
- Check CORS settings in Django settings
- Verify API_BASE_URL in frontend JavaScript

**Database Errors**
- Run migrations: `python manage.py migrate`
- Check database configuration in settings.py

**Static Files Not Loading**
- Run `python manage.py collectstatic`
- Check STATIC_URL and STATIC_ROOT settings

**Authentication Issues**
- Verify JWT token validity
- Check cookie settings for token storage

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue on GitHub
- Contact the development team
- Check the documentation for common solutions

---

**Version:** 1.0.0
**Last Updated:** 2024
