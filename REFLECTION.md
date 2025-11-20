# Capstone Project, Individual Reflections

### Khayalethu – Docker & CI/CD

I owned the entire containerisation and continuous delivery track. I delivered:

- A production-grade multi-stage Dockerfile that produces a secure, non-root user image and is resilient – it builds successfully even with minimal backend files (proven in local build screenshot).
- A valid docker-compose.yml that enables the full stack to start with one command.
- A fully automated GitHub Actions CI/CD pipeline that builds and publishes the Docker image to Docker Hub on every push to main.

After Mfobe finalised the Gemini backend, I debugged and resolved Docker Hub authentication issues (username mismatch + token permissions). The latest successful run (#10) is green and the image was pushed 30 minutes ago.

**Live proof:**
- CI/CD pipeline (green run #10): https://github.com/Khaya14/resume-job-matcher/actions
- Published image with latest tag: https://hub.docker.com/r/khayalethu14/resume-matcher/tags
- Local successful build proof attached

Local development command:
```bash
docker compose -f docker/docker-compose.yml up --build