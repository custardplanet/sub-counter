# Gift Sub Counter

This is a small Twitch chat bot that can track gift subs in your channel, let viewers vote toward options using their gift subs, and optionally say a message in chat when a user has cumulatively gifted a certain amount of subs (configured by you). The number of subs is stored in a sqlite3 database, which you can query to review which users have gifted however many subs.

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
Next, you need to get the code onto your computer. If you're familiar with git, clone the repository. If you're not familiar with git, look for the "Clone or Download" button on this page, click it, and click Download ZIP. Extract the folder in that zip file to somewhere on your computer (e.g. your user folder, `C:/Users/Tom/sub-counter-master`).

Inside of this folder, you will find a file called `config.json.dist`. Rename this file to `config.json` and open it with a text editor (e.g. Notepad, Notepad++, Sublime Text 3).

- Change the `channel` value to the name of your channel on Twitch (lower case only)
- Change the `nick` value to the name of the account (in lower case) you would like to say the messages in chat (your own username, or your bot. This will not work with a bot like Nightbot, only a bot you control the account of).
- Change the `subgoal` value to the number of subs you would like to trigger a message. Set to 0 if you don't want any messages triggered.
- Change the `message` value to the message you would like the bot to say when someone gifts `subgoal` number of subs. `{username}` will be replaced with the users username in the message. Leave this blank (empty quotes `""`) if you don't want a message displayed.
- To get the value of the `oauth` field, visit [this webpage](https://www.twitchapps.com/tmi/). Make sure you're signed in as the account you want to use (likely your bot account), click Connect, then Authorize, and then get the value from the next page.
- Change the `successful_vote_message` field to whatever message you'd like displayed after a successful vote.
- Update the `admins` list to a list of users (likely moderators of your channel) who will have the ability to manually vote for users if they're having trouble doing it themselves for some reason.
- Change the `options` value to a list of options your viewers will vote toward, formatted as follows, e.g. `["blue", "green", "red"]`

Here is what a completed `config.json` file will look like
```
{
    "server": "irc.chat.twitch.tv",
    "port": 6667,
    "channel": "spoongalaxy",
    "nick": "barkeith",
    "oauth": "oauth:asdfjkl123456",
    "subgoal": "5",
    "message": "Thank you {username} for gifting those subs! Please message a moderator to redeem your reward.",
    "failed_vote_message": "Sorry {username}, you don't have any points to vote with!",
    "successful_vote_message": "Thank you for voting for {option}!",
    "admins": ["spoongalaxy", "coruscating"]
    "options": ["foo", "bar", "baz"]
}
```

## Run the bot
To run the bot, open a command prompt and change directories to the location of the files from the previous step. When you open a command prompt, you will be on the C: drive by default. If you are storing the files on a different drive, for example your F: drive, first type `F:` in the command prompt to change to that drive before executing the following command.
```
cd \Users\Tom\sub-counter-master
```
Execute the script by typing `python bot.py`.

The counters of votes toward various options will be found in separate text files in the `counters` subdirectory. You can point OBS text sources at these files to display the counters on your stream.

If you find that you would like to reset sub numbers (perhaps per stream, weekly, or monthly), simply delete the `subs.db` file that is created in the directory with the other files.

## Commands
- `!vote <option>` allows a user to vote for an option. Example: `!vote blue`
- `!adminvote <username> <option> <points>` allows a channel admin to manually vote if a viewer is having trouble for whatever reason. Example: `!adminvote twitchfan69 blue 5` if you want to vote 5 points from twitchfan69 toward the blue option.

## View the data
If you'd like to review how many subs users have gifted in your channel while the bot was running, you can do so by running the provided export script (change directories to the folder containing the script as in the previous step).
```
python export_to_csv.py
```
This will create a csv export from the sqlite database that you can open with Excel or similar. Of course, you can also query the sqlite database directly, if you're familiar with how to do that.
