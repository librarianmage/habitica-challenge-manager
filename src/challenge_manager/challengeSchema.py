"""
Module that contains challenge schema
"""
from strictyaml import Map, MapPattern, Int, Float, Str, Enum, Bool, Seq, Optional, Datetime
from strictyaml.exceptions import raise_exception
from strictyaml.representation import YAML
from strictyaml.scalar import Scalar
import uuid
import sys

if sys.version_info[0] == 3:
    unicode = str


class UUID(Scalar):
    def validate_scalar(self, chunk, value=None):
        uuidStr = unicode(chunk.contents) if value is None else value
        try:
            id = uuid.UUID(uuidStr)
        except:
            raise_exception("when expecting a UUID", "did not find a valid UUID", chunk)
        return YAML(id, uuidStr, chunk=chunk)


taskSchema = {
    "text": Str(),
    Optional("alias"): Str(),
    Optional("attribute"): Enum(["str", "int", "per", "con"]),
    Optional("notes"): Str(),
    Optional("priority"): Float()
}

todoSchema = taskSchema.copy()
todoSchema.update({
    Optional("date"): Datetime()
})

dailySchema = taskSchema.copy()
dailySchema.update({
    Optional("frequency"): Enum(["daily", "weekly", "montly", "yearly"]),
    Optional("repeat"): MapPattern(Str(), Bool()),
    Optional("everyX"): Int(),
    Optional("startDate"): Datetime()
})

habitSchema = taskSchema.copy()
habitSchema.update({
    Optional("up"): Bool(),
    Optional("down"): Bool()
})

rewardSchema = taskSchema.copy()
rewardSchema.update({
    Optional("value"): Float()
})

challengeSchema = Map({
    "challenge": Map({
        "group": UUID(),
        "name": Str(),
        "shortName": Str(),
        Optional("summary"): Str(),
        Optional("description"): Str(),
        Optional("prize"): Int()
    }),
    Optional("tasks"): Map({
        Optional("habit"): Seq(Map(habitSchema)),
        Optional("daily"): Seq(Map(dailySchema)),
        Optional("todo"): Seq(Map(todoSchema)),
        Optional("reward"): Seq(Map(rewardSchema))
    })
})
