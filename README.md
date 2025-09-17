# Internet Art Tools & Applications

A Django-based user management panel with login authentication and dashboard functionality.

## Features
- **Secure Login System** (no registration required)
- **User Management Dashboard** - Create, Enable, Disable, Delete users
- **Modern UI** with responsive design
- **Production Ready** with security best practices

## Local Development

### Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Start development server
python manage.py runserver
```

Open http://127.0.0.1:8000/

## Production Deployment (EC2)

### Prerequisites
- Ubuntu EC2 instance
- Security group with HTTP (80) and SSH (22) ports open

### Quick Deploy
```bash
# Clone repository
git clone <your-repo-url>
cd internet_art_login/AI\ Mailer

# Make deploy script executable
chmod +x deploy.sh

# Run deployment
./deploy.sh
```

### Manual Setup
1. Update environment variables in `internet-art-tools.service`
2. Update domain/IP in `nginx.conf`
3. Run the deployment script
4. Your app will be available at `http://your-ec2-ip`

## Environment Variables
- `SECRET_KEY` - Django secret key
- `DEBUG` - Set to False in production
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

## Project Structure
```
AI Mailer/
├── internet_art_tools/     # Django project settings
├── users/                  # Main app
│   ├── models.py          # UserAccount model
│   ├── views.py           # Login, Dashboard, User management
│   ├── templates/         # HTML templates
│   └── static/            # CSS and static files
├── requirements.txt       # Python dependencies
├── deploy.sh             # EC2 deployment script
├── nginx.conf            # Nginx configuration
└── internet-art-tools.service  # Systemd service
```
