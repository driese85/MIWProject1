# MakeITWork Project 1 - De gezondheidszorg
### Student: Elmer van den Dries
<br>

# Cloning the repository
Clone the repo to a folder of your choosing on your local machine:

```bash
git clone git@github.com:ElmerHR/MIWProject1.git

cd MIWProject1
```

# How to run the "build" folder?
### **ETL**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

pip install -r pip_requirements.txt

python build/etl.py
```
### **Regression modeling**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

pip install -r pip_requirements.txt

python build/regression.py
```
<br>

# How to run the "run" folder?
### **CLI app**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

pip install -r pip_requirements.txt

python run/cli/cli.py
```

### **Flask app**
Run the below commands where \<env> is substituted by your chosen environment name:
```bash
conda create --name <env> --file conda_requirements.txt

conda activate <env>

pip install -r pip_requirements.txt

cd run/flask && flask run
```

