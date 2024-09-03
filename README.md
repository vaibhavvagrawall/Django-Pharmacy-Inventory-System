# Pharmacy Management System

## Project Overview
The Pharmacy Management System is a web application designed to streamline pharmacy operations, including inventory management, user profiles, and item tracking. Developed using Django, Bootstrap, and PostgreSQL (via Supabase), this project offers a comprehensive solution for managing pharmacy inventory with an intuitive and responsive user interface.

## Technologies Used
- **Django**: A high-level Python web framework used for building the backend of the application.
- **Bootstrap**: A front-end framework used for designing responsive and visually appealing UI components.
- **PostgreSQL**: A powerful open-source database management system used for storing and managing application data, accessed through Supabase.
- **Supabase**: An open-source platform providing PostgreSQL database as a service.
- **Crispy Forms**: A Django package used for enhancing form rendering and styling.

## Features
- **User Authentication**: Registration, login, logout, and password management.
- **Profile Management**: Update profile details and manage account settings.
- **Inventory Management**: Add, edit, and view pharmacy items and categories.
- **Alerts**: Notifications for low stock and other updates.
- **Responsive Design**: Mobile-friendly and responsive across various devices.

## Project Structure
- **pharmacy/**: Contains the main application code.
  - `models.py`: Defines the data models for the application, including pharmacy items and user profiles.
  - **views/**: Contains view logic.
    - `auth.py`: Handles authentication and user-related views.
    - `forms.py`: Contains form classes for user input handling.
  - **templates/**: HTML templates for rendering pages.
  - **static/**: CSS, JavaScript, and other static files.
  - `urls.py`: Defines URL routing for the application.
  - `settings.py`: Configuration settings for the Django application, including database settings for PostgreSQL via Supabase.

## Virtual Environment
The project uses a virtual environment located inside the Pharmacy directory:
- **Pharmacy**: Project root directory.
- **pharma_env**: Virtual Environment.
- **Pharmacy_app**: Django App.

## Live Demo
[Pharmacy Management System - Live Demo](https://django-pharmacy-inventory-system.vercel.app/)

