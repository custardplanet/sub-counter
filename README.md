# Gift Sub Counter

This is a small Twitch chat bot that can track gift subs in your channel, and say a message in chat when a user has gifted a certain amount of subs (configured by you). The number of subs is stored in a sqlite3 database, which you can query to review which users have gifted however many subs.

## Installation
These instructions are intended for Windows 10. You can obviously run this on Linux as well, but if you have the means to do that, you probably don't need setup instructions.

### Python 3
First, install Python 3. I recommend installing the latest version of Python 3, found [here](https://www.python.org/downloads/windows/). Download the Windows x86-64 executable installer, and run it. Check the box on the installation splash screen to "Add Python 3.8 to PATH", and then click "Install Now".

Once it finishes, open up a command prompt (search for the program called Command Prompt in the Windows menu) and type `python --version`, which should produce some output showing the version of Python you just installed, indicating the installation was successful.
```
C:\Users\Tom>python --version
Python 3.8.2
```
### Configuration
Next, you need to get the code onto your computer. If you're familiar with git, clone the repository. If you're not familiar with git, look for the "Clone or Download" button, click it, and click Download ZIP. Extract the folder in that zip file to somewhere on your computer (e.g. your user folder, `C:/Users/Tom/sub-counter-master`).

Inside of this folder, you will find a file called `config.json.dist`. Rename this file to `config.json` and open it with a text editor (e.g. Notepad, Notepad++, Sublime Text 3).

- Change the `channel` value to the name of your channel on Twitch.
- Change the `nick` value to the name of the account you would like to say the messages in chat (your own username, or your bot. This will not work with a bot like Nightbot, only a bot you control the account of).
- Change the `subgoal` value to the number of subs you would like to trigger a message.
- Change the `message` value to the message you would like the bot to say when someone gifts `subgoal` number of subs.
- To get the value of the `oauth` field, visit [this webpage](https://www.twitchapps.com/tmi/). Make sure you're signed in as the account you want to use, click Connect, then Authorize, and then get the value from the next page.

Here is what a completed `config.json` file will look like
```
{
    "server": "irc.chat.twitch.tv",
    "port": 6667,
    "channel": "spoongalaxy",
    "nick": "barkeith",
    "oauth": "oauth:asdfjkl123456",
    "subgoal": "5",
    "message": "Thank you so much for gifting those subs! Please message a moderator to redeem your reward."
}
```

## Run the bot
To run the bot, open a command prompt and change directories to the location of the files from the previous step.
```
cd \Users\Tom\sub-counter-master
```
Execute the script by typing `python bot.py`.
