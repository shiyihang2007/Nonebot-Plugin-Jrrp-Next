import datetime
from pathlib import Path
import json


RankNode = tuple[str, str, int]


class RankNodeType(enumerate):
    USER_ID = 0
    NICKNAME = 1
    RP = 2


RankRecordsType = dict[str, RankNode]
RankType = dict


class RankData:
    rank: RankType
    """
    {
        "date": date, 
        group_id: {user_id: {rp, nickname}}
    }
    """
    path: Path

    def __init__(self, filename: Path) -> None:
        self.path = filename
        self.load()

    def load(self, filename: Path | None = None):
        path = self.path
        if filename:
            path = filename
        t: dict[str, str | dict[str, RankNode]]
        try:
            with open(path) as f:
                t = json.load(f)
                if t["date"] != datetime.datetime.now().strftime("%Y/%m/%d"):
                    raise ValueError("Out of date.")
        except Exception as e:
            print(f"WARN: {e}, data cleared. ")
            t = {"date": datetime.datetime.now().strftime("%Y/%m/%d")}
        self.rank = t

    def dump(self, filename: Path | None = None):
        path = self.path
        if filename:
            path = filename
        with open(path) as f:
            json.dump(self.rank, f)

    def load_rank(self, group_id: str) -> RankRecordsType:
        if group_id == "date":
            raise KeyError
        return self.rank[group_id]

    def set_rank(self, obj: str | RankType):
        if isinstance(obj, str):
            self.rank = json.loads(obj)
        else:
            self.rank = obj
        self.dump()

    def insert(self, group_id: str, record: RankNode):
        if group_id == "date":
            raise KeyError
        if not self.rank[group_id]:
            self.rank[group_id] = {}
        self.rank[group_id][record[RankNodeType.USER_ID]] = record
        self.dump()
