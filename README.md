# DariaProject

A Django web application built with MongoDB integration using Djongo, featuring REST API capabilities and JWT authentication.

## Features

- **Django 5.2.1** - Modern Python web framework
- **MongoDB Integration** - Using Djongo5 for seamless Django-MongoDB connectivity
- **REST API** - Built with Django REST Framework
- **JWT Authentication** - Secure token-based authentication
- **Data Processing** - Integrated NumPy and Pandas for data analysis
- **Multi-Database Support** - MySQL client support alongside MongoDB

## Tech Stack

- **Backend**: Django 5.2.1
- **Database**: MongoDB (primary), MySQL (optional)
- **API**: Django REST Framework 3.16.0
- **Authentication**: JWT (djangorestframework-simplejwt)
- **ODM**: Djongo5 1.3.9
- **Data Processing**: NumPy, Pandas
- **Database Drivers**: PyMongo, MySQLClient

## Prerequisites

Before running this project, make sure you have:

- Python 3.8+ installed
- MongoDB server running
- MySQL server (if using MySQL features)
- pip package manager

## Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd DariaProject
```

2. **Create a virtual environment**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure MongoDB**
   
   Make sure MongoDB is running on your system. Update your `settings.py` with MongoDB configuration:
   
   ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'daria-db',
            'USER': os.getenv("MYSQL_USER"),
            'PASSWORD': os.getenv("MYSQL_PASSWORD"),
            'HOST': 'localhost',
            'PORT': '3306',
        },
        'mongo': {
                'ENGINE': 'djongo',
                'NAME': 'daria-db',
                'ENFORCE_SCHEMA': False,
                'CLIENT': {
                    'host': os.getenv("MONGO_HOST")
                }  
            }
    }
   ```

5. **Run migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```
5. **Run core commands**
```bash
python manage.py import_cross  ./data/cross.csv
python manage.py import_long  ./data/long.csv
```

6. **Create a superuser**
```bash
python manage.py createsuperuser
```

7. **Start the development server**
```bash
uvicorn daria.asgi:application --host 0.0.0.0 --port 8000 --reload
```

The application will be available at `http://localhost:8000`


## API Endpoints

The project includes REST API endpoints. Common endpoints might include:

- `GET /api/` - API root (customize based on your models)
- `POST /api/token/` - Obtain JWT token
- `POST /api/token/refresh/` - Refresh JWT token
- `GET /api/admin/users/` - Admin users list
- `POST /api/admin/users/` - Admin user create
- `PUT /api/admin/users/:id/` - Admin user update
- `PATCH /api/admin/users/:id/` - Admin user update
- `GET /api/admin/users/:id/` - Admin user detail
- `GET /api/data/` - Cross and Long data concatenation
- `GET /api/rf_result/` - XGBoost result
- `GET /api/y_result/` - Predict probability result

## Project Structure

```
DariaProject/
├── manage.py
├── docker-compose.yml
├── .env
├── requirements.txt
├── README.md
├── trainer/
│   ├── __init__.py
│   ├── config.yml
│   ├── exceptions.py
│   └── helper.py
├── data/
│   ├── cross.csv
│   └── long.csv
├── docs/
│   └── Daria.postman_collection.json
├── daria/
│   ├── __init__.py
│   ├── settings.py
│   ├── db_routers.py
│   ├── asgi.py
│   ├── urls.py
│   └── wsgi.py
├── core/
│   ├── management/
│   │   ├── __init__.py
│   |   ├── commands/
│   |   |   ├── __init__.py
│   |   |   ├── import_cross.py
│   |   |   └── import_long.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── views.py
│   │   └── urls.py
│   ├── __init__.py
│   ├── admin.py
│   ├── managers.py
│   ├── models.py
│   └── views.py
└── client/
    ├──
    ├── api/
    │   ├── __init__.py
    │   ├── views.py
    │   ├── serializers.py
    │   └── urls.py
    ├── __init__.py
    ├── admin.py
    ├── models.py
    └── views.py
```

## Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure allowed hosts
3. Set up proper MongoDB authentication
4. Use environment variables for sensitive data
5. Configure static files serving
6. Set up proper logging

## Troubleshooting

### Common Issues

1. **MongoDB Connection Error**
   - Ensure MongoDB service is running
   - Check connection string in settings.py
   - Verify database permissions

2. **Djongo Migration Issues**
   - Some Django features may not be fully compatible with MongoDB
   - Use embedded documents carefully
   - Avoid complex queries that don't translate well to MongoDB

3. **JWT Token Issues**
   - Check token expiration settings
   - Ensure proper token format in requests
   - Verify authentication middleware setup

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## Support

For support and questions, please contact m.asadnejad97@gmail.com.