import datetime
import random

from nonebot import CommandGroup, get_plugin_config, logger, require
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent, Message
from nonebot.params import CommandArg

from .configs import Config
from .draw_img import draw_img
from .draw_rank import draw_rank
from .rank_data import RankData
from .utils import get_jrrp

config = get_plugin_config(Config).jrrp_next

require("nonebot_plugin_localstore")

import nonebot_plugin_localstore as store  # noqa: E402


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

rankDataFile = store.get_data_file("nonebot_plugin_jrrp_next", "ranks.json")
rankData: RankData = RankData(rankDataFile)


@JRRP_COMMAND.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    global rankData

    args = arg.extract_plain_text().split()
    _jrrp: int = 0
    group_id = event.group_id

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
    rankData.insert(str(group_id), (str(user_id), nickname, _jrrp))
    await JRRP_COMMAND.finish(image)


@RANK_COMMAND.handle()
async def _(bot: Bot, event: GroupMessageEvent, arg: Message = CommandArg()):
    group_id = str(event.group_id)
    args = arg.extract_plain_text().split()

    style: int = 1
    color: tuple[int, int, int] = (0, 102, 204)
    if len(args) >= 1:
        style: int = int(args[0])
    if len(args) >= 2:
        color: tuple[int, int, int] = (
            int(args[1][0:2], base=16),
            int(args[1][2:4], base=16),
            int(args[1][4:6], base=16),
        )

    await RANK_COMMAND.finish(
        await draw_rank(rankData.load_rank(group_id), style, color)
    )
