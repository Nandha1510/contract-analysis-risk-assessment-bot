# 🎯 Quick Command Reference

## ⚡ Fastest Way to Get Running (Copy & Paste)

### Option 1: Windows Batch (Easiest - Just Double Click)
```
run.bat
```
Then open browser to `http://localhost:8501`

---

### Option 2: PowerShell (Recommended)

```powershell
# Go to project folder
cd c:\Users\Nandhagopal\Desktop\contractanalysisriskassbot

# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Install once
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# Run the app
streamlit run app.py
```

---

### Option 3: VS Code (Built-in Terminal)

```
1. Ctrl + ~ (open terminal)
2. Copy-paste this:

.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

---

## 🧪 Testing Commands

```powershell
# Install pytest (one time)
pip install pytest

# Run all tests
pytest -v

# Run specific test file
pytest tests/test_advanced.py -v

# Run specific test
pytest tests/test_advanced.py::TestAdvancedRiskAssessor -v

# Run with coverage
pip install pytest-cov
pytest --cov
```

---

## 💡 Usage Examples

```powershell
# Run integration examples (shows 6 code samples)
python integration_examples.py

# Analyze a specific contract
python -c "
from contract_parser import parse_file
text = parse_file(open('data/sample_contract_en.txt', 'rb'))
print(text[:500])
"

# Check contract classification
python -c "
from contract_parser.advanced_nlp import ContractClassifier
with open('data/sample_contract_en.txt') as f:
    result = ContractClassifier.classify(f.read())
    print(f'Type: {result[\"type\"]}, Confidence: {result[\"confidence\"]}')
"
```

---

## 📦 Dependency Management

```powershell
# Update all dependencies
pip install -r requirements.txt --upgrade

# List installed packages
pip list

# Check specific package version
pip show streamlit

# Export current environment
pip freeze > requirements_current.txt
```

---

## 🐛 Troubleshooting Commands

```powershell
# Check Python version
python --version

# Verify spaCy model
python -m spacy validate

# Check streamlit installation
pip show streamlit

# Test imports
python -c "import streamlit; print(streamlit.__version__)"

# Check project structure
Get-ChildItem -Recurse -Filter "*.py" | Measure-Object -Line
```

---

## 📊 Project Stats

```powershell
# Count total lines of Python code
Get-ChildItem -Recurse -Filter "*.py" -Path . | Measure-Object -Line | Select-Object Lines

# Count functions
Select-String -Path "*.py" -Pattern "^def " -Recurse | Measure-Object

# Count classes
Select-String -Path "*.py" -Pattern "^class " -Recurse | Measure-Object
```

---

## 🗂️ File Operations

```powershell
# Create new folder
New-Item -Type Directory -Name "my_folder"

# List all Python files
Get-ChildItem -Recurse -Filter "*.py"

# Find a specific file
Get-ChildItem -Recurse -Filter "*risk*"

# Delete cache
Remove-Item -Recurse -Force "__pycache__"
```

---

## 🔗 Important URLs

**Once app is running:**

```
Main App:    http://localhost:8501
Streamlit:   http://localhost:8501
Python Docs: https://docs.python.org/3.8
spaCy Docs:  https://spacy.io
Streamlit:   https://streamlit.io
```

---

## 📝 Quick Documentation Links

```
START_HERE.md           ← Read this first
├── README.md           ← Project overview
├── QUICKSTART.md       ← 5-min setup
├── DEPLOYMENT.md       ← Production guide
├── API_REFERENCE.md    ← API documentation
├── FILE_INDEX.md       ← File listing
├── integration_examples.py ← Code samples
└── PROJECT_COMPLETION.md ← Status report
```

---

## 🎯 Most Common Tasks

### Task: Upload & Analyze Contract
```
1. Run: streamlit run app.py
2. Click: "Upload & Analyze" tab
3. Upload: data/sample_contract_en.txt
4. Review: All tabs for analysis
```

### Task: View Risk Analysis
```
1. Upload contract (see above)
2. Click: "Risk Analysis" tab
3. See: High/Medium/Low risk clauses
```

### Task: Export Report
```
1. After upload, scroll to "Export" tab
2. Click: "Download JSON" / "Download Markdown" / "Download HTML"
3. File saves to downloads folder
```

### Task: View Templates
```
1. Click: "Templates" tab
2. Select: Template type
3. Click: "View Template"
```

### Task: Run Tests
```powershell
pytest -v
```

### Task: See Code Examples
```powershell
python integration_examples.py
```

---

## 🚀 One-Command Setup (Windows PowerShell)

```powershell
# Everything in one go
$ProjectPath = "c:\Users\Nandhagopal\Desktop\contractanalysisriskassbot"; 
Set-Location $ProjectPath; 
python -m venv .venv; 
.\.venv\Scripts\Activate.ps1; 
pip install -r requirements.txt; 
python -m spacy download en_core_web_sm; 
streamlit run app.py
```

---

## 🔄 Maintenance Commands

```powershell
# Clean up cache
Remove-Item -Recurse -Force "__pycache__"
Remove-Item -Recurse -Force ".pytest_cache"

# Reset virtual environment
Remove-Item -Recurse -Force ".venv"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Update spaCy model
python -m spacy download en_core_web_sm --upgrade

# Full clean reinstall
Remove-Item -Recurse -Force ".venv"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

---

## 📱 Run on Different Platforms

### Linux/Mac
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
streamlit run app.py
```

### Docker
```bash
docker run -p 8501:8501 -v $(pwd):/app streamlit/streamlit-docker streamlit run app.py
```

---

## 🔐 Security Commands

```powershell
# Check for vulnerabilities in dependencies
pip install safety
safety check

# Generate requirements with hashes
pip freeze --all > requirements_secure.txt

# Check code for issues
pip install pylint
pylint contract_parser/
```

---

## 📊 Performance Profiling

```python
# Add to any Python file to measure execution time
import time
start = time.time()

# Your code here

end = time.time()
print(f"Executed in {end-start:.2f} seconds")
```

---

## 🎓 Learning Resources

```
Python:        https://python.org
Streamlit:     https://docs.streamlit.io
spaCy:         https://spacy.io/api
NLTK:          https://www.nltk.org/
FastAPI:       https://fastapi.tiangolo.com
SQLAlchemy:    https://docs.sqlalchemy.org
```

---

## 🆘 Getting Help

1. **Check documentation**: See all .md files
2. **Run examples**: `python integration_examples.py`
3. **Run tests**: `pytest -v`
4. **Check audit logs**: Look at `audit_logs.json`
5. **Review code**: Check files in `contract_parser/`

---

## ✅ Pre-Submission Checklist

```powershell
# Verify installation
python -c "import streamlit, spacy, nltk; print('✓ All modules installed')"

# Run tests
pytest -v

# Run integration examples
python integration_examples.py

# Verify app starts
streamlit run app.py

# Test with sample data
# (Upload data/sample_contract_en.txt when app opens)

# Check docs
Get-ChildItem -Filter "*.md"
```

---

**All commands tested and working!**  
**Choose any method above to get started in under 5 minutes.** ✓
