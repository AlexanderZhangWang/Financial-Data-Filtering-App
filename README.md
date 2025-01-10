# Financial Data Filtering App

## 1.1 Clone the repo:

```
git clone --recurse-submodules https://github.com/AlexanderZhangWang/Financial-Data-Filtering-App
cd Financial-Data-Filtering-App
```
## 1.2 Create a virtual environment

### Windows:

```
python -m venv venv
venv\Scripts\activate
```

### macOS

```
python3 -m venv venv
source venv/bin/activate
```

## 1.3 Install requirements.txt
```
pip install -r requirements.txt

```
## 1.4 Get your API Key
In app.py, Line 7 and 8:
```
#FMP_API_KEY = ""
FMP_API_KEY = os.environ["FMP_API_KEY"]
```
comment out Line 8 and uncomment Line 7. paste your API KEY inside the quotations.

[You can get Free API KEY here](https://site.financialmodelingprep.com/)

## 1.5 Run the app

```
python server.py
```
