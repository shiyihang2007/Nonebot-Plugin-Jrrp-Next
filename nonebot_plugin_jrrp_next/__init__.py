from nonebot.adapters.onebot.v11 import Bot, Message, GroupMessageEvent
from nonebot.params import CommandArg
from nonebot import CommandGroup, logger, get_plugin_config

from .draw_rank import draw_rank

from .utils import get_jrrp
from .draw_img import draw_img

import datetime
import random


from .configs import Config


config = get_plugin_config(Config).jrrp_next


async def is_enabled(event: GroupMessageEvent) -> bool:
    _, group_id, user_id = event.get_session_id().split("_")
    # 不回复黑名单用户
    if user_id in config.ban_user:
        return False
    # 在允许的群聊中启用
    if group_id in config.groups_enabled:
        return True
    return False


RP_COMMAND_GROUP = CommandGroup("jrrp", rule=is_enabled)
JRRP_COMMAND = RP_COMMAND_GROUP.command(tuple(), aliases={"今日人品", "rp"})
RANK_COMMAND = RP_COMMAND_GROUP.command("rank", aliases={"人品排行", "rk"})

rank_data: list[dict] = []


@JRRP_COMMAND.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global rank_data

    args = arg.extract_plain_text().split()
    _jrrp: int = 0

    if len(args) == 0:
        user_id = event.user_id
        _jrrp = get_jrrp(str(user_id))

    else:
        user_id = int(args[0])
        _jrrp = get_jrrp(str(user_id))

    USER_DATA: dict = await bot.call_api("get_stranger_info", **{"user_id": user_id})
    nickname = str(USER_DATA.get("nickname"))
    localtime = datetime.datetime.now()
    url = random.choice(config.image_url_list)
    try:
        image = await draw_img(user_id, _jrrp, nickname, url, localtime)
    except Exception as e:
        logger.warning(f"Error at draw_img: {e}")
        image = "Bot出了点问题, 返回文字版:\n您今天的人品值是: " + str(_jrrp)
    # image = await draw_img(user_id, _jrrp, nickname, url, localtime)
    rank_data.append({"rp": _jrrp, "user_id": user_id, "nickname": nickname})
    await JRRP_COMMAND.finish(image)


@RANK_COMMAND.handle()
async def _(bot: Bot, event: GroupMessageEvent):
    await RANK_COMMAND.finish(await draw_rank(rank_data))
