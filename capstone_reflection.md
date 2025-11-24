# Capstone Project, Individual Reflections

### Member 1 - UI & Low-code

While integrating a third-party API into an AppSmith application, I encountered an issue where the two pages failed to communicate properly after adding the API key. 
The key wasn’t being correctly passed or recognized in the request context, which prevented the results page from reflecting whether the API call was successful or returning data.
I systematically debugged the authentication flow, request headers, and AppSmith’s API binding behavior, identified that the key needed to be injected via the ‘Headers’ section instead of query params, and added proper error handling with success/failure widgets.

### Member 2 - AI Backend (FastAPI + Gemini)



### Member 3 – Docker & CI/CD

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

### Member 4 - Kubernetes & Documentation