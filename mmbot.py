import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix='$', intents=intents)


user_profits = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


class MercyView(discord.ui.View):
    def __init__(self, client_role_name: str):
        super().__init__(timeout=None)
        self.client_role_name = client_role_name

    @discord.ui.button(label="Accept", style=discord.ButtonStyle.green)
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        member = interaction.user
        role = discord.utils.get(guild.roles, name=self.client_role_name)
        if not role:
            role = await guild.create_role(name=self.client_role_name)
        await member.add_roles(role)
        await interaction.response.send_message(f"You have been given the '{self.client_role_name}' role.", ephemeral=True)

    @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message("Your banned lil nga.", ephemeral=True)

@bot.command()
async def gotraped(ctx):
    embed = discord.Embed(title="You have been scammed LIL NGA", description="If you want to join us, choose below:", color=discord.Color.red())
    embed.add_field(name="Info", value="Accept to get the client role, Decline to get refunded.")
    view = MercyView(client_role_name="client")
    await ctx.send(embed=embed, view=view)

@bot.command()
async def mmfee(ctx):
    await ctx.send('Middleman fee: split 50/50 or pay 100')


@bot.command()
async def mminfo(ctx):
    embed = discord.Embed(
        title="Middleman Information",
        description=(
            "When you use a middleman, both parties give their items/currency to the middleman. "
            "The middleman holds both until both sides confirm the trade. "
            "Once confirmed, the middleman releases the items/currency to each party. "
            "This ensures a safe and fair trade. Fees apply. Both parties must confirm."
        ),
        color=discord.Color.blue()
    )
    await ctx.send(embed=embed)


@bot.command()
async def confirm(ctx):
    class ConfirmView(discord.ui.View):
        @discord.ui.button(label="Confirm", style=discord.ButtonStyle.green)
        async def confirm_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(f"{interaction.user.mention} has Confirmed the trade!", ephemeral=False)

        @discord.ui.button(label="Decline", style=discord.ButtonStyle.red)
        async def decline_btn(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message(f"{interaction.user.mention} has Declined the trade!", ephemeral=False)

    embed = discord.Embed(title="Trade Confirmation", description="Please confirm or decline the trade.", color=discord.Color.orange())
    await ctx.send(embed=embed, view=ConfirmView())

@bot.command()
async def ask(ctx):
    await ctx.send('Please provide your Roblox usernames. Can you join a private server?')


# very simple ticket system for mm or anything in general
@bot.command()
@commands.has_permissions(administrator=True)
async def ticketpanel(ctx):
    class TicketPanel(discord.ui.View):
        @discord.ui.button(label="Create Ticket", style=discord.ButtonStyle.green)
        async def create(self, interaction: discord.Interaction, button: discord.ui.Button):
            guild = interaction.guild
            category = discord.utils.get(guild.categories, name="Requests")
            if not category:
                category = await guild.create_category("Requests")
            channel = await guild.create_text_channel(
                name=f"request-{interaction.user.name}",
                category=category,
                topic=f"Request for {interaction.user.display_name}",
            )
            await channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            await channel.set_permissions(guild.default_role, read_messages=False)
            await channel.send(f"Welcome {interaction.user.mention}! An MiddleMan will be with you shortly.")
            await interaction.response.send_message(f"Your Request has been created: {channel.mention}", ephemeral=True)
    embed = discord.Embed(title="MiddleMan Request", description="Click below to create a MiddleMan Request.", color=discord.Color.green())
    await ctx.send(embed=embed, view=TicketPanel())

# ads the clinet getting scammed or anyone to a ticket
@bot.command()
async def add(ctx, member: discord.Member):
    if ctx.channel.category and ctx.channel.category.name == "Requests":
        await ctx.channel.set_permissions(member, read_messages=True, send_messages=True)
        await ctx.send(f"{member.mention} has been added to the request.")
    else:
        await ctx.send("This command can only be used in a request channel.")

@bot.command()
async def profit(ctx, member: discord.Member = None):
    member = member or ctx.author
    profit = user_profits.get(member.id, 0)
    await ctx.send(f'{member.mention} has ${profit} profit available for middleman.')

@bot.command()
async def addprofit(ctx, member: discord.Member, amount: int):
    user_profits[member.id] = user_profits.get(member.id, 0) + amount
    await ctx.send(f'Added ${amount} to {member.mention} profit. Total: ${user_profits[member.id]}')

@bot.command()
async def removeprofit(ctx, member: discord.Member, amount: int):
    user_profits[member.id] = max(0, user_profits.get(member.id, 0) - amount)
    await ctx.send(f'Removed ${amount} from {member.mention} profit. Total: ${user_profits[member.id]}')

# put youir bot token here IDK what your token is so just put it there lol
bot.run('MTQ2NDQxODg4NDM5OTY2MTQwNA.GKmryJ.z4V_EvnR66sKSDLxq0WUVLO8U5-jt5CpTqTJdE')
