# Kasparro Agentic Facebook Performance Analyst - Makefile
# =========================================================

# === Setup environment ===
setup:
	python -m venv venv
	venv\Scripts\python.exe -m pip install --upgrade pip
	venv\Scripts\python.exe -m pip install -r requirements.txt

# === Run the full agentic pipeline ===
run:
	venv\Scripts\python.exe run.py "Analyze ROAS drop"

# === Run all tests ===
test:
	venv\Scripts\python.exe -m pytest -v

# === Run only unit tests ===
test-unit:
	venv\Scripts\python.exe -m pytest -v -m unit

# === Run only integration tests ===
test-integration:
	venv\Scripts\python.exe -m pytest -v -m integration

# === Clean up artifacts ===
clean:
	@echo Cleaning reports and logs...
	@if exist reports (del /q reports\*.*)
	@if exist logs (del /q logs\*.*)
