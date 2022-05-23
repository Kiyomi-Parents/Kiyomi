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
    # Set environment variables manually
    # Alternatively rename .env.example to .env and fill out the configuration there instead
	export DISCORD_TOKEN=<Discord bot token>
    export DATABASE_IP=<MySql/MariaDB host ip>
    export DATABASE_USER=<Database username>
    export DATABASE_PW=<Database password>
    export DATABASE_NAME=<Database name>
    export DEFAULT_GUILD=<Default guild ID. Used for fallback if something isn't found/overridden on the current guild>
    export ADMIN_GUILDS=<Comma seperated list of guild ids. This is for bot owner commands.>
    export DEBUG_GUILDS=<Comma seperated list of guild ids. This is for development only. Leave empty on production>

    # Run database migrations
    alembic upgrade head
  
	# Start bot  
	python3 Kiyomi.py

### Lint
    # Run pylint
    pylint Kiyomi.py src

### Code formatter
    pip install black
    python -m black ./Kitomi.py ./src

### Generate alembic migration
    alembic revision --autogenerate -m "Change message"
