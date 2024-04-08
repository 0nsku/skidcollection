import json

def get_prefix(ctx):
    try:
        with open("data/prefixes.json", "r") as f:
            prefixes = json.load(f)
        px = prefixes[str(ctx.message.guild.id)]
    except:
        px = ";"
    return px