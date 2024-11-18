from nextcord.ext import commands
from nextcord import Interaction
import nextcord
from Config import ConfigLoader


class AssignColour(commands.Cog):
    def __init__(self, client):
        self.client = client
    
    testserverid = 554737777049206794

    @nextcord.slash_command(name = "test",description = "intro",guild_ids=[testserverid])
    async def test(self,interaction : Interaction):
        await interaction.response.send_message("test",view=DropdownView(interaction))
class DropdownView(nextcord.ui.View):
    def __init__(self,interaction):
        super().__init__()
        self.add_item(ColourDropdown(interaction))

class ColourDropdown(nextcord.ui.Select):
    def __init__(self, interaction : Interaction):
        select_options = []
        for i in ConfigLoader.Config.config["colour"]:
            try:
                role = interaction.guild.get_role(int(i))
                select_options.append(nextcord.SelectOption(label=role.name,description=role.colour))
            except:
                continue
        super().__init__(placeholder="none",min_values=1,max_values=1,options=select_options)
    
    async def callback(self, interaction: Interaction) -> None:
        await interaction.response.send_message("succeded")