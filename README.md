# ShikinhaBot
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://forthebadge.com)

## What is the ShikinhaBot?

  Shikinha is a multipurpose discord bot  made in Python 3 (discord.py=2.0.1), with it's core features being the integration with the OpenAI's API
  (allowing access to DALL-E and GPT-3 models via commands), the capability to play music (Youtube) using Lavalink and many other features.
  
  The default prefix for the bot is ";", wich you can change in line 19 ```client = commands.Bot(command_prefix=";", intents=intents)``` 

## Setting up...

  First of all, you'll need a Discord API token, wich you can get at the [Discord developer portal](https://discord.com/developers/applications) by creating a new application and generating a new token. After you get the token, just paste it into the "disc_token" variable present in the "secret.py" file.

  For the GPT and and DALL-E commands to work, you will need to get an API key for OpenAI's API, wich you can get here: https://platform.openai.com/overview
and paste the key into the "secret.py" file too ("openai_token" variable).
  
  As for the music commands, you will need to have a Lavalink server running. Download the Lavalink.jar [here](https://github.com/freyacodes/Lavalink/releases) (Note that you'll need at least Java 13 to run a Lavalink server) and copy the application.yml file present [here](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example) and paste everything into the same folder your code is in. After you've downloaded everything, you can simply run the Lavalink server with the command ```java --jar Lavalink.jar```
  
  Before you run the bot, make sure you've installed all the libs present in the "requirements.txt" file with the command ```pip install -r requirements.txt```
  Now that everything is set up, you can run your Shikinha Bot! Just run ```python Shikinha.py``` and have fun!

## Commands

### Miscellaneous:
  * help
  	*  Displays a help message;
  * clear [n°]
  	* Clears [n°] messages from chat (requires "manage messages" permissions);
  * ping
  	* Shows latency;
  * wiki [search]: 
  	* Searches [search] on Wikipedia;
  * random_wiki
  	* Searches for a random post on Wikipedia;

### Music:
  * connect
  	* Makes Shikinha join your voice channel;
  * disconnect
  	* Makes Shikinha disconnect from your voice channel;
  * play [song name/url]
  	* Plays a song [song name/url];
  * skip
  	* Skips the song that is currently playing;
  * pause
  	* Pauses the song that is currently playing;
  * resume
  	* Resumes the song that is currently playing;
 
 ### IA (OpenAI):
  * gpt [prompt]:
  	* Interacts with GTP-3 (davinci) with the provided prompt [prompt]; 
  * dalle [prompt]:
  	* Generates a 1024x1024 image using DALL-E; 

### NSFW:
 * e621 [tags]:
 	* Searches for a random post on E621 with the tags [tags]; 
 * rule34 [tags]:
 	* Searches for a random post on Rule34 with the tags [tags]; 
