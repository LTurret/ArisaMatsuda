from io import BytesIO

from interactions import slash_command
from interactions import slash_option
from interactions import Extension
from interactions import File
from interactions import OptionType
from interactions import SlashContext
from interactions import SlashCommandChoice
from PIL import Image
from PIL import ImageChops

class goods(Extension):
    def __init__(self, Misaki):
        self.Misaki = Misaki
        print(f"↳ Extension {__name__} created")

    @slash_command(
        name = "goods",
        description = "六周年立牌產生器"
    )
    @slash_option(
        name = "idol",
        description = "偶像名",
        required = True,
        opt_type = OptionType.STRING,
    )
    @slash_option(
        name = "base",
        description = "底座樣式",
        required = False,
        opt_type = OptionType.INTEGER,
        choices=[
            SlashCommandChoice(name="普通底座", value=1),
            SlashCommandChoice(name="金色底座", value=3),
            SlashCommandChoice(name="前十底座", value=2)
        ]
    )

    async def goods(self, ctx: SlashContext, idol: str="杏奈", base: int=1):
        manifest = {
            "春香": 1,
            "千早": 2,
            "美希": 3,
            "雪步": 4,
            "彌生": 5,
            "真": 6,
            "伊織": 7,
            "貴音": 8,
            "律子": 9,
            "梓": 10,
            "亞美": 11,
            "真美": 12,
            "響": 13,
            "未來": 14,
            "靜香": 15,
            "翼": 16,
            "琴葉": 17,
            "艾琳娜": 18,
            "美奈子": 19,
            "恵美": 20,
            "茉莉": 21,
            "星梨花": 22,
            "茜": 23,
            "杏奈": 24,
            "Roco": 25,
            "百合子": 26,
            "紗代子": 27,
            "亞利沙": 28,
            "海美": 29,
            "育": 30,
            "朋花": 31,
            "Emily": 32,
            "志保": 33,
            "步": 34,
            "日向": 35,
            "可奈": 36,
            "奈緒": 37,
            "千鶴": 38,
            "木實": 39,
            "環": 40,
            "風花": 41,
            "美也": 42,
            "法子": 43,
            "瑞希": 44,
            "可憐": 45,
            "莉緒": 46,
            "昴": 47,
            "麗花": 48,
            "桃子": 49,
            "Julia": 50,
            "紬": 51,
            "歌織": 52
        }

        DIR: str = "./image/goods"
        img_base = Image.open(f"{DIR}/base/{base}.png")
        img_idol = Image.open(f"{DIR}/idol/{manifest[idol]}.png")
        image = Image.new("RGBA", (256, 300))

        if base == 1:
            img_base = img_base.resize((211, 111))
            image.alpha_composite(img_base)
            image = ImageChops.offset(image, 24, 165)

        if base == 2:
            img_base = img_base.resize((211, 111))
            image.alpha_composite(img_base)
            image = ImageChops.offset(image, 24, 161)

        if base == 3:
            img_base = img_base.resize((211, 111))
            image.alpha_composite(img_base)
            image = ImageChops.offset(image, 24, 165)

        image.alpha_composite(img_idol)

        with BytesIO() as image_binary:
            image.save(image_binary, "PNG")
            image_binary.seek(0)
            attachment = File(image_binary, file_name="goods.png")
            await ctx.send(files=attachment)

def setup(Misaki):
    goods(Misaki)