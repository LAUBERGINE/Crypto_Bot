import discord
import requests
import asyncio

TOKEN = '[TOKEN DISCORD]'
SERVER_ID = '[YOUR SERVER]'
CHANNEL_ID = '[YOUR CHANNEL]'

intents = discord.Intents.default()
intents.messages = True

client = discord.Client(intents=intents)

async def fetch_crypto_data():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin,ethereum&vs_currencies=usd&include_24hr_change=true"
    response = requests.get(url)
    data = response.json()
    return data

async def send_crypto_price():
    data = await fetch_crypto_data()
    btc_price = data['bitcoin']['usd']
    btc_change = data['bitcoin']['usd_24h_change']
    eth_price = data['ethereum']['usd']
    eth_change = data['ethereum']['usd_24h_change']

    channel = client.get_channel(int(CHANNEL_ID))
    if channel:
        embtc = discord.Embed(colour=discord.Colour.gold(), title='<:Bitcoin:1235650542643187823> BITCOIN')
        embtc.add_field(name="**Prix actuel**", value=f"{btc_price}$", inline=False)
        embtc.add_field(name="**Variation 24h**", value=f"{btc_change}%", inline=False)
        
        emeth = discord.Embed(colour=discord.Colour.dark_gray(), title='<:Ethereum:1235650579095748649> ETHEREUM')
        emeth.add_field(name="**Prix actuel**", value=f"{eth_price}$", inline=False)
        emeth.add_field(name="**Variation 24h**", value=f"{eth_change}%", inline=False)
        
        await channel.send(embed=embtc)
        await channel.send(embed=emeth)

async def main():
    while True:
        await send_crypto_price()
        await asyncio.sleep(3600)

@client.event
async def on_ready():
    print("Attack on Eggplants")
    print(f'Logged in as {client.user}')
    asyncio.create_task(main())

client.run(TOKEN)

