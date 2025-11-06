# Django Workshop



## Requirements
- Python 3.11+ (or the version you used)
- Git
- (Optional) [uv](https://github.com/astral-sh/uv) if you want to use it instead of pip

---

## 1. Clone the repository
```bash
git clone https://github.com/LindaOuer/PFW_2526_3IA5.git
cd PFW_2526_3IA5
```
---

## 2. Set up a virtual environment
### Option A – Using pip / venv
#### create venv
```bash
python -m venv venv
```
#### activate
- Windows:
```bash
venv\Scripts\activate
```
- macOS/Linux:
```bash
source venv/bin/activate
```
#### install dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```
### Option B – Using uv

#### create an environment
```bash
uv venv
```
#### activate 
- macOS/Linux
```bash
source .venv/bin/activate
```        
- Windows PowerShell
```bash
.venv\Scripts\activate
```

#### install dependencies from requirements.txt
```bash
uv pip install -r requirements.txt
```

## 3. Database migrations
```bash
python manage.py migrate
```

## 4. Run the development server
```bash
python manage.py runserver
```
