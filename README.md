# Axio

## Very awesome discord selfbot

Axio is a sequel to [https://github.com/vined-underscore/VBot](VBot).
> Axio has 60+ commands and it supports multiple accounts at once.
> It uses embeds (with links) instead of normal messages as responses to commands.

## How to use

1. Install Python 3.11 or 3.12
2. Run setup.bat
3. You do not need to install and fix discord.py-self manually as it is already in the repository.
4. Put your tokens in ./configs/tokens.json, the `main` part is where you should put your main account and for your alts you have to put them in the `others` part.
-  This is how it should look like:
```py
{
    "tokens": {
        "main": "tokenmain",
        "other": [
          "tokenalt1",
          "tokenalt2"
        ]
    }
}
```

5. Run axio.py, it will create config folders and you can modify the config.json files for each respective account


### TODO:
1. Account nuker
2. More commands
