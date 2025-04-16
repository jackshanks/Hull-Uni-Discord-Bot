import nextcord
from Bot.Cogs._BaseCog import BaseCog
import json


class RuleManager(BaseCog):
    def __init__(self, bot, db):
        super().__init__(bot, db)
        self.rule_file = "rules.json"
        self.channel_id = self.config.rule_channel
        self.channel = None

    async def on_run_rules(self):
        try:
            self.channel = self.bot.get_channel(self.channel_id)
            message_id = await self.load_message_data()
            if message_id:
                try:
                    message = await self.channel.fetch_message(message_id)
                    await message.edit(embed=await self.create_rules_embed())
                    print("Updated existing rules message")
                except nextcord.NotFound:
                    # Message not found, create new one
                    message = await self.channel.send(embed=await self.create_rules_embed())
                    await self.save_message_data(message.id)
                    print("Created new rules message (old message not found)")
            else:
                message = await self.channel.send(embed=await self.create_rules_embed())
                await self.save_message_data(message.id)
                print("Created new rules message")

        except Exception as e:
            print(f"Error handling rules message: {e}")

    async def load_message_data(self):
        """Load the message ID from file"""
        try:
            with open(self.rule_file, 'r') as f:
                data = json.load(f)
                return data.get('message_id')
        except (FileNotFoundError, json.JSONDecodeError):
            return None

    async def save_message_data(self, message_id):
        """Save the message ID to a file"""
        data = {'message_id': message_id}
        with open(self.rule_file, 'w') as f:
            json.dump(data, f)

    async def create_rules_embed(self):
        """Create the rules embed with current rules with larger, more readable text"""
        embed = nextcord.Embed(
            title="__**Community Rules**__",  # Bold and underline for emphasis
            description="**Please read and follow these rules:**\n\n",  # Bold and extra spacing
            color=nextcord.Color.blue()
        )

        default_rules = await self.db.execute("""SELECT rule FROM rules""")

        # Add rules to embed with larger text formatting
        for i, rule in enumerate(default_rules, 1):
            rule = rule[0]
            # Using markdown for larger text and better spacing
            formatted_rule = f"**{rule}**"  # Make rule text bold
            embed.add_field(
                name=f"📌 **Rule {i}**",  # Add emoji and bold text
                value=f"{formatted_rule}\n\n",  # Add extra spacing between rules
                inline=False
            )

        embed.set_footer(text="Last updated")
        # Make embed thicker by adding empty field if needed
        if len(default_rules) % 2 == 0:
            embed.add_field(name="\u200b", value="\u200b", inline=False)

        return embed
