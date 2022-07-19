<h1 align="center">
  <br>
  <a href="https://github.com/Kiyomi-Parents/Kiyomi"><img src="https://share.lucker.xyz/qahu5/WelisUWo93.png/raw.png" alt="Kiyomi"></a>
  <br>
  Kiyomi 🦊
  <br>
</h1>

# Overview

Discord bot that has various functionality related to Beat Saber 💜</br>
<sub>Watching your Beat Saber activity very closely 👀</sub></br>
<sub>Measures your Score Saber PP everyday 📏</sub>


### Install dependencies
    # Install requirements  
	python3 -m pip install -r requirements.txt  

### Starting Kiyomi
    rename example.config.json to config.json and fill in your configuration details.

    # Run database migrations
    alembic upgrade head
  
	# Start bot  
	python3 Kiyomi.py

### Lint
    # Run pylint
    pylint Kiyomi.py src

### Code formatter
    pip install black
    python -m black ./Kiyomi.py ./src

### Generate alembic migration
    alembic revision --autogenerate -m "Change message"
