FULL_DD = """Given the following python data structures and functions:

```python
@dataclass
class Person:
    name: str

    def find_team_of() -> List["Person"]:
        ...

    def find_reports_of() -> List["Person"]:
        ...

    def find_manager_of() -> "Person":
        ...

@dataclass
class Event:
    attendees: List[Person] = None
    attendees_to_avoid: List[Person] = None
    subject: Optional[str] = None
    location: Optional[str] = None
    starts_at: Optional[List[DateTimeClause]] = None
    ends_at: Optional[List[DateTimeClause]] = None
    duration: Optional["TimeUnit"] = None
    show_as_status: Optional["ShowAsStatus"] = None

DateTimeValues = Enum("DateTimeValues", ["Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening",
    "FullMonthofMonth", "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning",
    "NextMonth", "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring",
    "SeasonSummer", "SeasonWinter", "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"])

class DateTimeClause:
    def get_by_value(date_time_value: DateTimeValues) -> "DateTimeClause": ...
    def get_next_dow(day_of_week: str) -> "DateTimeClause": ...
    def date_by_mdy(month: int = None, day: int = None, year: int = None) -> "DateTimeClause": ...
    def time_by_hm(hour: int = None, minute: int = None, am_or_pm: str = None) -> "DateTimeClause": ...
    def on_date_before_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def on_date_after_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def around_date_time(date_time: "DateTimeClause") -> "DateTimeClause": ...


TimeUnits = Enum("TimeUnits", ["Hours", "Minutes", "Days"])
TimeUnitsModifiers = Enum("TimeUnitsModifiers", ["Acouple", "Afew"])

@dataclass
class TimeUnit:
    number: Optional[Union[int,float]] = None
    unit: Optional[TimeUnits] = None
    modifier: Optional[TimeUnitsModifiers] = None

ShowAsStatusType = Enum("ShowAsStatusType", ["Busy", "OutOfOffice"])


class API:
    def find_person(name: str) -> Person:
        ...

    def get_current_user() -> Person:
        ...

    def add_event(event: Event) -> None:
        ...

    def find_event(attendees: Optional[List[Person]] = None, subject: Optional[str] = None) -> Event:
        ...

api = API()
```

Your task is to write python code for the given question.
Note:
1. Do not use any external libraries.
2. Do not write comments in the code.
3. Strictly adhere to the provided data structures, classes, and enums. Only use the defined values and methods.
"""


FULL_DD_FOR_STEP_BY_STEP = """Given the following python data structures and functions:

```python
@dataclass
class Person:
    name: str

    def find_team_of() -> List["Person"]:
        ...

    def find_reports_of() -> List["Person"]:
        ...

    def find_manager_of() -> "Person":
        ...

@dataclass
class Event:
    attendees: List[Person] = None
    attendees_to_avoid: List[Person] = None
    subject: Optional[str] = None
    location: Optional[str] = None
    starts_at: Optional[List[DateTimeClause]] = None
    ends_at: Optional[List[DateTimeClause]] = None
    duration: Optional["TimeUnit"] = None
    show_as_status: Optional["ShowAsStatus"] = None

DateTimeValues = Enum("DateTimeValues", ["Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening",
    "FullMonthofMonth", "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning",
    "NextMonth", "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring",
    "SeasonSummer", "SeasonWinter", "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"])

class DateTimeClause:
    def get_by_value(date_time_value: DateTimeValues) -> "DateTimeClause": ...
    def get_next_dow(day_of_week: str) -> "DateTimeClause": ...
    def date_by_mdy(month: int = None, day: int = None, year: int = None) -> "DateTimeClause": ...
    def time_by_hm(hour: int = None, minute: int = None, am_or_pm: str = None) -> "DateTimeClause": ...
    def on_date_before_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def on_date_after_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def around_date_time(date_time: "DateTimeClause") -> "DateTimeClause": ...


TimeUnits = Enum("TimeUnits", ["Hours", "Minutes", "Days"])
TimeUnitsModifiers = Enum("TimeUnitsModifiers", ["Acouple", "Afew"])

@dataclass
class TimeUnit:
    number: Optional[Union[int,float]] = None
    unit: Optional[TimeUnits] = None
    modifier: Optional[TimeUnitsModifiers] = None

ShowAsStatusType = Enum("ShowAsStatusType", ["Busy", "OutOfOffice"])


class API:
    def find_person(name: str) -> Person:
        ...

    def get_current_user() -> Person:
        ...

    def add_event(event: Event) -> None:
        ...

    def find_event(attendees: Optional[List[Person]] = None, subject: Optional[str] = None) -> Event:
        ...

api = API()
```

Your task is to write python code for the given question.
Note:
1. Do not use any external libraries.
2. Strictly adhere to the provided data structures, classes, and enums. Use only the defined values and methods.
3. Make no assumptions beyond the provided information. Follow the general flow demonstrated in the examples.
4. Ensure that the final code always starts with `def answer():` and follows this exact format:
```python
def answer():
    # Your code here
```

** IMPORTANT **
Follow the output format very carefully
```
"""


FULL_DD_WO_INST = """Given the following python data structures and functions:

```python
@dataclass
class Person:
    name: str

    def find_team_of() -> List["Person"]:
        ...

    def find_reports_of() -> List["Person"]:
        ...

    def find_manager_of() -> "Person":
        ...

@dataclass
class Event:
    attendees: List[Person] = None
    attendees_to_avoid: List[Person] = None
    subject: Optional[str] = None
    location: Optional[str] = None
    starts_at: Optional[List[DateTimeClause]] = None
    ends_at: Optional[List[DateTimeClause]] = None
    duration: Optional["TimeUnit"] = None
    show_as_status: Optional["ShowAsStatus"] = None

DateTimeValues = Enum("DateTimeValues", ["Afternoon", "Breakfast", "Brunch", "Dinner", "Early", "EndOfWorkDay", "Evening",
    "FullMonthofMonth", "FullYearofYear", "LastWeekNew", "Late", "LateAfternoon", "LateMorning", "Lunch", "Morning",
    "NextMonth", "NextWeekend", "NextWeekList", "NextYear", "Night", "Noon", "Now", "SeasonFall", "SeasonSpring",
    "SeasonSummer", "SeasonWinter", "ThisWeek", "ThisWeekend", "Today", "Tomorrow", "Yesterday"])

class DateTimeClause:
    def get_by_value(date_time_value: DateTimeValues) -> "DateTimeClause": ...
    def get_next_dow(day_of_week: str) -> "DateTimeClause": ...
    def date_by_mdy(month: int = None, day: int = None, year: int = None) -> "DateTimeClause": ...
    def time_by_hm(hour: int = None, minute: int = None, am_or_pm: str = None) -> "DateTimeClause": ...
    def on_date_before_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def on_date_after_date_time(date: "DateTimeClause", time: "DateTimeClause") -> "DateTimeClause": ...
    def around_date_time(date_time: "DateTimeClause") -> "DateTimeClause": ...


TimeUnits = Enum("TimeUnits", ["Hours", "Minutes", "Days"])
TimeUnitsModifiers = Enum("TimeUnitsModifiers", ["Acouple", "Afew"])

@dataclass
class TimeUnit:
    number: Optional[Union[int,float]] = None
    unit: Optional[TimeUnits] = None
    modifier: Optional[TimeUnitsModifiers] = None

ShowAsStatusType = Enum("ShowAsStatusType", ["Busy", "OutOfOffice"])


class API:
    def find_person(name: str) -> Person:
        ...

    def get_current_user() -> Person:
        ...

    def add_event(event: Event) -> None:
        ...

    def find_event(attendees: Optional[List[Person]] = None, subject: Optional[str] = None) -> Event:
        ...

api = API()
```"""
