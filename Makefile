# V2 Evaluators Framework - Easy Commands

.PHONY: help setup test evaluate example clean install

help: ## Show this help message
	@echo "🎯 V2 Evaluators Framework - Easy Commands"
	@echo "=========================================="
	@echo ""
	@echo "Available commands:"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'
	@echo ""
	@echo "Quick start: make setup && make example"

setup: ## Run automated setup
	@echo "🚀 Setting up V2 Evaluators Framework..."
	python setup_evaluators.py

install: ## Install dependencies only
	@echo "📦 Installing dependencies..."
	pip install -r requirements_v2.txt

test: ## Run all tests
	@echo "🧪 Running tests..."
	python test_evaluators.py
	python -m pytest tests/ -v

test-quick: ## Run quick functionality test
	@echo "⚡ Running quick test..."
	python test_evaluators.py

test-unit: ## Run unit tests only
	@echo "🔬 Running unit tests..."
	python -m pytest tests/ -v

example: ## Run example evaluation
	@echo "🎯 Running example evaluation..."
	python example_usage.py

evaluate: ## Interactive code evaluation
	@echo "🔍 Starting interactive evaluation..."
	@echo "Usage: make evaluate CODE='your_code_here'"
	@if [ -z "$(CODE)" ]; then \
		echo "❌ Please provide CODE parameter"; \
		echo "Example: make evaluate CODE='def add(a,b): return a+b'"; \
	else \
		python evaluate_code.py "$(CODE)" --problem "Code evaluation"; \
	fi

evaluate-file: ## Evaluate code from file
	@echo "📁 Evaluating code from file..."
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Please provide FILE parameter"; \
		echo "Example: make evaluate-file FILE=my_code.py"; \
	else \
		python evaluate_code.py $(FILE) --file; \
	fi

evaluate-with-llm: ## Evaluate code with LLM judges
	@echo "🤖 Evaluating with LLM judges..."
	@if [ -z "$(CODE)" ]; then \
		echo "❌ Please provide CODE parameter"; \
		echo "Example: make evaluate-with-llm CODE='def add(a,b): return a+b'"; \
	else \
		python evaluate_code.py "$(CODE)" --problem "Code evaluation" --llm; \
	fi

check-api: ## Check API keys
	@echo "🔑 Checking API keys..."
	@python -c "import os; keys=['OPENAI_API_KEY','ANTHROPIC_API_KEY','GEMINI_API_KEY']; found=[k for k in keys if os.getenv(k)]; print(f'Found {len(found)} API key(s): {found}' if found else 'No API keys found. Set at least one API key.')"

check-deps: ## Check dependencies
	@echo "📋 Checking dependencies..."
	@python -c "import sys; print(f'Python: {sys.version.split()[0]}'); import pkg_resources; deps=['aiohttp','scikit-learn','docker','pytest','pylint','bandit','radon','mypy','psutil','pandas','numpy','pyyaml']; installed=[d for d in deps if d in [p.project_name for p in pkg_resources.working_set]]; print(f'Installed: {len(installed)}/{len(deps)} packages')"

clean: ## Clean up generated files
	@echo "🧹 Cleaning up..."
	rm -f *.json *.csv
	rm -rf __pycache__ */__pycache__ */*/__pycache__
	rm -rf .pytest_cache
	rm -rf calibration_models
	rm -f calibration_data.json

format: ## Format code with black
	@echo "🎨 Formatting code..."
	black evaluators/ tests/ *.py

lint: ## Run linting
	@echo "🔍 Running linters..."
	pylint evaluators/ || true
	black --check evaluators/ tests/ *.py || true

docs: ## Generate documentation
	@echo "📚 Generating documentation..."
	@echo "Documentation is available in:"
	@echo "  - README_Evaluators.md (comprehensive guide)"
	@echo "  - QUICKSTART.md (quick start guide)"
	@echo "  - example_usage.py (code examples)"

# Development commands
dev-install: ## Install development dependencies
	@echo "🛠️  Installing development dependencies..."
	pip install -r requirements_v2.txt
	pip install pytest pytest-cov black isort pylint

dev-test: ## Run development tests with coverage
	@echo "🧪 Running development tests..."
	python -m pytest tests/ --cov=evaluators --cov-report=html --cov-report=term

dev-format: ## Format and lint code
	@echo "🎨 Formatting and linting..."
	black evaluators/ tests/ *.py
	isort evaluators/ tests/ *.py
	pylint evaluators/

# Docker commands (optional)
docker-build: ## Build Docker image for sandbox
	@echo "🐳 Building Docker image..."
	docker build -t v2-evaluators-python:3.11-slim -f Dockerfile.python .

docker-test: ## Test with Docker
	@echo "🐳 Testing with Docker..."
	python -c "from evaluators import SandboxRunner; r = SandboxRunner(use_docker=True); print('Docker test:', r.use_docker)"
