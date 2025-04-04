FULL_DD_WO_DO_FOR_STEP_BY_STEP = """Given the following data structures and functions:
```
НайтиКомандуДля  # given a person name or id, returns a pseudo-person representing the team of that person
НайтиОтчеты  # given a person name or id, returns a pseudo-person representing the reports of that person
НайтиМенеджера  # given a person name or id, returns the manager of that person

с_участником  # given a person name or id, returns a clause to match or create an event with that person as an attendee
избегать_участника  # given a person name or id, returns an event clause to avoid that attendee when creating an event
имеет_тему  # given a string, returns an event to match or create an event with that subject
в_местоположении  # given a string, returns an event clause to match or create an event at that location
начинается_в  # given a datetime clause, returns an event clause to match or create an event starting at that time
заканчивается_в  # given a datetime clause, returns an event clause to match or create an event ending at that time
имеет_продолжительность  # given a time unit value, returns an event clause to match or create an event with that duration
имеет_статус  # given a ShowAsStatus value, returns an event clause to match or create an event with that status

# the following operators return datetime clauses and accept no arguments
ПослеПолудня
Завтрак
Бранч
Ужин
Рано
КонецРабочегоДня
Вечер
ПолныйМесяцМесяца
ПолныйГодГода
НоваяПрошлаяНеделя
Поздно
ПозднийПолдень
ПозднееУтро
Обед
Утро
СледующийМесяц
СледующиеВыходные
СписокСледующейНедели
СледующийГод
Ночь
Полдень
Сейчас
Осень
Весна
Лето
Зима
ЭтаНеделя
ЭтиВыходные
Сегодня
Завтра
Вчера

# general date time clauses
КлассДатаВремя  # given either a datetime clause representing a date and/or a time operator representing a time, returns a datetime clause
КлассДата  # given a date or dayofweek, returns a date
КлассДеньНедели  # given a day of week string, returns a time clause
СледующийРабочийДень  # given a day of week string, returns a time clause for the next occurrence of that day of week
МесяцДень  # given a month and day as arguments, returns a date clause
МесяцДеньГод  # given a month, day, and year as arguments, returns a date clause

# given a value, the following operators return datetime clauses according to the given value
вМесяц
вЧетырехзначныйГод
ЧасМинутаАМ
ЧасМинутаПМ
ЧислоАМ
ЧислоПМ

# given a datetime clause, the following operators modify the clause and return a datetime clause according to the modification
НаДатуПослеВремени
НаДатуДоВремени
ОколоДатыВремени

# given either a number or the operators Acouple/Afew, all the following operators return time unit values according to the given unit
вДни
вЧасы
вМинуты

# these operators can be used to create time unit values instead of using integer values
Пара
Несколько

ПоказатьКакСтатус  # enumeration of possible event statuses (Busy, OutOfOffice)

СоздатьСобытие  # given multiple event clauses (such as с_участником, имеет_тему, combined together with `И`), creates an event complying with those clauses
НайтиСобытия  # given multiple event clauses (such as с_участником, имеет_тему, combined together with `И`), returns a list of events complying with those clauses
ТекущийПользователь  # returns the current user (person)

И  # combines multiple event clauses together

Your task is to write DSL code for the given question.
Note:
1. Do not use any external libraries.
2. Strictly adhere to the provided data structures, classes, and enums. Use only the defined values and methods.
3. Make no assumptions beyond the provided information. Follow the general flow demonstrated in the examples.
```"""
