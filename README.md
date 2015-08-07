# scrum-progress
At the moment this service posts data to a postgres database.

##requirements:
- postgres
- python 3
- python modules listed in requirements.txt

##How to run

```
vagrant up
```

```
vagrant ssh
```

```
cd /vagrant
```

```
source ~/venvs/scrum-progress/bin/activate
```

```
source environment.sh
```

```
python3 manage.py db upgrade
```

```
pip install -r requirements.txt
```

```
./run.sh
```
