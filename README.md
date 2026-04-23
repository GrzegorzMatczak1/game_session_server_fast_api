# game_session_server_fast_api

## Overview

This repository implements a basic game session server using Fast-api to create a development server and Pydantic to ensure the proper file structure. 

Every second each player gets 1 mana. 
You can spend this mana to either deal damage to all other players or you can use it to upgrade your stats. 
Each player regenerates 1 hp per second. However after taking damage there is a 5 second pause where hp does not regenerate. The attacking player's pause lasts 2 seconds. 

## Usage
```
fastapi dev
```

