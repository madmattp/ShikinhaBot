# ShikinhaBot

  Shikinha is a multipurpose discord bot made in Python 3, with it's core features being the integration with the OpenAI's API (allowing access to DALL-E and GPT-3 models) and the capability to play music (Youtube) using Lavalink. 

# Setting up...

  For the GPT and and DALL-E commands to work, you will need to get an API key for OpenAI's API, wich you can get here: https://platform.openai.com/overview
  and paste the key in the "secret.py" file.
  
  As for the music commands, you will need to have a Lavalink server running. Download the Lavalink.jar [here](https://github.com/freyacodes/Lavalink/releases) (Note that you'll need at least Java 13 to run a Lavalink server) and copy the application.yml file present [here](https://github.com/freyacodes/Lavalink/blob/master/LavalinkServer/application.yml.example) and paste everything in the same folder your code is in. After you've downloaded everything, you can simply run the Lavalink server with the command ```java --jar Lavalink.jar```
  
  Now that everything is set up, you can run your Shikinha Bot! just run ```python Shikinha.py``` and have fun!
