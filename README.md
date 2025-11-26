# ✨ InspireBoard
Inspirational Board for best-in-class motivational quotes and citations. Start your day right!

by **Andrew Oranskyi**

## 🚀 Quick Start with Docker (Recommended)

### Pull and Run from GitHub Container Registry

```bash
# Pull the latest image
docker pull ghcr.io/YOUR_GITHUB_USERNAME/REPO_NAME:latest

# Run the container
docker run -d -p 5000:5000 --name inspireboard ghcr.io/YOUR_GITHUB_USERNAME/REPO_NAME:latest

# Visit http://localhost:5000
```

### Build and Run Locally

```bash
# Clone the repository
git clone <your-repo-url>
cd "CI:CD project"

# Build Docker image
docker build -t inspireboard .

# Run the container
docker run -d -p 5000:5000 --name inspireboard inspireboard
```

## 🐍 Run with Python

```bash
# Install Flask
pip install flask

# Run the application
python app.py

# Visit http://localhost:5000
```

## 🛠️ Features

- ✨ Beautiful, modern UI with gradient design
- 📝 Add your own inspirational quotes
- 🎲 Display random quotes
- 💾 SQLite database for persistence
- 🏥 Health check endpoint (`/health`)
- 🐳 Fully containerized with Docker
- 🚀 CI/CD ready with GitHub Actions

## 📦 Docker Commands

```bash
# View running containers
docker ps

# View logs
docker logs inspireboard

# Stop the container
docker stop inspireboard

# Remove the container
docker rm inspireboard

# Check application health
curl http://localhost:5000/health
```

## 🔄 CI/CD Pipeline

The project includes a GitHub Actions workflow that automatically:
- ✅ Tests the application
- ✅ Lints the code
- 🐳 Builds Docker image
- 📦 Pushes to GitHub Container Registry

Triggered on every push to `main` branch.

## 🌐 API Endpoints

- `GET /` - Main application page
- `GET /health` - Health check endpoint
- `GET /api/quotes` - Get all quotes
- `GET /api/quotes/random` - Get a random quote
- `POST /api/quotes` - Add a new quote
- `DELETE /api/quotes/<id>` - Delete a quote

## 💡 Tech Stack

⚡ **Powered by:** AWS • Jenkins • Datadog • Flask

© 2025 Andrew O. All rights reserved.
