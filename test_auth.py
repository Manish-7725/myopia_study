import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('Myopia_Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Myopia_Project.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

# Check if test user exists
if User.objects.filter(username='test').exists():
    print('Test user exists')
    user = User.objects.get(username='test')
else:
    print('Creating test user...')
    user = User.objects.create_user(username='test', email='test@example.com', password='test123')
    print('Test user created')

# Generate tokens
refresh = RefreshToken.for_user(user)
tokens = {
    'refresh': str(refresh),
    'access': str(refresh.access_token),
}

print('Tokens generated:')
print(f'Access: {tokens["access"]}')
print(f'Refresh: {tokens["refresh"]}')

# Test the API
import requests

url = 'http://127.0.0.1:8000/api/forms/submit-student/'
headers = {'Authorization': f'Bearer {tokens["access"]}'}
data = {
    'visit_date': '2024-01-01',
    'name': 'Test Student',
    'age': 10,
    'gender': 'Male',
    'school_name': 'Test School',
    'lifestyle': {},
    'environment': {},
    'history': {},
    'awareness': {},
    'ocular': {}
}

try:
    response = requests.post(url, json=data, headers=headers)
    print(f'Status Code: {response.status_code}')
    print(f'Response: {response.text}')
except Exception as e:
    print(f'Error: {e}')
