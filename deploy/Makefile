# Makefile
# PetVoice AI Development Commands

# Variables
PYTHON := python3
PIP := pip3
FLASK := flask
DOCKER := docker
COMPOSE := docker-compose

# Default target
.PHONY: help
help:
	@echo "PetVoice AI Development Commands"
	@echo "=============================="
	@echo "help            - Show this help message"
	@echo "install         - Install Python dependencies"
	@echo "setup           - Setup development environment"
	@echo "run             - Run the development server"
	@echo "test            - Run tests"
	@echo "clean           - Clean up temporary files"
	@echo "docs            - Generate API documentation"
	@echo "backup          - Create database backup"
	@echo "health          - Run health check"
	@echo "security        - Run security check"
	@echo "docker-build    - Build Docker images"
	@echo "docker-up       - Start services with Docker Compose"
	@echo "docker-down     - Stop Docker Compose services"
	@echo "docker-logs     - Show Docker Compose logs"

# Install dependencies
.PHONY: install
install:
	$(PIP) install -r requirements.txt

# Setup development environment
.PHONY: setup
setup:
	$(PYTHON) setup_dev.py

# Run development server
.PHONY: run
run:
	$(PYTHON) run.py

# Run tests
.PHONY: test
test:
	$(PYTHON) run_tests.py

# Clean temporary files
.PHONY: clean
clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf *.log
	rm -rf temp/

# Generate API documentation
.PHONY: docs
docs:
	$(PYTHON) generate_docs.py

# Create database backup
.PHONY: backup
backup:
	$(PYTHON) backup_db.py backup

# Run health check
.PHONY: health
health:
	$(PYTHON) health_check.py

# Run security check
.PHONY: security
security:
	$(PYTHON) security_check.py

# Build Docker images
.PHONY: docker-build
docker-build:
	$(DOCKER) build -t petvoice-app .

# Start services with Docker Compose
.PHONY: docker-up
docker-up:
	$(COMPOSE) up -d

# Stop Docker Compose services
.PHONY: docker-down
docker-down:
	$(COMPOSE) down

# Show Docker Compose logs
.PHONY: docker-logs
docker-logs:
	$(COMPOSE) logs -f

# Initialize database
.PHONY: init-db
init-db:
	$(PYTHON) init_db.py

# Run all checks
.PHONY: check
check: health security

# Generate project summary
.PHONY: summary
summary:
	$(PYTHON) project_summary.py