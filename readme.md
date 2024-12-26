# Streamlit visualisatie logbook archery

authentication: 

https://github.com/mkhorasani/Streamlit-Authenticator?tab=readme-ov-file#authenticateregister_user


## how to run?

1) add config.yaml file
````yaml
credentials:
  usernames:
    test:
      email: test@test.com
      name: test
      password: test # To be replaced with hashed password
cookie:
  expiry_days: 30
  key: abcdef # Must be string
  name: logbook_archery
preauthorized:
  emails:
  - melsby@gmail.com
````

2) setup virtual env

````
python -m venv streamlit_env
streamlit_env/Scripts/activate
````

3) install requirements
````
pip install -r requirements.txt
````

4) add secrets.toml file (maar misschien overbodig, gezien dit van een vorige authenticatiemethode was (zie docs streamlit zelf user authentication option 2))
````
[passwords]
# Follow the rule: username = "password"
jarno = "jarno"
test = "test"
````

streamlit run Home.py
