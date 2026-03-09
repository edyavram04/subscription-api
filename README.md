# SaaS Subscription API

A production-ready backend REST API built with Django and Django REST Framework for managing user registrations, subscription plans, and secure access control.

## Technical Stack
* Framework: Django & Django REST Framework (DRF)
* Database: PostgreSQL
* Authentication: JWT (JSON Web Tokens) via simplejwt
* Documentation: Swagger UI (OpenAPI 3.0)
* DevOps: Docker & Docker Compose, GitHub Actions (CI/CD)
* Testing: Django TestCase (Unit Testing)

## Key Features
* User Management: Secure registration and login with JWT authentication.
* Subscription Engine: Dynamic management of plans (Free, Premium) using Django ORM and Raw SQL for analytics.
* Mock Payment System: An endpoint that simulates payment processing and updates user profile status.
* Security: Environment variables integration for protecting sensitive database credentials.
* Automated Workflows: GitHub Actions pipeline to ensure code quality and system integrity on every push.
* Interactive API Documentation: Fully documented endpoints accessible via Swagger UI.

## Getting Started with Docker

To run this project locally without manually installing Python or PostgreSQL, follow these steps:

1. Clone the repository:
   ```bash
   git clone <your-repo-url>
   cd subscription-api