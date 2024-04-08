import discord
from discord.ext import commands
import random
import asyncio

class Flags(commands.Cog):
    def __init__(self, bot: commands.AutoShardedBot):
        self.bot = bot
        self.flags_per_round = 10
        self.round_duration = 20
        self.rounds = 10
        self.active_game = False
        self.countries = [
                {"name": "Afghanistan", "code": "AF"},
    {"name": "Aland Islands", "code": "AX"},
    {"name": "Albania", "code": "AL"},
    {"name": "Algeria", "code": "DZ"},
    {"name": "American Samoa", "code": "AS"},
    {"name": "Andorra", "code": "AD"},
    {"name": "Angola", "code": "AO"},
    {"name": "Anguilla", "code": "AI"},
    {"name": "Antarctica", "code": "AQ"},
    {"name": "Antigua and Barbuda", "code": "AG"},
    {"name": "Argentina", "code": "AR"},
    {"name": "Armenia", "code": "AM"},
    {"name": "Aruba", "code": "AW"},
    {"name": "Australia", "code": "AU"},
    {"name": "Austria", "code": "AT"},
    {"name": "Azerbaijan", "code": "AZ"},
    {"name": "Bahamas", "code": "BS"},
    {"name": "Bahrain", "code": "BH"},
    {"name": "Bangladesh", "code": "BD"},
    {"name": "Barbados", "code": "BB"},
    {"name": "Belarus", "code": "BY"},
    {"name": "Belgium", "code": "BE"},
    {"name": "Belize", "code": "BZ"},
    {"name": "Benin", "code": "BJ"},
    {"name": "Bermuda", "code": "BM"},
    {"name": "Bhutan", "code": "BT"},
    {"name": "Bolivia", "code": "BO"},
    {"name": "Bosnia and Herzegovina", "code": "BA"},
    {"name": "Botswana", "code": "BW"},
    {"name": "Bouvet Island", "code": "BV"},
    {"name": "Brazil", "code": "BR"},
    {"name": "British Indian Ocean Territory", "code": "IO"},
    {"name": "Brunei Darussalam", "code": "BN"},
    {"name": "Bulgaria", "code": "BG"},
    {"name": "Burkina Faso", "code": "BF"},
    {"name": "Burundi", "code": "BI"},
    {"name": "Cambodia", "code": "KH"},
    {"name": "Cameroon", "code": "CM"},
    {"name": "Canada", "code": "CA"},
    {"name": "Cape Verde", "code": "CV"},
    {"name": "Cayman Islands", "code": "KY"},
    {"name": "Central African Republic", "code": "CF"},
    {"name": "Chad", "code": "TD"},
    {"name": "Chile", "code": "CL"},
    {"name": "China", "code": "CN"},
    {"name": "Christmas Island", "code": "CX"},
    {"name": "Cocos Islands", "code": "CC"},
    {"name": "Colombia", "code": "CO"},
    {"name": "Comoros", "code": "KM"},
    {"name": "Congo", "code": "CG"},
    {"name": "Democratic Republic of the Congo", "code": "CD"},
    {"name": "Cook Islands", "code": "CK"},
    {"name": "Costa Rica", "code": "CR"},
    {"name": "Cote D'Ivoire", "code": "CI"},
    {"name": "Croatia", "code": "HR"},
    {"name": "Cuba", "code": "CU"},
    {"name": "Cyprus", "code": "CY"},
    {"name": "Czech Republic", "code": "CZ"},
    {"name": "Denmark", "code": "DK"},
    {"name": "Djibouti", "code": "DJ"},
    {"name": "Dominica", "code": "DM"},
    {"name": "Dominican Republic", "code": "DO"},
    {"name": "Ecuador", "code": "EC"},
    {"name": "Egypt", "code": "EG"},
    {"name": "El Salvador", "code": "SV"},
    {"name": "Equatorial Guinea", "code": "GQ"},
    {"name": "Eritrea", "code": "ER"},
    {"name": "Estonia", "code": "EE"},
    {"name": "Ethiopia", "code": "ET"},
    {"name": "Falkland Islands (Malvinas)", "code": "FK"},
    {"name": "Faroe Islands", "code": "FO"},
    {"name": "Fiji", "code": "FJ"},
    {"name": "Finland", "code": "FI"},
    {"name": "France", "code": "FR"},
    {"name": "French Guiana", "code": "GF"},
    {"name": "French Polynesia", "code": "PF"},
    {"name": "French Southern Territories", "code": "TF"},
    {"name": "Gabon", "code": "GA"},
    {"name": "Gambia", "code": "GM"},
    {"name": "Georgia", "code": "GE"},
    {"name": "Germany", "code": "DE"},
    {"name": "Ghana", "code": "GH"},
    {"name": "Gibraltar", "code": "GI"},
    {"name": "Greece", "code": "GR"},
    {"name": "Greenland", "code": "GL"},
    {"name": "Grenada", "code": "GD"},
    {"name": "Guadeloupe", "code": "GP"},
    {"name": "Guam", "code": "GU"},
    {"name": "Guatemala", "code": "GT"},
    {"name": "Guernsey", "code": "GG"},
    {"name": "Guinea", "code": "GN"},
    {"name": "Guinea-Bissau", "code": "GW"},
    {"name": "Guyana", "code": "GY"},
    {"name": "Haiti", "code": "HT"},
    {"name": "Heard Island and Mcdonald Islands", "code": "HM"},
    {"name": "Vatican City", "code": "VA"},
    {"name": "Honduras", "code": "HN"},
    {"name": "Hong Kong", "code": "HK"},
    {"name": "Hungary", "code": "HU"},
    {"name": "Iceland", "code": "IS"},
    {"name": "India", "code": "IN"},
    {"name": "Indonesia", "code": "ID"},
    {"name": "Iran", "code": "IR"},
    {"name": "Iraq", "code": "IQ"},
    {"name": "Ireland", "code": "IE"},
    {"name": "Isle of Man", "code": "IM"},
    {"name": "Israel", "code": "IL"},
    {"name": "Italy", "code": "IT"},
    {"name": "Jamaica", "code": "JM"},
    {"name": "Japan", "code": "JP"},
    {"name": "Jersey", "code": "JE"},
    {"name": "Jordan", "code": "JO"},
    {"name": "Kazakhstan", "code": "KZ"},
    {"name": "Kenya", "code": "KE"},
    {"name": "Kiribati", "code": "KI"},
    {"name": "North Korea", "code": "KP"},
    {"name": "South Korea", "code": "KR"},
    {"name": "Kuwait", "code": "KW"},
    {"name": "Kyrgyzstan", "code": "KG"},
    {"name": "Laos", "code": "LA"},
    {"name": "Latvia", "code": "LV"},
    {"name": "Lebanon", "code": "LB"},
    {"name": "Lesotho", "code": "LS"},
    {"name": "Liberia", "code": "LR"},
    {"name": "Libyan Arab Jamahiriya", "code": "LY"},
    {"name": "Liechtenstein", "code": "LI"},
    {"name": "Lithuania", "code": "LT"},
    {"name": "Luxembourg", "code": "LU"},
    {"name": "Macao", "code": "MO"},
    {"name": "Macedonia", "code": "MK"},
    {"name": "Madagascar", "code": "MG"},
    {"name": "Malawi", "code": "MW"},
    {"name": "Malaysia", "code": "MY"},
    {"name": "Maldives", "code": "MV"},
    {"name": "Mali", "code": "ML"},
    {"name": "Malta", "code": "MT"},
    {"name": "Marshall Islands", "code": "MH"},
    {"name": "Martinique", "code": "MQ"},
    {"name": "Mauritania", "code": "MR"},
    {"name": "Mauritius", "code": "MU"},
    {"name": "Mayotte", "code": "YT"},
    {"name": "Mexico", "code": "MX"},
    {"name": "Micronesia", "code": "FM"},
    {"name": "Moldova, Republic of", "code": "MD"},
    {"name": "Monaco", "code": "MC"},
    {"name": "Mongolia", "code": "MN"},
    {"name": "Montserrat", "code": "MS"},
    {"name": "Morocco", "code": "MA"},
    {"name": "Mozambique", "code": "MZ"},
    {"name": "Myanmar", "code": "MM"},
    {"name": "Namibia", "code": "NA"},
    {"name": "Nauru", "code": "NR"},
    {"name": "Nepal", "code": "NP"},
    {"name": "Netherlands", "code": "NL"},
    {"name": "Netherlands Antilles", "code": "AN"},
    {"name": "New Caledonia", "code": "NC"},
    {"name": "New Zealand", "code": "NZ"},
    {"name": "Nicaragua", "code": "NI"},
    {"name": "Niger", "code": "NE"},
    {"name": "Nigeria", "code": "NG"},
    {"name": "Niue", "code": "NU"},
    {"name": "Norfolk Island", "code": "NF"},
    {"name": "Northern Mariana Islands", "code": "MP"},
    {"name": "Norway", "code": "NO"},
    {"name": "Oman", "code": "OM"},
    {"name": "Pakistan", "code": "PK"},
    {"name": "Palau", "code": "PW"},
    {"name": "Palestine", "code": "PS"},
    {"name": "Panama", "code": "PA"},
    {"name": "Papua New Guinea", "code": "PG"},
    {"name": "Paraguay", "code": "PY"},
    {"name": "Peru", "code": "PE"},
    {"name": "Philippines", "code": "PH"},
    {"name": "Pitcairn", "code": "PN"},
    {"name": "Poland", "code": "PL"},
    {"name": "Portugal", "code": "PT"},
    {"name": "Puerto Rico", "code": "PR"},
    {"name": "Qatar", "code": "QA"},
    {"name": "Reunion", "code": "RE"},
    {"name": "Romania", "code": "RO"},
    {"name": "Russian Federation", "code": "RU"},
    {"name": "Rwanda", "code": "RW"},
    {"name": "Saint Helena", "code": "SH"},
    {"name": "Saint Kitts and Nevis", "code": "KN"},
    {"name": "Saint Lucia", "code": "LC"},
    {"name": "Saint Pierre and Miquelon", "code": "PM"},
    {"name": "Saint Vincent and the Grenadines", "code": "VC"},
    {"name": "Samoa", "code": "WS"},
    {"name": "San Marino", "code": "SM"},
    {"name": "Sao Tome and Principe", "code": "ST"},
    {"name": "Saudi Arabia", "code": "SA"},
    {"name": "Senegal", "code": "SN"},
    {"name": "Serbia and Montenegro", "code": "CS"},
    {"name": "Seychelles", "code": "SC"},
    {"name": "Sierra Leone", "code": "SL"},
    {"name": "Singapore", "code": "SG"},
    {"name": "Slovakia", "code": "SK"},
    {"name": "Slovenia", "code": "SI"},
    {"name": "Solomon Islands", "code": "SB"},
    {"name": "Somalia", "code": "SO"},
    {"name": "South Africa", "code": "ZA"},
    {"name": "South Georgia and the South Sandwich Islands", "code": "GS"},
    {"name": "Spain", "code": "ES"},
    {"name": "Sri Lanka", "code": "LK"},
    {'name': 'Sudan', 'code': 'SD'},
    {'name': 'Suriname', 'code': 'SR'},
    {'name': 'Svalbard and Jan Mayen', 'code': 'SJ'},
    {'name': 'Swaziland', 'code': 'SZ'},
    {'name': 'Sweden', 'code': 'SE'},
    {'name': 'Switzerland', 'code': 'CH'},
    {'name': 'Syria', 'code': 'SY'},
    {'name': 'Taiwan', 'code': 'TW'},
    {'name': 'Tajikistan', 'code': 'TJ'},
    {'name': 'Tanzania, United Republic of', 'code': 'TZ'},
    {'name': 'Thailand', 'code': 'TH'},
    {'name': 'Timor-Leste', 'code': 'TL'},
    {'name': 'Togo', 'code': 'TG'},
    {'name': 'Tokelau', 'code': 'TK'},
    {'name': 'Tonga', 'code': 'TO'},
    {'name': 'Trinidad and Tobago', 'code': 'TT'},
    {'name': 'Tunisia', 'code': 'TN'},
    {'name': 'Turkey', 'code': 'TR'},
    {'name': 'Turkmenistan', 'code': 'TM'},
    {'name': 'Turks and Caicos Islands', 'code': 'TC'},
    {'name': 'Tuvalu', 'code': 'TV'},
    {'name': 'Uganda', 'code': 'UG'},
    {'name': 'Ukraine', 'code': 'UA'},
    {'name': 'United Arab Emirates', 'code': 'AE'},
    {'name': 'United Kingdom', 'code': 'GB'},
    {'name': 'United States', 'code': 'US'},
    {'name': 'United States Minor Outlying Islands', 'code': 'UM'},
    {'name': 'Uruguay', 'code': 'UY'},
    {'name': 'Uzbekistan', 'code': 'UZ'},
    {'name': 'Vanuatu', 'code': 'VU'},
    {'name': 'Venezuela', 'code': 'VE'},
    {'name': 'Vietnam', 'code': 'VN'},
    {'name': 'Virgin Islands, British', 'code': 'VG'},
    {'name': 'Virgin Islands, U.S.', 'code': 'VI'},
    {'name': 'Wallis and Futuna', 'code': 'WF'},
    {'name': 'Western Sahara', 'code': 'EH'},
    {'name': 'Yemen', 'code': 'YE'},
    {'name': 'Zambia', 'code': 'ZM'},
    {'name': 'Zimbabwe', 'code': 'ZW'}
            
        ]
        self.active_game = False

    def get_random_flag(self):
        country = random.choice(self.countries)
        flag_url = f"https://flagcdn.com/w2560/{country['code'].lower()}.png"
        return flag_url, country['name']

    async def get_points(self, guild_id, user_id, round_num):
        query = "SELECT points FROM flags_scores WHERE guild_id = $1 AND user_id = $2 AND round_num = $3;"
        return await self.bot.db.fetchval(query, guild_id, user_id, round_num) or 0

    async def set_points(self, guild_id, user_id, round_num, points):
        query = "INSERT INTO flags_scores (guild_id, user_id, round_num, points) VALUES ($1, $2, $3, $4) ON CONFLICT (guild_id, user_id, round_num) DO UPDATE SET points = $4;"
        await self.bot.db.execute(query, guild_id, user_id, round_num, points)

    async def show_leaderboard(self, ctx, round_num):
        query = "SELECT user_id, SUM(points) as total_points FROM flags_scores WHERE guild_id = $1 GROUP BY user_id ORDER BY total_points DESC;"
        records = await self.bot.db.fetch(query, ctx.guild.id)

        if not records:
            await ctx.send_warning("No one scored points yet.")
            return

        leaderboard_embed = discord.Embed(color=self.bot.color)
        leaderboard_embed.title = f"Leaderboard for {ctx.guild.name}"

        leaderboard_description = ""
        for position, record in enumerate(records, start=1):
            user = ctx.guild.get_member(record['user_id'])
            if user:
                leaderboard_description += f"**{position}.** {user.mention} with **{record['total_points']}** points\n"

        leaderboard_embed.description = leaderboard_description

        await ctx.send(embed=leaderboard_embed)

    async def start_round(self, ctx, round_num):
        for current_round in range(1, self.flags_per_round + 1):
            if not self.active_game:
                break

            flag_url, correct_flag_name = self.get_random_flag()

            flag_embed = discord.Embed(color=self.bot.color)
            flag_embed.set_image(url=flag_url)
            flag_embed.set_footer(text=f"Type the full country name, you have 20 seconds to guess, this is round {current_round}/{self.flags_per_round}")

            flag_message = await ctx.send(embed=flag_embed)

            def check(message):
                return message.content.lower() == correct_flag_name.lower()

            try:
                response = await self.bot.wait_for('message', check=check, timeout=self.round_duration)
            except asyncio.TimeoutError:
                await ctx.send(embed=discord.Embed(description=f"> Time's up! The correct flag was **{correct_flag_name}**.", color=self.bot.color))
                asyncio.sleep(3)
            else:
                user = response.author
                current_points = await self.get_points(ctx.guild.id, user.id, round_num)
                new_points = current_points + 1
                await self.set_points(ctx.guild.id, user.id, round_num, new_points)
                await ctx.send(embed=discord.Embed(description=f"> {user.mention}: Correctly guessed the flag of **{correct_flag_name}**.", color=self.bot.color))
                asyncio.sleep(3)

            if current_round == self.flags_per_round or round_num == self.rounds:
                self.active_game = False
                break 

        if round_num == self.rounds:
            await ctx.send(embed=discord.Embed(description="> The game has **finished**!", color=self.bot.color))
            self.active_game = False

    @commands.group(name='flags')
    async def flags(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send_warning(f"Invalid flags command. Use `{ctx.clean_prefix}flags start` or `{ctx.clean_prefix}flags leaderboard`")

    @flags.command(name='start')
    async def flags_start(self, ctx):
        if self.active_game:
            await ctx.send_warning("A game is already in progress!")
            return

        self.active_game = True

        for round_num in range(1, self.rounds + 1):
            if not self.active_game:
                break

            await self.start_round(ctx, round_num)

        self.active_game = False
        await self.show_leaderboard(ctx, self.rounds)

    @flags.command(name='leaderboard')
    async def flags_leaderboard(self, ctx):
        await self.show_leaderboard(ctx, 1)

    @flags.command(name='stop', aliases=["end"])
    async def flags_stop(self, ctx):
        if not self.active_game:
            await ctx.send_warning("No game is currently in progress!")
            return

        self.active_game = False
        await ctx.send(embed=discord.Embed(description="> **Stopped** the **ongoing** game!", color=self.bot.color))

async def setup(bot) -> None:
    await bot.add_cog(Flags(bot))