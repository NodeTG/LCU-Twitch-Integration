import asyncio
import random
from twitchio.ext import pubsub, commands
import logging
import json
import datetime
import lcu_mod

# TODO: cleanup code so it doesn't make my eyes bleed, and so that it doesn't suck as much

with open("config.json", "r") as cfg:
    config = json.load(cfg)
    queue_delay = config["QUEUE_DELAY"]
    queue_type = config["QUEUE_TYPE"]
    queue_alerts = bool(config["QUEUE_ALERTS"])

bot = commands.Bot(token = config["TOKEN"], prefix = config["BOT_PREFIX"], initial_channels=[config["CHANNEL"]])
bot.pubsub = pubsub.PubSubPool(bot)
setup_complete = False
channel = None
frozen = False
stopped = False
moderators = ["djortho", "nodetg"]  # Put Twitch usernames in here of people you want to be able to control the bot (TODO: move to config.json)

@bot.event()
async def event_pubsub_channel_points(event: pubsub.PubSubChannelPointsMessage):
    if event.reward.id in lcu_mod.effect_reference.keys():
        if not frozen:
            lcu_mod.effect_queue.append((lcu_mod.effect_reference[event.reward.id], event.user.name))
            logging.info(f"[EVENT] New effect in queue: {lcu_mod.effect_reference[event.reward.id]}")
        else:
            logging.info(f"[EVENT] Couldn't handle event due to frozen queue! User name: {event.user.name}, timestamp: {event.timestamp}")

        if queue_alerts and channel is not None and not frozen:
            await channel.send(f"[BOT] {event.user.name} I've added your effect to the queue! \
            Your request is in position {len(lcu_mod.effect_queue)} (approximately {queue_delay * len(lcu_mod.effect_queue)} seconds away).")
        elif queue_alerts and channel is not None and frozen:
            await channel.send(f"[BOT] {event.user.name} Sorry! The queue has been frozen! Your points will be refunded by a moderator.")
    else:
        logging.info(f"[EVENT] Unknown redemption! ID: {event.reward.id} | Name: {event.reward.title}")

@bot.command(name="queue")
async def queue(ctx: commands.Context):
    if ctx.author.name.lower() not in moderators:
        await ctx.send(f"[BOT] There are {len(lcu_mod.effect_queue)} items in the queue!")
    else:
        try:
            await ctx.send(f"[BOT] Here is the queue: {lcu_mod.effect_queue} ({len(lcu_mod.effect_queue)} items)")
        except:
            await ctx.send(f"[BOT] There are {len(lcu_mod.effect_queue)} items in the queue (cannot print queue contents due to size)!")

@bot.command(name="queue-mode")
async def queue_mode(ctx: commands.Context, mode: str):
    global queue_type
    if ctx.author.name.lower() not in moderators:
        return

    if mode == "LINEAR" or mode == "RANDOM":
        queue_type = mode
        await ctx.send(f"[BOT] Queue mode set to: {mode}")
    else:
        await ctx.send(f"[BOT] Cannot set the queue to mode: {mode}")

@bot.command(name="queue-delay")
async def queue_delay_set(ctx: commands.Context, delay: int):
    global queue_delay
    if ctx.author.name.lower() not in moderators:
        return
    
    queue_delay = delay
    await ctx.send(f"[BOT] Queue delay set to: {delay}")

@bot.command(name="queue-priority")
async def queue_priority(ctx: commands.Context, index: int):
    if ctx.author.name.lower() not in moderators:
        return
    
    if queue_type == "RANDOM":
        await ctx.send("[BOT] Cannot give priority; queue is in RANDOM mode!")
    else:
        effect = lcu_mod.effect_queue.pop(index)
        lcu_mod.effect_queue.insert(0, effect)
        await ctx.send(f"[BOT] Gave priority to effect {effect} at index {index}!")
    
@bot.command(name="queue-add")
async def queue_add(ctx: commands.Context, effect: int, priority: bool = False):
    if ctx.author.name.lower() not in moderators:
        return
    
    if priority:
        lcu_mod.effect_queue.insert(0, (effect, ctx.author.name))
        await ctx.send(f"[BOT] Added effect with ID {effect} to the queue (priority!)")
    else:
        lcu_mod.effect_queue.append((effect, ctx.author.name))
        await ctx.send(f"[BOT] Added effect with ID {effect} to the queue!")

@bot.command(name="queue-remove")
async def queue_remove(ctx: commands.Context, index: int):
    if ctx.author.name.lower() not in moderators:
        return
    
    await ctx.send(f"[BOT] Removed effect with ID {lcu_mod.effect_queue.pop(index)} at index {index} from the queue!")

@bot.command(name="toggle-alerts")
async def toggle_alerts(ctx: commands.Context):
    global queue_alerts
    if ctx.author.name.lower() not in moderators:
        return
    
    queue_alerts = not queue_alerts
    await ctx.send(f"[BOT] Toggled alerts to: {queue_alerts}")

@bot.command(name="add-random")
async def add_random(ctx: commands.Context, amount: int):
    if ctx.author.name.lower() not in moderators:
        return
    for i in range(amount):
        lcu_mod.effect_queue.append((random.randint(1001,1014), ctx.author.name))
    await ctx.send(f"[BOT] Added {amount} random effects to the queue!")

@bot.command(name="stop")
async def stop_queue(ctx: commands.Context, toggle: bool):
    global stopped
    if ctx.author.name.lower() not in moderators:
        return
    
    stopped = toggle
    await ctx.send(f"[BOT] Set queue stopped state to: {stopped}")

@bot.command(name="freeze")
async def freeze_queue(ctx: commands.Context, toggle: bool):
    global frozen
    if ctx.author.name.lower() not in moderators:
        return
    
    frozen = toggle
    await ctx.send(f"[BOT] Set queue frozen state to: {frozen}")

@bot.command(name="setup")
async def setup(ctx: commands.Context):
    global setup_complete, channel
    if ctx.author.name.lower() not in moderators:
        return
    if not setup_complete:
        topics = [
            pubsub.channel_points(config["TOKEN"])[config["CHANNEL_ID"]]
        ]
        await bot.pubsub.subscribe_topics(topics)
        channel = bot.get_channel("DjOrtho")
        await channel.send(f"[BOT] We're good to go!")
        setup_complete = True
    else:
        await channel.send("[BOT] We're already good to go!")

async def handle_queue():
    global channel
    try:
        await lcu_mod.initialise()
    except Exception as e:
        return logging.error(f"[ERROR] Could not find LEGOLCUR_DX11.exe! Make sure the game is running!\n{e}")
    while True:
        logging.info(f'[QUEUE] waiting {queue_delay} seconds')
        await asyncio.sleep(queue_delay)
        logging.info("[QUEUE] delay passed")
        if len(lcu_mod.effect_queue) >= 1 and not stopped:
            if queue_type == "LINEAR":
                effect_to_send = lcu_mod.effect_queue.pop(0)
            elif queue_type == "RANDOM":
                effect_to_send = lcu_mod.effect_queue.pop(random.randint(0, len(lcu_mod.effect_queue) - 1))
            else:
                effect_to_send = lcu_mod.effect_queue.pop(0)
    
            logging.info(f"[QUEUE]  - queue not empty ({effect_to_send}), waiting")
            await lcu_mod.wait_until_ready()
            logging.info("[QUEUE]  - sending message")
            
            logging.info("[QUEUE]  - writing and waiting\n")

            try: 
                if channel is not None and queue_alerts: 
                    await channel.send(f"[BOT] Executing Effect: `{lcu_mod.effect_text[effect_to_send[0]]}` ({effect_to_send[1]})")

                await lcu_mod.write_data_value(effect_to_send[0], True)
            except:
                logging.error(f"[ERROR] Failed to write effect {effect_to_send}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, handlers=[logging.FileHandler(f"logs\\{str(datetime.datetime.now()).replace(':','')}.txt"), logging.StreamHandler()],
                        format="%(asctime)s : %(levelname)s:%(module)s:%(lineno)d -  %(message)s")

    bot.loop.create_task(handle_queue())
    bot.loop.create_task(bot.run())
    bot.loop.run_forever()