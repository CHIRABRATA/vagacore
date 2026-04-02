# VagaCore Deployment Guide

## 🎯 Deployment Options

VagaCore is a Python library, so "deployment" means making it available for others to install and use.

---

## Option 1: Deploy to PyPI (Python Package Index) ⭐ Recommended

This allows anyone to install your package with `pip install vagacore`.

### Prerequisites

1. **Create PyPI Account**
   - Go to [https://pypi.org/account/register/](https://pypi.org/account/register/)
   - Create an account and verify your email

2. **Create TestPyPI Account** (for testing)
   - Go to [https://test.pypi.org/account/register/](https://test.pypi.org/account/register/)
   - Create a separate test account

### Step-by-Step Deployment

#### 1. Install Build Tools

```bash
pip install --upgrade build twine
```

#### 2. Build the Package

```bash
# Navigate to project root
cd d:\vagacore

# Build distribution files
python -m build
```

This creates:
- `dist/vagacore-1.0.1.tar.gz` (source distribution)
- `dist/vagacore-1.0.1-py3-none-any.whl` (wheel distribution)

#### 3. Test on TestPyPI First

```bash
# Upload to TestPyPI
python -m twine upload --repository testpypi dist/*

# You'll be prompted for:
# Username: your_testpypi_username
# Password: your_testpypi_password
```

#### 4. Test Installation from TestPyPI

```bash
# Create a fresh virtual environment
python -m venv test_env
.\test_env\Scripts\activate

# Install from TestPyPI
pip install --index-url https://test.pypi.org/simple/ --no-deps vagacore

# Test it works
python -c "from vagacore import compress; print('Works!')"
```

#### 5. Deploy to Production PyPI

```bash
# Upload to real PyPI
python -m twine upload dist/*

# Enter your PyPI credentials
```

#### 6. Verify Installation

```bash
# Anyone can now install with:
pip install vagacore
```

### Using API Tokens (More Secure)

Instead of passwords, use API tokens:

1. **Generate Token on PyPI**
   - Go to [https://pypi.org/manage/account/](https://pypi.org/manage/account/)
   - Scroll to "API tokens" → "Add API token"
   - Scope: "Entire account" or "Project: vagacore"
   - Copy the token (starts with `pypi-`)

2. **Create `.pypirc` file**

```bash
# Windows: C:\Users\YourUsername\.pypirc
# Linux/Mac: ~/.pypirc
```

Add this content:

```ini
[distutils]
index-servers =
    pypi
    testpypi

[pypi]
username = __token__
password = pypi-YourActualTokenHere

[testpypi]
repository = https://test.pypi.org/legacy/
username = __token__
password = pypi-YourTestPyPITokenHere
```

3. **Upload without entering credentials**

```bash
python -m twine upload dist/*
```

### Updating Your Package

When you make changes:

1. **Update version in `setup.py`**
   ```python
   version="1.0.2",  # Increment version
   ```

2. **Update version in `vagacore/__init__.py`**
   ```python
   __version__ = "1.0.2"
   ```

3. **Rebuild and upload**
   ```bash
   # Remove old builds
   rm -rf dist/ build/ vagacore.egg-info/
   
   # Build new version
   python -m build
   
   # Upload
   python -m twine upload dist/*
   ```

---

## Option 2: Deploy as a Web API (Flask/FastAPI)

If you want to create a web service that users can call via HTTP:

### Create a Simple API

#### 1. Create `api.py`

```python
from flask import Flask, request, jsonify
from vagacore import compress

app = Flask(__name__)

@app.route('/api/extract', methods=['POST'])
def extract_facts():
    """Extract facts from text."""
    data = request.get_json()
    text = data.get('text', '')
    mode = data.get('mode', 'json')
    
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    
    try:
        result = compress(text, mode=mode)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def home():
    """API documentation."""
    return jsonify({
        'name': 'VagaCore API',
        'version': '1.0.1',
        'endpoints': {
            '/api/extract': {
                'method': 'POST',
                'body': {
                    'text': 'string (required)',
                    'mode': 'json|text|llm (optional)'
                }
            }
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
```

#### 2. Create `requirements-api.txt`

```txt
spacy>=3.0.0
flask>=2.0.0
gunicorn>=20.0.0
```

#### 3. Deploy to Render/Heroku/Railway

**Render (Free Tier):**

1. Push code to GitHub
2. Go to [https://render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Connect your GitHub repo
5. Configure:
   - **Build Command**: `pip install -r requirements-api.txt && python -m spacy download en_core_web_sm`
   - **Start Command**: `gunicorn api:app`
   - **Environment**: Python 3

**Railway:**

1. Go to [https://railway.app](https://railway.app)
2. "New Project" → "Deploy from GitHub repo"
3. Select your repo
4. Railway auto-detects Python and deploys

#### 4. Test Your API

```bash
curl -X POST https://your-api.onrender.com/api/extract \
  -H "Content-Type: application/json" \
  -d '{"text": "Apple earned $100B in Q3 2024.", "mode": "json"}'
```

---

## Option 3: Documentation Website (Netlify/GitHub Pages)

Create a documentation website for VagaCore:

### Using MkDocs

#### 1. Install MkDocs

```bash
pip install mkdocs mkdocs-material
```

#### 2. Create `mkdocs.yml`

```yaml
site_name: VagaCore Documentation
site_url: https://vagacore.netlify.app
theme:
  name: material
  palette:
    primary: indigo

nav:
  - Home: index.md
  - Installation: installation.md
  - Quick Start: quickstart.md
  - API Reference: api.md
  - Examples: examples.md
  - Contributing: contributing.md

markdown_extensions:
  - pymdownx.highlight
  - pymdownx.superfences
```

#### 3. Create `docs/` folder

```bash
mkdir docs
# Copy sections from README.md into separate files
```

#### 4. Build Static Site

```bash
mkdocs build
# Creates site/ directory with static HTML
```

#### 5. Deploy to Netlify

**Netlify Configuration:**

Create `netlify.toml`:

```toml
[build]
  command = "pip install mkdocs mkdocs-material && mkdocs build"
  publish = "site"

[build.environment]
  PYTHON_VERSION = "3.8"
```

**In Netlify UI:**
- **Branch**: `main`
- **Build Command**: `pip install mkdocs mkdocs-material && mkdocs build`
- **Publish Directory**: `site`

---

## Option 4: GitHub Releases

Simple distribution without PyPI:

1. **Create a Release on GitHub**
   ```bash
   git tag v1.0.1
   git push origin v1.0.1
   ```

2. **Users install directly from GitHub**
   ```bash
   pip install git+https://github.com/CHIRABRATA/vagacore.git
   ```

---

## 📊 Comparison

| Option | Best For | Difficulty | Reach |
|--------|----------|------------|-------|
| **PyPI** | Python developers | Medium | ⭐⭐⭐⭐⭐ Worldwide |
| **Web API** | Non-Python users | Hard | ⭐⭐⭐ Anyone with HTTP |
| **Docs Site** | Documentation | Easy | ⭐⭐⭐ Information only |
| **GitHub** | Open source | Easy | ⭐⭐ Developers only |

---

## ✅ Recommended Approach

1. **Deploy to PyPI** (primary distribution)
2. **Create documentation site** (for guides and tutorials)
3. **(Optional) Create Web API** if you want non-Python users to access it

---

## 🆘 Need Help?

- PyPI Documentation: https://packaging.python.org/
- Render Deployment: https://render.com/docs
- MkDocs Guide: https://www.mkdocs.org/
