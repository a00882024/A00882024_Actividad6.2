# A00882024_Actividad6.2

## Installation

1. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run tests

```bash
pytest tests/
```

### Run tests with coverage

```bash
pytest --cov=src tests/
```

To see missing lines:

```bash
pytest --cov=src --cov-report=term-missing tests/
```

To generate an HTML report:

```bash
pytest --cov=src --cov-report=html tests/
```

### Linting

Run pylint:

```bash
pylint src/
```

Run flake8:

```bash
flake8 src/
```
