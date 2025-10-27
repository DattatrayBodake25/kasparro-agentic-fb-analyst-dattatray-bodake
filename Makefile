# Kasparro Agentic Facebook Performance Analyst - Makefile

# === Setup environment ===
setup:
	python -m venv venv
	venv\Scripts\activate && pip install -r requirements.txt

# === Run the full agentic pipeline ===
run:
	venv\Scripts\activate && python run.py "Analyze ROAS drop"

# === Run all tests ===
test:
	venv\Scripts\activate && pytest -v

# === Run only unit tests ===
test-unit:
	venv\Scripts\activate && pytest -v -m unit

# === Run only integration tests ===
test-integration:
	venv\Scripts\activate && pytest -v -m integration

# === Clean up artifacts ===
clean:
	@echo "Cleaning reports and logs..."
	@if exist reports (del /q reports\*.*)
	@if exist logs (del /q logs\*.*)