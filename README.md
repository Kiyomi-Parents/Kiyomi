# BSBot

cool bot

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


### Tests
    # Run tests
    pytest
    # or
    pytest -v --numprocesses=auto

### Lint
    # Run pylint
    pylint BSBot.py src tests
