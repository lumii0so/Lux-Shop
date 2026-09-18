# Lux Shop

A Telegram shopping bot built with Python, aiogram, PostgreSQL and Docker.

## Overview

Lux Shop is a Telegram based shopping bot that allows clients to browse products
catalog, order products, view orders and contact support if needed.

The project was built as a practical e-commerce bot with PostgreSQL for data
storage and Docker for deployment.

## Features

### Customer

#### Available

- Browse products
    - View product details
    - Managing products cart
- Contact support
    - Make support requests
    - View submitted requests
        - Two sided chat with admins

#### In Development

- Place orders
- View order history

### Admin

#### Available

- Admin-only panel
- Products menu
    - Add products
    - View products
        - Edit product
        - Delete product
- Support requests
    - View open requests
        - Respond to requests

#### In Development

- Products menu
    - View products
        - Product statistics
- Manage orders
- Manage users
- Support requests
    - View all requests
    - Close requests
- View statistics

## Tech Stack

| Technology | Role |
|------------|---------|
| **Python 3.14.3** | Core programming language and asynchronous application logic |
| **Aiogram 3.31.0** | Asynchronous framework for interfacing with the Telegram Bot API |
| **PostgreSQL 18** | Primary relational database for user data and persistent storage |
| **Psycopg 3.3.5** | Database driver for high-performance Python-to-PostgreSQL connectivity |
| **Docker 29.7.2** | Containerization for consistent development and deployment environments |
| **Docker Compose 5.5.0** | Service orchestration for the bot and database containers |

## Project Structure

```text
app/
├── admin/          # Admin panel handlers and keyboards
├── user/           # User interface handlers and keyboards
├── assets/         # Bot assets
├── database/       # Database connection and queries
├── config.py       # Application configuration
├── main.py         # Application entry point
└── paths.py        # Application file paths

database/
└── schema.sql      # Database initialization schema

Dockerfile
docker-compose.yml
requirements.txt
.env.example
.gitignore
.dockerignore
README.md
```

## Installation

Follow these steps to run the bot locally using Docker and Docker Compose.


### Prerequisites
Make sure you have [Docker](https://docker.com) and [Docker Compose](https://docker.com) installed.

### 1. Clone the repository:
<<<<<<< HEAD
```bash
git clone https://github.com/lumii0so/Lux-Shop.git
cd your-repo-name
```
=======
    ```bash
    git clone https://github.com/lumii0so/Lux-Shop.git
    cd your-repo-name
    ```
>>>>>>> 01dee69 (Update project to v0.2.0 - Support System Release)

### 2. Create the environment file:
    Copy `.env.example` to `.env` and fill in your actual Telegram Bot Token and database credentials.

### 3. Start the application:
   Run the following command to build the image and start both the bot and the PostgreSQL database in the background:
   ```bash
   docker compose up -d --build
   ```

### 4. Verify if it is running:
   Check the real-time container logs to ensure the bot connected to Telegram successfully:
   ```bash
   docker compose logs -f
   ```

### 5. How to Stop:
To shut down the containers while preserving your PostgreSQL database data:
```bash
docker compose down
```
