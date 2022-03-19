<h1 align="center">
  <br>
  <a href="https://github.com/Kiyomi-Parents/Kiyomi"><img src="https://share.lucker.xyz/qahu5/rakOHeSi09.png/raw.png" alt="Kiyomi"></a>
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
    # Set environment variables manually
    # Alternatively rename .env.example to .env and fill out the configuration there instead
	export DISCORD_TOKEN=<Discord bot token>
    export DATABASE_IP=<MySql/MariaDB host ip>
    export DATABASE_USER=<Database username>
    export DATABASE_PW=<Database password>
    export DATABASE_NAME=<Database name>

    # Run database migrations
    alembic upgrade head
  
	# Start bot  
	python3 Kiyomi.py

### Lint
    # Run pylint
    pylint Kiyomi.py src

### Generate alembic migration
    alembic revision --autogenerate -m "Change message"
