from typing import Any, Dict


class PivotMapper:
    class Field:
        YEAR = "year"
        MONTH = "month"
        DATA = "data"

    @classmethod
    def to_json(cls, data):
        list = []
        for row in data:
            json: Dict[str, Any] = {}
            json[cls.Field.YEAR] = row.pop(cls.Field.YEAR)
            json[cls.Field.MONTH] = row.pop(cls.Field.MONTH)
            json[cls.Field.DATA] = row
            list.append(json)
        return list


pivot_mapper = PivotMapper()
