# To use this code, make sure you
#
import json
#
# and then, to convert JSON from a string, do
#
#     result = welcome8_from_dict(json.loads(json_string))

from typing import Any, List, Optional, Union, TypeVar, Callable, Type, cast
from uuid import UUID


T = TypeVar("T")


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def from_bool(x: Any) -> bool:
    assert isinstance(x, bool)
    return x


def from_none(x: Any) -> Any:
    assert x is None
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except:
            pass
    assert False


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


class Hwi:
    hw: str

    def __init__(self, hw: str) -> None:
        self.hw = hw

    @staticmethod
    def from_dict(obj: Any) -> 'Hwi':
        assert isinstance(obj, dict)
        hw = from_str(obj.get("hw"))
        return Hwi(hw)

    def to_dict(self) -> dict:
        result: dict = {}
        result["hw"] = from_str(self.hw)
        return result


class Meta:
    ants: List[Any]
    id: str
    offensive: bool
    section: str
    src: str
    stems: List[str]
    syns: List[List[str]]
    uuid: UUID

    def __init__(self, ants: List[Any], id: str, offensive: bool, section: str, src: str, stems: List[str], syns: List[List[str]], uuid: UUID) -> None:
        self.ants = ants
        self.id = id
        self.offensive = offensive
        self.section = section
        self.src = src
        self.stems = stems
        self.syns = syns
        self.uuid = uuid

    @staticmethod
    def from_dict(obj: Any) -> 'Meta':
        assert isinstance(obj, dict)
        ants = from_list(lambda x: x, obj.get("ants"))
        id = from_str(obj.get("id"))
        offensive = from_bool(obj.get("offensive"))
        section = from_str(obj.get("section"))
        src = from_str(obj.get("src"))
        stems = from_list(from_str, obj.get("stems"))
        syns = from_list(lambda x: from_list(from_str, x), obj.get("syns"))
        uuid = UUID(obj.get("uuid"))
        return Meta(ants, id, offensive, section, src, stems, syns, uuid)

    def to_dict(self) -> dict:
        result: dict = {}
        result["ants"] = from_list(lambda x: x, self.ants)
        result["id"] = from_str(self.id)
        result["offensive"] = from_bool(self.offensive)
        result["section"] = from_str(self.section)
        result["src"] = from_str(self.src)
        result["stems"] = from_list(from_str, self.stems)
        result["syns"] = from_list(lambda x: from_list(from_str, x), self.syns)
        result["uuid"] = str(self.uuid)
        return result


class Wvr:
    wva: str
    wvl: str

    def __init__(self, wva: str, wvl: str) -> None:
        self.wva = wva
        self.wvl = wvl

    @staticmethod
    def from_dict(obj: Any) -> 'Wvr':
        assert isinstance(obj, dict)
        wva = from_str(obj.get("wva"))
        wvl = from_str(obj.get("wvl"))
        return Wvr(wva, wvl)

    def to_dict(self) -> dict:
        result: dict = {}
        result["wva"] = from_str(self.wva)
        result["wvl"] = from_str(self.wvl)
        return result


class SimList:
    wd: str
    wvrs: Optional[List[Wvr]]

    def __init__(self, wd: str, wvrs: Optional[List[Wvr]]) -> None:
        self.wd = wd
        self.wvrs = wvrs

    @staticmethod
    def from_dict(obj: Any) -> 'SimList':
        assert isinstance(obj, dict)
        wd = from_str(obj.get("wd"))
        wvrs = from_union([lambda x: from_list(Wvr.from_dict, x), from_none], obj.get("wvrs"))
        return SimList(wd, wvrs)

    def to_dict(self) -> dict:
        result: dict = {}
        result["wd"] = from_str(self.wd)
        result["wvrs"] = from_union([lambda x: from_list(lambda x: to_class(Wvr, x), x), from_none], self.wvrs)
        return result


class SseqClass:
    dt: List[List[str]]
    sim_list: List[List[SimList]]

    def __init__(self, dt: List[List[str]], sim_list: List[List[SimList]]) -> None:
        self.dt = dt
        self.sim_list = sim_list

    @staticmethod
    def from_dict(obj: Any) -> 'SseqClass':
        assert isinstance(obj, dict)
        dt = from_list(lambda x: from_list(from_str, x), obj.get("dt"))
        sim_list = from_list(lambda x: from_list(SimList.from_dict, x), obj.get("sim_list"))
        return SseqClass(dt, sim_list)

    def to_dict(self) -> dict:
        result: dict = {}
        result["dt"] = from_list(lambda x: from_list(from_str, x), self.dt)
        result["sim_list"] = from_list(lambda x: from_list(lambda x: to_class(SimList, x), x), self.sim_list)
        return result


class Def:
    sseq: List[List[List[Union[SseqClass, str]]]]

    def __init__(self, sseq: List[List[List[Union[SseqClass, str]]]]) -> None:
        self.sseq = sseq

    @staticmethod
    def from_dict(obj: Any) -> 'Def':
        assert isinstance(obj, dict)
        sseq = from_list(lambda x: from_list(lambda x: from_list(lambda x: from_union([SseqClass.from_dict, from_str], x), x), x), obj.get("sseq"))
        return Def(sseq)

    def to_dict(self) -> dict:
        result: dict = {}
        result["sseq"] = from_list(lambda x: from_list(lambda x: from_list(lambda x: from_union([lambda x: to_class(SseqClass, x), from_str], x), x), x), self.sseq)
        return result


class Result:
    result_def: List[Def]
    fl: str
    hwi: Hwi
    meta: Meta
    shortdef: List[str]
    sls: List[str]

    def __init__(self, result_def: List[Def], fl: str, hwi: Hwi, meta: Meta, shortdef: List[str], sls: List[str]) -> None:
        self.result_def = result_def
        self.fl = fl
        self.hwi = hwi
        self.meta = meta
        self.shortdef = shortdef
        self.sls = sls

    @staticmethod
    def from_dict(obj: Any) -> 'Result':
        assert isinstance(obj, dict)
        result_def = from_list(Def.from_dict, obj.get("def"))
        fl = from_str(obj.get("fl"))
        hwi = Hwi.from_dict(obj.get("hwi"))
        meta = Meta.from_dict(obj.get("meta"))
        shortdef = from_list(from_str, obj.get("shortdef"))
        sls = from_list(from_str, obj.get("sls"))
        return Result(result_def, fl, hwi, meta, shortdef, sls)

    def to_dict(self) -> dict:
        result: dict = {}
        result["def"] = from_list(lambda x: to_class(Def, x), self.result_def)
        result["fl"] = from_str(self.fl)
        result["hwi"] = to_class(Hwi, self.hwi)
        result["meta"] = to_class(Meta, self.meta)
        result["shortdef"] = from_list(from_str, self.shortdef)
        result["sls"] = from_list(from_str, self.sls)
        return result


class APIObject:
    result: List[Result]

    def __init__(self, result: List[Result]) -> None:
        self.result = result

    @staticmethod
    def from_dict(obj: Any) -> 'APIObject':
        assert isinstance(obj, dict)
        result = from_list(Result.from_dict, obj.get("result"))
        return APIObject(result)

    def to_dict(self) -> dict:
        result: dict = {}
        result["result"] = from_list(lambda x: to_class(Result, x), self.result)
        return result


def welcome8_from_dict(s: Any) -> APIObject:
    return APIObject.from_dict(s)


def welcome8_to_dict(x: APIObject) -> Any:
    return to_class(APIObject, x)