from pydantic import BaseModel


class ScopedConfig(BaseModel):
    command_priority: int = 10

    groups_enabled: set[str] = set()
    ban_user: set[str] = set()

    image_url_list: list[str] = [
        "https://t.alcy.cc/moe/",
        "https://t.alcy.cc/ycy/",
        # "https://t.alcy.cc/ai/",
        "https://t.alcy.cc/ys/",
    ]


class Config(BaseModel):
    jrrp_next: ScopedConfig
