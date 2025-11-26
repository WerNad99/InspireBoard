# 🚀 Deployment Guide - GitHub Container Registry

## Overview

This project automatically builds and publishes Docker images to **GitHub Container Registry (ghcr.io)** when you push to the `main` branch.

## 📋 Setup Steps

### 1. Enable GitHub Packages (One-time setup)

**No additional setup needed!** The workflow uses `GITHUB_TOKEN` which is automatically available in GitHub Actions.

### 2. Push to Main Branch

```bash
git add .
git commit -m "Your commit message"
git push origin main
```

### 3. GitHub Actions Will:

✅ **Build Job:**
- Checkout code
- Set up Python 3.11
- Install dependencies
- Lint code with flake8
- Run application tests

🐳 **Docker Job** (only on main branch):
- Checkout code
- Set up Docker Buildx
- Log in to GitHub Container Registry
- Build Docker image
- Push image with multiple tags:
  - `ghcr.io/YOUR_USERNAME/REPO_NAME:latest`
  - `ghcr.io/YOUR_USERNAME/REPO_NAME:main`
  - `ghcr.io/YOUR_USERNAME/REPO_NAME:main-<commit-sha>`

## 📦 Using the Published Image

### Pull the Image

```bash
# Replace with your actual repository path
docker pull ghcr.io/YOUR_USERNAME/REPO_NAME:latest
```

### Run the Container

```bash
docker run -d -p 5000:5000 --name inspireboard ghcr.io/YOUR_USERNAME/REPO_NAME:latest
```

### Access the Application

Open your browser: `http://localhost:5000`

## 🔐 Making Your Package Public (Optional)

By default, packages are private. To make them public:

1. Go to your GitHub repository
2. Click on **Packages** in the right sidebar
3. Click on your package name
4. Go to **Package settings** (bottom right)
5. Scroll down to **Danger Zone**
6. Click **Change visibility** → Select **Public**

## 🌐 Deployment Options

### Deploy to AWS ECS

```bash
# Update ECS service to use new image
aws ecs update-service \
  --cluster your-cluster \
  --service inspireboard \
  --force-new-deployment
```

### Deploy to Google Cloud Run

```bash
gcloud run deploy inspireboard \
  --image ghcr.io/YOUR_USERNAME/REPO_NAME:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --port 5000
```

### Deploy to Azure Container Instances

```bash
az container create \
  --resource-group myResourceGroup \
  --name inspireboard \
  --image ghcr.io/YOUR_USERNAME/REPO_NAME:latest \
  --dns-name-label inspireboard \
  --ports 5000
```

### Deploy to Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: inspireboard
spec:
  replicas: 3
  selector:
    matchLabels:
      app: inspireboard
  template:
    metadata:
      labels:
        app: inspireboard
    spec:
      containers:
      - name: inspireboard
        image: ghcr.io/YOUR_USERNAME/REPO_NAME:latest
        ports:
        - containerPort: 5000
---
apiVersion: v1
kind: Service
metadata:
  name: inspireboard
spec:
  type: LoadBalancer
  ports:
  - port: 80
    targetPort: 5000
  selector:
    app: inspireboard
```

Apply with:
```bash
kubectl apply -f deployment.yaml
```

### Deploy to Your Own Server via SSH

```bash
# SSH into your server
ssh user@your-server.com

# Pull the latest image
docker pull ghcr.io/YOUR_USERNAME/REPO_NAME:latest

# Stop and remove old container
docker stop inspireboard || true
docker rm inspireboard || true

# Run new container
docker run -d -p 5000:5000 --name inspireboard --restart unless-stopped \
  ghcr.io/YOUR_USERNAME/REPO_NAME:latest
```

## 🔍 Viewing Build Status

1. Go to your GitHub repository
2. Click on **Actions** tab
3. You'll see all workflow runs
4. Click on any run to see detailed logs

## 🐛 Troubleshooting

### Image Not Found
- Make sure the workflow completed successfully
- Check if the package is public or you're authenticated
- Verify the image path: `ghcr.io/<username>/<repo-name>:latest`

### Authentication Required
If pulling a private image:

```bash
# Create a Personal Access Token (PAT) with read:packages permission
echo $YOUR_GITHUB_TOKEN | docker login ghcr.io -u YOUR_USERNAME --password-stdin

# Then pull
docker pull ghcr.io/YOUR_USERNAME/REPO_NAME:latest
```

### Workflow Not Running
- Check that you pushed to `main` branch
- Verify the workflow file is in `.github/workflows/`
- Check Actions tab for any errors

## 📊 Monitoring

Check the health of your deployed application:

```bash
curl http://your-server:5000/health
```

Expected response:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-26T...",
  "version": "1.0.0"
}
```

## 🎯 Best Practices

1. **Tag your releases**: Use semantic versioning (v1.0.0, v1.1.0, etc.)
2. **Test locally first**: Build and test Docker image before pushing
3. **Monitor builds**: Check GitHub Actions for any failures
4. **Use specific tags**: In production, use specific version tags instead of `latest`
5. **Set resource limits**: Configure memory and CPU limits in production

## 📚 Additional Resources

- [GitHub Container Registry Docs](https://docs.github.com/en/packages/working-with-a-github-packages-registry/working-with-the-container-registry)
- [Docker Documentation](https://docs.docker.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

---

⚡ **Powered by:** AWS • Jenkins • Datadog • Flask | © 2025 Andrew O.

