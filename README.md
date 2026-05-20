# Managed Services Platform

Enterprise platform operations simulation: Linux server provisioning, CI/CD,
observability stack, and automated incident response.

## Architecture
- **app-server** (Multipass VM): Runs the FastAPI client application
- **monitor-server** (Multipass VM): Runs Grafana, Loki, Prometheus
- **CI/CD**: GitHub Actions for build/test/deploy/rollback
- **Provisioning**: Bash scripts + cloud-init

## Status
In active development.
