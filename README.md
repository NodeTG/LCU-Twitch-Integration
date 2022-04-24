## LCU / Twitch Integration Mod
This mod integrates with LEGO City Undercover and Twitch to allow viewers of a livestream of the game to spend their channel points in order to redeem various effects on the streamer's game.

## Explanation and Examples
Channel points are gained by watching a certain streamer for long periods of time, and consistently, as well as through methods such as following or subscribing. Streamers can create custom "rewards" that people can redeem using their points. This mod takes advantage of this, and allows you to make rewards that have actual effects inside the streamer's game.

For example, you could kill the player, teleport them randomly across the map, spawn a mountain of vehicles on their head, or just spawn a bunch of money around them. The possibilities are (almost) endless.

This mod was first used on 23/04/22 in a stream by DjOrtho. You can view that stream in full here: https://www.twitch.tv/videos/1464786737

## Where do I get it?
What I've provided in this repo is essentially the bare bones skeleton of the mod. Essentially, it's designed for a developer to take and build up their own features into, rather than being something that any random person can pick up and use.

This is partly because configuring and running the Twitch bot isn't the most user-friendly process in the world, and also because I don't really feel like cleaning up all the code I used in the stream(s) by Dj. That being said, I will still upload the code I used purely as an example for what can be done. This is not available at time of writing, but will be uploaded soon (after I finish cleaning the rest of the code).

## I'm a developer - how do I use it?
I'd like to just say "figure it out yourself", but even I think the thing is a mess, so I doubt that'd go down well with you.

For starters, the code provided in this repo includes, as mentioned, the bare minimum needed for the mod, and includes an example .SF file with a "kill players" effect built in as an example for how redemptions should be added.

In terms of dependencies, you'll obviously need Python. I used Python 3.10, but anything later than at least 3.6 should work (though there is a match: case statement in my example code, with requires 3.10).
You will also need to install the following modules:

 - `pymeow`
 - `twitchio`

To install the .SF file, for running the script in-game:

 1. Extract the game files using QuickBMS
 2. Copy the example `LEVEL31.SF` file to `LEVELS\LEGO_CITY\LEGO_CITY\AI`
 3. Add the line `level31` to `LEVELS\LEGO_CITY\LEGO_CITY\AI\SCRIPT.TXT`

In order to use the mod inside levels, you should repeat steps 2 and 3 for the AI folder of every level in the game, or only the levels that you need to be enabled (in my case, I only needed to do the first four levels and the last level).

To configure the Python side of the mod, you need to fill in some information inside a file called `config.json`
You can get some of this information from the following site: https://twitchtokengenerator.com/
(I know very little about the Twitch API, so I cannot  help much with this)
 - `"TOKEN"` - the OAuth token for your bot (ensure it has read/write chat and read redemptions permissions)
 - `"CLIENT_ID"` - the client id for your bot
 - `"BOT_PREFIX` - the prefix to use for commands in the bot, e.g. "?" or "!"
 - `"CHANNEL"` - the name of the channel to run the bot on
 - `"CHANNEL_ID"` - the id of the channel to run the bot on
 - `QUEUE_DELAY"` - how much time between each redemption being executed from the queue (can be changed at runtime)
 - `"QUEUE_TYPE"` - whether to execute redemptions in order or randomly ("LINEAR" or "RANDOM", can be changed at runtime)
 - `"QUEUE_ALERTS"` - whether to display messages when redemptions are added/executed (can be changed at runtime)

Once you have configured the bot, run it using `bot.py`
Make sure to run `?setup` in chat before using it, and that the game is running before you launch the bot.

## Final Thoughts
This repo is in its early stages. I'd like to clean up the code a whole lot more before calling it done, and make it a lot friendlier towards developers who are interested in using the code.
Speaking of which, I am obviously completely fine with people using and building on the code here. However, if you could credit me for being the original source, that would be greatly appreciated.

I also plan to include a section here with useful tips related to modding the game, such as making in-game messages for when a reward is triggered, as well as a quick-fire tutorial on how to use .SF files, as I know very few people are familiar with their structure.

Thanks to DjOrtho for being the original source of motivation for me to make this, and for doing a great job showing it off. Also a big thanks to everyone who participated in the stream(s) - it would be completely pointless if nobody used it, so thanks a lot for bringing chaos :)

And, while I wasn't actually aware of it at the time, I'd like to give a small mention to a very similar mod for Super Mario Odyssey that happened to gain attention around the time I started working on this. I took a few ideas for redemption rewards from the mod after I noticed it, so thanks to Amethyst for that! (anyone who has not seen these videos but is interested in this kind of mod concept should definitely check them out)