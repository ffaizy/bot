from discord.ext import commands
import json
import random

Bot = commands.Bot(command_prefix="!")


@Bot.event
async def on_ready():
    print(f"logged on as {Bot.user}")


@Bot.event
async def on_message(message):
    print(f"{message.guild} -> {message.channel} -> {message.author}: {message.content}")
    await Bot.process_commands(message)


@Bot.command()
async def fact(ctx, num, mode="RANDOM"):
    """display fact from database, `random` or `all`"""

    if not num.isdigit():
        await ctx.send(f"{num} is not a number")
        return

    mode = mode.upper()
    if mode not in ["ALL", "RANDOM"]:
        await ctx.send(f"{mode} is not a valid mode, valid modes are: `RANDOM` and `ALL`")
        return

    with open("facts.json") as f:
        data = json.load(f)

    if num in data:
        if mode == "RANDOM":
            await ctx.send(random.choice(data[num]))
        elif mode == "ALL":
            for i, fact_ in enumerate(data[num]):
                await ctx.send(f"{i} | {fact_}")

    else:
        await ctx.send(f"{num} does not have any facts add some using \n"
                       f"`!add {num} [fact]`")


@Bot.command()
async def add(ctx, num, *fact_):
    """add fact to data base"""

    if not num.isdigit():
        await ctx.send(f"{num} is not a number")
        return

    fact_ = " ".join(fact_)
    with open("facts.json") as f:
        data = json.load(f)

    if num not in data:
        data[num] = []
    data[num].append(fact_)

    with open("facts.json", "w") as f:
        json.dump(data, f)

    await ctx.send(f"add fact about {num}:\n"
                   f"`{fact_}`")


@Bot.command()
async def remove(ctx, num, fact_index):
    """remove a fact from a number at a index, see al indexes with `!fact number ALL`"""

    if not num.isdigit():
        await ctx.send(f"{num} is not a number")
        return

    if not fact_index.isdigit():
        await ctx.send(f"{fact_index} is not a number")
        return

    with open("facts.json") as f:
        data = json.load(f)

    try:
        fact_ = data[num].pop(int(fact_index))
    except IndexError:
        await ctx.send(f"{fact_index} is a to big index")
    except KeyError:
        await ctx.send(f"{num} does not have any facts")
    else:
        await ctx.send(f"removed fact `{fact_}` about {num}")
        if len(data[num]) == 0:
            del data[num]

        with open("facts.json", "w") as f:
            json.dump(data, f)


if __name__ == "__main__":
    Bot.run("token")
