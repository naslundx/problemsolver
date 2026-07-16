# Problem Solver

A full-stack application designed to test kids and adults on mathematical problem-solving skills. The app presents math problems and allows users to ask clarifying questions via an OpenAI-powered chat interface to gather the necessary data before attempting a solution.

## 🏗 Architecture

The project is divided into two main parts: a **Frontend** client and a **Backend** API. 

- **Frontend**: A Single Page Application (SPA) built with Vue 3, Vite, Vue Router, and Pinia for state management. Styling is handled with SCSS and FontAwesome icons.
- **Backend**: A Python Flask REST API utilizing `uv` for fast dependency management. It handles game logic, session progress, and integrates with the OpenAI API for answering user queries.
- **Database**: PostgreSQL is used to persist game sessions, uploaded questions, and the chat history between users and the AI.

### Data Flow
1. A new game session is created via the backend (`/api/game`).
2. The UI fetches the current math problem (`/api/start`), which may include text and images.
3. Users can ask questions about the problem (`/api/chat`). The backend limits the AI to only provide short facts and explicitly forbids it from doing calculations for the user.
4. The user submits their final answer (`/api/answer`). Correct answers progress the game, while incorrect answers may provide clues.

---

## 🚀 Running Locally

### Prerequisites
- [Docker](https://www.docker.com/) & Docker Compose (Recommended for local dev)
- *Alternative manual setup:* [Node.js](https://nodejs.org/), [Python 3.13+](https://www.python.org/), [uv](https://github.com/astral-sh/uv), and [PostgreSQL](https://www.postgresql.org/).

### 1. Environment Variables
Create a `.env` file in the root of the project:

```text
OPENAI_API_KEY=sk-...
# If running manually without Docker, also include:
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
```

### 2. Start the Application

The easiest way to run the application seamlessly is using Docker Compose. It will spin up the frontend, backend, and PostgreSQL database automatically.

```bash
docker compose up --build
```

### 3. Database Initialization

Once the containers are running, open a new terminal and initialize the local database (this will drop existing tables and seed the initial questions):

```bash
./reset-database.sh
```

*(This script runs `docker compose exec backend uv run python3 -c "from src.database import *; reset_database(); upload_questions()"`. It will drop existing tables!)*

---

## 🌍 Deploying to Heroku

This project is configured for automated deployment to Heroku using GitHub Actions. The application is built as a single Docker container (using `Dockerfile.heroku`) where the Flask backend also serves the compiled Vue frontend.

### 1. GitHub Secrets
To enable the CI/CD pipeline, add the following secrets to your GitHub repository (**Settings > Secrets and variables > Actions > New repository secret**):
- `HEROKU_API_KEY`: Your Heroku API key (found in your Heroku Account Settings).
- `HEROKU_APP_NAME`: The exact name of your Heroku app.

### 2. Heroku Configuration
Ensure your Heroku app has the following Config Vars set in the dashboard (**Settings > Reveal Config Vars**):
- `OPENAI_API_KEY`: Your OpenAI API key.
- `DATABASE_URL`: This will be automatically injected if you provision the **Heroku Postgres** add-on under the Resources tab.

### 3. Automatic Deployment
Every time you push or merge code to the `main` branch, the GitHub Actions workflow (`.github/workflows/ci.yml`) will:
1. Check the code formatting and lint both the frontend and backend.
2. Build the production Docker image.
3. Push the image to the Heroku Container Registry and release it.

### 4. Initializing the Heroku Database
After your first deployment finishes successfully, you need to initialize the production database. You can do this using the Heroku CLI:

```bash
heroku run "uv run python3 -c \"from src.database import *; reset_database(); upload_questions()\"" -a <your-heroku-app-name>
```

---

## Todo
- Go through frontend, fix any obvious issues, inconsistencies or layout problems
- **Type Safety**: Migrate the Vue frontend JavaScript files to TypeScript for enhanced developer experience and error checking.

## Possible future ideas

- **Authentication & User Accounts**: Allow users to create accounts to save their progress across multiple devices and sessions.
- **Internationalization (i18n)**: The system prompts in `chat.py` are currently hardcoded in Swedish. Extracting text strings and adding multi-language support would significantly broaden the audience.
- **Testing**: Introduce unit and integration tests (e.g., `pytest` for the backend, and `Vitest` for the frontend).
- **Model Configuration**: Update the OpenAI API model string. It currently points to a theoretical `gpt-5-mini`. This should be mapped to an existing model like `gpt-4o-mini` or pulled from environment variables.
