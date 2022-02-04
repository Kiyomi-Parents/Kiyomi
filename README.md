<h1 align="center">
  <br>
  <a href="https://github.com/Kiyomi-Parents/Kiyomi"><img src="https://share.lucker.xyz/qahu5/rakOHeSi09.png/raw.png" alt="Kiyomi"></a>
  <br>
  Kiyomi
  <br>
</h1>

# Overview

Discord bot that has various functionality related to Beat Saber.

### Install

    # Install requirements  
	python3 -m pip install -r requirements.txt  

### Usage
    # Run database migrations
    alembic upgrade head

    # Set discord token  
	export DISCORD_TOKEN=<My very secret token>  
  
	# Start bot  
	python3 BSBot.py

### Lint
    # Run pylint
    pylint BSBot.py src tests
