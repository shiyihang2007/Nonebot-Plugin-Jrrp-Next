import asyncio
from io import BytesIO
import random
import math

from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import json

if __name__ == "__main__":
    from rank_data import RankNodeType, RankRecordsType
    from resource_manager import StaticPath
    from utils import (
        DataText,
        avatar_handler,
        draw_text,
        open_img,
        drawer_draw_shadowed_text,
    )
else:
    from .rank_data import RankNodeType, RankRecordsType
    from .resource_manager import StaticPath
    from .utils import (
        DataText,
        avatar_handler,
        draw_text,
        open_img,
        drawer_draw_shadowed_text,
    )


avatars: dict[str, Image.Image] = {}


async def _get_avatar(user_id: str):
    global avatars
    avatars[user_id] = await open_img(f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640")


async def _draw_rank(
    data: RankRecordsType,
    color: tuple[int, int, int] | None = None,
) -> Image.Image:
    if not color:
        color = (0, 102, 204)

    # config
    rank_width_m = 728
    rank_height_m = int(rank_width_m * 0.1)
    rank_avatar_size = int(rank_height_m * 1.0)
    rank_width = int(rank_width_m * 2.2)
    rank_height = int(rank_height_m * 1.2)

    # get avatar_img
    get_avatar_tasks: list = []
    for it in data:
        if it not in avatars:
            get_avatar_tasks.append(asyncio.Task(_get_avatar(it)))
    if len(get_avatar_tasks) > 0:
        await asyncio.wait(get_avatar_tasks)
    # draw rank
    image = Image.new(
        "RGBA", (rank_width, rank_height * (len(data) + 1)), (255, 255, 255, 255)
    )
    image = draw_text(
        image,
        DataText(
            (rank_height - rank_height_m * 0.8) // 2,
            (rank_height - rank_height_m * 0.8) // 2,
            int(rank_height_m * 0.8),
            "RP rank",
            StaticPath.AlibabaPuHuiTi,
        ),
        (0, 0, 0, 255),
    )
    draw = ImageDraw.Draw(image)
    i = 0
    for it in sorted(data.values(), key=lambda x: x[RankNodeType.RP], reverse=True):
        i += 1
        x = int(rank_height - rank_height_m * 0.8) // 2
        y = i * rank_height + (rank_height - rank_height_m) // 2
        draw.rectangle(
            [x, y, x + rank_width_m * it[RankNodeType.RP] // 100, y + rank_height_m],
            color,
        )
        avatar_img = avatars[it[RankNodeType.USER_ID]]
        avatar_img = avatar_img.resize((rank_height_m, rank_height_m))
        avatar_img = avatar_handler(avatar_img)
        image.alpha_composite(
            avatar_img,
            (
                x
                + max(rank_width_m * it[RankNodeType.RP] // 100, rank_width_m // 20)
                + rank_avatar_size // 2,
                y,
            ),
        )
        draw.text(
            (
                x + (rank_height - rank_height_m * 0.8) // 2,
                y + (rank_height - rank_height_m * 0.8) // 2,
            ),
            str(it[RankNodeType.RP]),
            font=ImageFont.truetype(
                str(StaticPath.AlibabaPuHuiTi), int(rank_height_m * 0.8)
            ),
            fill=(255, 255, 255, 255),
            anchor="lt",
            stroke_width=int(rank_height_m * 0.1),
            stroke_fill=color,
        )
        draw.text(
            (
                x
                + max(rank_width_m * it[RankNodeType.RP] // 100, rank_width_m // 20)
                + rank_avatar_size * 1.8,
                y + (rank_height - rank_height_m * 0.8) // 2,
            ),
            str(it[RankNodeType.NICKNAME]),
            font=ImageFont.truetype(
                str(StaticPath.AlibabaPuHuiTi), int(rank_height_m * 0.8)
            ),
            fill=(0, 0, 0, 255),
            anchor="lt",
        )
    return image


async def _draw_rank_1(
    data: RankRecordsType,
    color: tuple[int, int, int] | None = None,
) -> Image.Image:
    if not color:
        color = (0, 102, 204)

    # config
    rank_width_m = 728
    rank_height_m = int(rank_width_m * 0.1)
    rank_avatar_size = int(rank_height_m * 1.0)
    rank_width = int(rank_width_m * 2.2)
    rank_height = int(rank_height_m * 1.2)

    # get avatar_img
    get_avatar_tasks: list = []
    for it in data:
        if it not in avatars:
            get_avatar_tasks.append(asyncio.Task(_get_avatar(it)))
    if len(get_avatar_tasks) > 0:
        await asyncio.wait(get_avatar_tasks)
    # draw rank
    image = Image.new(
        "RGBA", (rank_width, rank_height * (len(data) + 1)), (255, 255, 255, 255)
    )
    image = draw_text(
        image,
        DataText(
            (rank_height - rank_height_m * 0.8) // 2,
            (rank_height - rank_height_m * 0.8) // 2,
            int(rank_height_m * 0.8),
            "RP rank",
            StaticPath.AlibabaPuHuiTi,
        ),
        (0, 0, 0, 255),
    )
    draw = ImageDraw.Draw(image)
    i = 0
    for it in sorted(data.values(), key=lambda x: x[RankNodeType.RP], reverse=True):
        i += 1
        x = rank_height + int((rank_height - rank_height_m * 0.8) * 1.5)
        y = i * rank_height + (rank_height - rank_height_m) // 2
        draw.rectangle(
            [x, y, x + rank_width_m * it[RankNodeType.RP] // 100, y + rank_height_m],
            color,
        )
        avatar_img = avatars[it[RankNodeType.USER_ID]]
        avatar_img = avatar_img.resize((rank_height_m, rank_height_m))
        avatar_img = avatar_handler(avatar_img)
        image.alpha_composite(
            avatar_img,
            (x + rank_width_m * it[RankNodeType.RP] // 100 + rank_avatar_size // 2, y),
        )
        draw.text(
            (
                x - (rank_height - rank_height_m * 0.8) // 2,
                y + (rank_height - rank_height_m * 0.8) // 2,
            ),
            str(it[RankNodeType.RP]),
            font=ImageFont.truetype(
                str(StaticPath.AlibabaPuHuiTi), int(rank_height_m * 0.8)
            ),
            fill=(255, 255, 255, 255),
            anchor="rt",
            stroke_width=int(rank_height_m * 0.1),
            stroke_fill=color,
        )
        draw.text(
            (
                x + rank_width_m * it[RankNodeType.RP] // 100 + rank_avatar_size * 1.8,
                y + (rank_height - rank_height_m * 0.8) // 2,
            ),
            str(it[RankNodeType.NICKNAME]),
            font=ImageFont.truetype(
                str(StaticPath.AlibabaPuHuiTi), int(rank_height_m * 0.8)
            ),
            fill=(0, 0, 0, 255),
            anchor="lt",
        )
    return image


async def _draw_rank_2(
    data: RankRecordsType,
    color: tuple[int, int, int] | None = None,
) -> Image.Image:
    if not color:
        color = (120, 200, 255)

    # config

    rank_shape_k = 0.5

    rank_title_width = 1333
    rank_title_height = 320
    rank_title_padding_left = 100
    rank_title_font_size = 120
    rank_subtitle_font_size = 60

    rank_li_height = 320
    rank_label_width = 400
    rank_label_font_size = 60
    rank_item_size = 80

    rank_footer_height = 320

    rank_shadow_size = 6

    rank_width = 1600
    rank_height = int(
        rank_title_height * 1.5
        + rank_li_height * 1.5 * math.ceil(len(data) / 6)
        + rank_footer_height * 1.5
    )

    noise_count = 50
    noise_size = rank_width // 10
    noise_size_range = 60
    noise_color_range = 30

    # draw image
    image = Image.new("RGBA", (rank_width, rank_height), (255, 255, 255, 255))

    # draw background
    image_background = Image.new("RGBA", image.size, color)
    draw = ImageDraw.Draw(image_background)
    for i in range(noise_count):
        draw.circle(
            (random.randint(0, image.width - 1), random.randint(0, image.height - 1)),
            noise_size + random.randint(-noise_size_range // 2, noise_size_range // 2),
            (
                color[0]
                + random.randint(-noise_color_range // 2, noise_color_range // 2),
                color[1]
                + random.randint(-noise_color_range // 2, noise_color_range // 2),
                color[2]
                + random.randint(-noise_color_range // 2, noise_color_range // 2),
            ),
        )
    for i in range(noise_count // 8):
        draw.circle(
            (random.randint(0, image.width - 1), random.randint(0, image.height - 1)),
            noise_size * 2
            + random.randint(-noise_size_range // 2, noise_size_range // 2),
            (
                64 + random.randint(0, noise_color_range),
                64 + random.randint(0, noise_color_range),
                64 + random.randint(0, noise_color_range),
            ),
        )
    for i in range(noise_count // 5):
        draw.circle(
            (random.randint(0, image.width - 1), random.randint(0, image.height - 1)),
            noise_size * 2
            + random.randint(-noise_size_range // 2, noise_size_range // 2),
            (
                255 + random.randint(-noise_color_range, 0),
                255 + random.randint(-noise_color_range, 0),
                255 + random.randint(-noise_color_range, 0),
            ),
        )
    image_background = image_background.filter(ImageFilter.BoxBlur(image.width * 0.1))
    image.alpha_composite(image_background)

    # draw title
    image_title = Image.new("RGBA", image.size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image_title)
    draw.rectangle(
        [(0, rank_title_height * 0.5), (rank_width, rank_title_height * 1.5)],
        (0, 0, 0, 32),
    )
    draw.polygon(
        [
            (0, rank_title_height * 0.4),
            (
                rank_title_width + rank_title_height * 1.2 * rank_shape_k,
                rank_title_height * 0.4,
            ),
            (rank_title_width, rank_title_height * 1.6),
            (0, rank_title_height * 1.6),
        ],
        (0, 0, 0, 56),
    )
    image.alpha_composite(image_title)
    image_title = Image.new("RGBA", image.size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image_title)
    drawer_draw_shadowed_text(
        draw,
        (rank_title_padding_left, rank_title_height * 1.0),
        text="RP Rank",
        color=(255, 255, 255, 255),
        font=StaticPath.Aldrich,
        font_size=rank_title_font_size,
        shadow_size=rank_shadow_size,
        shadow_color=(0, 0, 0, 32),
        anchor="lb",
    )
    drawer_draw_shadowed_text(
        draw,
        (rank_title_padding_left, rank_title_height * 1.4),
        text="Create by Nonebot-Plugin-Jrrp-Next",
        color=(255, 255, 255, 255),
        font=StaticPath.Aldrich,
        font_size=rank_subtitle_font_size,
        shadow_size=rank_shadow_size,
        shadow_color=(0, 0, 0, 32),
        anchor="lb",
    )
    image.alpha_composite(image_title)

    # draw li
    image_li = Image.new("RGBA", image.size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image_li)
    for i in range(math.ceil(len(data) / 6)):
        ypos = rank_li_height * 1.5 * i + rank_title_height * 1.5
        # label
        draw.rectangle(
            [
                (0, ypos + rank_li_height * 0.8),
                (rank_width, ypos + rank_li_height * 1.2),
            ],
            (0, 0, 0, 32),
        )
        # bg
        draw.polygon(
            [
                (
                    rank_label_width + rank_li_height * 1 * rank_shape_k,
                    ypos + rank_li_height * 0.5,
                ),
                (
                    rank_width,
                    ypos + rank_li_height * 0.5,
                ),
                (rank_width, ypos + rank_li_height * 1.5),
                (rank_label_width, ypos + rank_li_height * 1.5),
            ],
            (0, 0, 0, 56),
        )
    image.alpha_composite(image_li)
    image_li = Image.new("RGBA", image.size, color=(0, 0, 0, 0))
    draw = ImageDraw.Draw(image_li)
    for i in range(math.ceil(len(data) / 6)):
        ypos = rank_li_height * 1.5 * i + rank_title_height * 1.5
        # label text
        drawer_draw_shadowed_text(
            draw,
            (rank_label_width * 0.2, ypos + rank_li_height * 1.0),
            f"Rank {i * 6 + 1}-{i * 6 + 6}",
            StaticPath.Aldrich,
            rank_label_font_size,
            rank_shadow_size,
            (255, 255, 255, 255),
            (0, 0, 0, 32),
            "lm",
        )
    image.alpha_composite(image_li)

    return image


async def draw_rank(
    data: RankRecordsType,
    style: int = 0,
    color: tuple[int, int, int] | None = None,
) -> MessageSegment:
    buffer = BytesIO()
    if style == 0:
        (await _draw_rank(data, color)).convert("RGBA").save(buffer, "png")
    elif style == 1:
        (await _draw_rank_1(data, color)).convert("RGBA").save(buffer, "png")
    elif style == 2:
        (await _draw_rank_2(data, color)).convert("RGBA").save(buffer, "png")
    return MessageSegment.image(buffer)


if __name__ == "__main__":
    data = json.loads(input())
    style = int(input())

    if style == 0:
        asyncio.run(_draw_rank(data)).convert("RGBA").save("tmp.png", "png")
    elif style == 1:
        asyncio.run(_draw_rank_1(data)).convert("RGBA").save("tmp.png", "png")
    elif style == 2:
        asyncio.run(_draw_rank_2(data)).convert("RGBA").save("tmp.png", "png")
