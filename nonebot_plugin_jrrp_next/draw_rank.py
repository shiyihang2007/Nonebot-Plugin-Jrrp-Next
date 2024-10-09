import asyncio
from io import BytesIO

from nonebot.adapters.onebot.v11 import MessageSegment
from PIL import Image, ImageDraw

from .resource_manager import StaticPath
from .utils import DataText, avatar_handler, draw_text, open_img

rank_width = 1600
rank_width_m = 1000
rank_height = 120
rank_height_m = 100
rank_avatar_size = 100


async def _draw_rank(
    data: list[dict],
    color: tuple[int, int, int] = (0, 102, 204),
) -> Image.Image:
    data = sorted(data, key=lambda x: x["rp"], reverse=True)
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
    i = 0
    for it in data:
        i += 1
        x = int(rank_height - rank_height_m * 0.8) // 2
        y = i * rank_height + (rank_height - rank_height_m) // 2
        tmp = Image.new("RGBA", (rank_width_m * it["rp"] // 100, rank_height_m), color)
        image.alpha_composite(tmp, (x, y))
        avatar_img = await open_img(
            f"http://q1.qlogo.cn/g?b=qq&nk={it["user_id"]}&s=640"
        )
        avatar_img = avatar_img.resize((rank_height_m, rank_height_m))
        avatar_img = avatar_handler(avatar_img)
        image.alpha_composite(
            avatar_img,
            (x + rank_width_m * it["rp"] // 100 + rank_avatar_size // 2, y),
        )
        image = draw_text(
            image,
            DataText(
                x + (rank_height - rank_height_m * 0.8) // 2,
                y + (rank_height - rank_height_m * 0.8) // 2,
                int(rank_height_m * 0.8),
                it["rp"],
                StaticPath.AlibabaPuHuiTi,
            ),
            color=(255, 255, 255, 255),
        )
        image = draw_text(
            image,
            DataText(
                x + rank_width_m * it["rp"] // 100 + rank_avatar_size * 1.8,
                y + (rank_height - rank_height_m * 0.8) // 2,
                int(rank_height_m * 0.8),
                it["nickname"],
                StaticPath.AlibabaPuHuiTi,
            ),
            color=(0, 0, 0, 255),
        )
    return image


async def draw_rank(
    data: list[dict],
    color: tuple[int, int, int] = (0, 102, 204),
) -> MessageSegment:
    buffer = BytesIO()
    (await _draw_rank(data, color)).convert("RGB").save(buffer, "png")
    return MessageSegment.image(buffer)


if __name__ == "__main__":
    asyncio.run(
        _draw_rank(
            [],
        )
    ).save("tmp.png", "png")
