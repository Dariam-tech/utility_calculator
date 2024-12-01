PYTHON_VERSION = 3.11
VENV = .venv

# Create virtual environment and install dependencies
init:
	uv venv --python=$(PYTHON_VERSION) $(VENV)
	uv sync

# Run the Streamlit application
run:
	uv run streamlit run utility_calculator.py

# Clean up generated files
clean:
	rm -rf $(VENV) __pycache__ *.pyc



