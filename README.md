# MAKE WORK FLOW Technical Task

Full-stack application built with FastAPI, React, TypeScript, PostgreSQL, and Docker.

## Run the Project

### Prerequisites

Make sure the following is installed and running:

- Docker Desktop
- Docker Compose

No local Python, Node.js, PostgreSQL, or package installation is required.

### 1. Clone the Repository

```bash

git clone <REPOSITORY_URL>

cd make-work-flow-technical-task

```

### 2. Start the Application

From the project root, run:

```bash

docker compose up --build

```

This will automatically:

- Start the PostgreSQL database
- Wait until PostgreSQL is healthy
- Run the Alembic database migrations
- Start the FastAPI backend
- Start the React frontend

No additional setup is required.

### 3. Open the Application

Once all containers are running, open:

Frontend:

```text

[http://localhost:5173](http://localhost:5173)

```

FastAPI Swagger documentation:

```text

[http://localhost:8000/docs](http://localhost:8000/docs)

```

Backend health check:

```text

[http://localhost:8000/health](http://localhost:8000/health)

```

### 4. Stop the Application

Press `Ctrl + C` in the terminal running Docker Compose.

Then run:

```bash

docker compose down

```

### Reset the Database

PostgreSQL data is persisted in a Docker volume.

To stop the application and completely remove the database data:

```bash

docker compose down -v

```

Then start the application again:

```bash

docker compose up --build

```

## Application Usage

From the frontend, users can:

- Create a user
- Fetch users
- Edit a user
- Delete a user

The frontend communicates with the FastAPI backend, and user data is stored in PostgreSQL.