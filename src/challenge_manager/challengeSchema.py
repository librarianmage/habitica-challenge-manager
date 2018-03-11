"""
Module that contains challenge schema
"""
import sys
import uuid

from strictyaml import Bool
from strictyaml import Datetime
from strictyaml import Enum
from strictyaml import Float
from strictyaml import Int
from strictyaml import Map
from strictyaml import MapPattern
from strictyaml import Optional
from strictyaml import Seq
from strictyaml import Str
from strictyaml.representation import YAML
from strictyaml.scalar import ScalarValidator

if sys.version_info[0] == 3:
    unicode = str


class UUID(ScalarValidator):
    def validate_scalar(self, chunk, value=None):
        uuidStr = unicode(chunk.contents) if value is None else value
        try:
            id = str(uuid.UUID(uuidStr))
        except:
            chunk.expected_but_found(
                "when expecting a UUID",
            )
        return YAML(id, uuidStr, chunk=chunk)

class isoDatetime(Datetime):
    def validate_scalar(self, chunk):
        datetimeDate = super(isoDatetime, self).validate_scalar(chunk)
        return datetimeDate.isoformat()

taskSchema = {
    "text": Str(),
    Optional("alias"): Str(),
    Optional("attribute"): Enum(["str", "int", "per", "con"]),
    Optional("notes"): Str(),
    Optional("priority"): Enum([0.1,1,1.5,2], item_validator=Float())
}

todoSchema = taskSchema.copy()
todoSchema.update({
    Optional("date"): isoDatetime()
})

dailySchema = taskSchema.copy()
dailySchema.update({
    Optional("frequency"): Enum(["daily", "weekly", "montly", "yearly"]),
    Optional("repeat"): MapPattern(Str(), Bool()),
    Optional("everyX"): Int(),
    Optional("startDate"): isoDatetime()
})

habitSchema = taskSchema.copy()
habitSchema.update({
    Optional("up"): Bool(),
    Optional("down"): Bool(),
    Optional("frequency"): Enum(["daily", "weekly", "monthly", "yearly"])
})

rewardSchema = taskSchema.copy()
rewardSchema.update({
    Optional("value"): Float()
})

challengeSchema = Map({
    "challenge": Map({
        "group": UUID() | Str(),
        "name": Str(),
        "shortName": Str(),
        Optional("summary"): Str(),
        Optional("description"): Str(),
        Optional("prize"): Int()
    }),
    Optional("tasks"): Map({
        Optional("habits"): Seq(Map(habitSchema)),
        Optional("dailys"): Seq(Map(dailySchema)),
        Optional("todos"): Seq(Map(todoSchema)),
        Optional("rewards"): Seq(Map(rewardSchema))
    })
})

challengeSchemaList = Seq(challengeSchema)