FULL_DD = """Given the following data structures and functions:
```
DalKhojen  # given a person name or id, returns a pseudo-person representing the team of that person
ReportDhoondho  # given a person name or id, returns a pseudo-person representing the reports of that person
PrabandhakKhojen  # given a person name or id, returns the manager of that person

InSahbhagiyonKeSaath  # given a person name or id, returns a clause to match or create an event with that person as an attendee
InSahbhagiyonKeBina  # given a person name or id, returns an event clause to avoid that attendee when creating an event
VishayHai  # given a string, returns an event to match or create an event with that subject
IsSthanPar  # given a string, returns an event clause to match or create an event at that location
SePrarambh  # given a datetime clause, returns an event clause to match or create an event starting at that time
PeSamapt  # given a datetime clause, returns an event clause to match or create an event ending at that time
AvdhiHai  # given a time unit value, returns an event clause to match or create an event with that duration
SthitiHai  # given a SthitiDikhayein value, returns an event clause to match or create an event with that status

# the following operators return datetime clauses and accept no arguments
DopaharBaad
Naashta
DerNashta
RaatKaBhojan
Jaldi
KaryaDivasSamapt
Shaam
MaahKaPuraMaah
VarshKaPurnaVarsh
PichleHafteNaya
Der
DerDopahar
DerSubah
DopaharKaBhojan
Subah
AglaMaah
AglaSaptahant
AgleHafteKiSuchi
AglaVarsh
Raat
Dopahar
Abhi
Patjhad
Vasant
Grishm
Shishir
IsHafte
IsSaptahant
Aaj
Kal
BitaKal

# general date time clauses
DinankSamayVarg  # given either a datetime clause representing a date and/or a time operator representing a time, returns a datetime clause
DinankVarg  # given a date or dayofweek, returns a date
SaptahKaVarshikDin  # given a day of week string, returns a time clause
AglaKaryaDiwas  # given a day of week string, returns a time clause for the next occurrence of that day of week
MahinaDin  # given a month and day as arguments, returns a date clause
MahinaDinVarsh  # given a month, day, and year as arguments, returns a date clause

# given a value, the following operators return datetime clauses according to the given value
MaahMein
ChaarAnkVarsh
GhantaMinatPoorvahn
GhantaMinatAparanh
SankhyaPoorvahn
SankhyaAparanh

# given a datetime clause, the following operators modify the clause and return a datetime clause according to the modification
DinankKeBaadSamay
DinankParSamaySePhele
SamayDinankKePaas

# given either a number or the operators EkDo/Kuch, all the following operators return time unit values according to the given unit
DinoMein
GhantoMein
MinatoMein

# these operators can be used to create time unit values instead of using integer values
EkDo
Kuch

SthitiDikhayein  # enumeration of possible event statuses (Busy, OutOfOffice)

KaryakramBanao  # given multiple event clauses (such as InSahbhagiyonKeSaath, VishayHai, combined together with `Aur`), creates an event complying with those clauses
KaryakramDhoondho  # given multiple event clauses (such as InSahbhagiyonKeSaath, VishayHai, combined together with `Aur`), returns a list of events complying with those clauses
VartamanUpyogkarta  # returns the current user (person)

Karo  # allows the execution of multiple commands in a single prompt (each command is an argument). Often used in conjunction with `Let` to define variables
Anumati  # defines a variable (first argument) with a value (second argument)

Aur  # combines multiple event clauses together
```"""


FULL_DD_WO_DO = """Given the following data structures and functions:
```
DalKhojen  # given a person name or id, returns a pseudo-person representing the team of that person
ReportDhoondho  # given a person name or id, returns a pseudo-person representing the reports of that person
PrabandhakKhojen  # given a person name or id, returns the manager of that person

InSahbhagiyonKeSaath  # given a person name or id, returns a clause to match or create an event with that person as an attendee
InSahbhagiyonKeBina  # given a person name or id, returns an event clause to avoid that attendee when creating an event
VishayHai  # given a string, returns an event to match or create an event with that subject
IsSthanPar  # given a string, returns an event clause to match or create an event at that location
SePrarambh  # given a datetime clause, returns an event clause to match or create an event starting at that time
PeSamapt  # given a datetime clause, returns an event clause to match or create an event ending at that time
AvdhiHai  # given a time unit value, returns an event clause to match or create an event with that duration
SthitiHai  # given a ShowAsStatus value, returns an event clause to match or create an event with that status

# the following operators return datetime clauses and accept no arguments
DopaharBaad
Naashta
DerNashta
RaatKaBhojan
Jaldi
KaryaDivasSamapt
Shaam
MaahKaPuraMaah
VarshKaPurnaVarsh
PichleHafteNaya
Der
DerDopahar
DerSubah
DopaharKaBhojan
Subah
AglaMaah
AglaSaptahant
AgleHafteKiSuchi
AglaVarsh
Raat
Dopahar
Abhi
Patjhad
Vasant
Grishm
Shishir
IsHafte
IsSaptahant
Aaj
Kal
BitaKal

# general date time clauses
DinankSamayVarg  # given either a datetime clause representing a date and/or a time operator representing a time, returns a datetime clause
DinankVarg  # given a date or dayofweek, returns a date
SaptahKaVarshikDin  # given a day of week string, returns a time clause
AglaKaryaDiwas  # given a day of week string, returns a time clause for the next occurrence of that day of week
MahinaDin  # given a month and day as arguments, returns a date clause
MahinaDinVarsh  # given a month, day, and year as arguments, returns a date clause

# given a value, the following operators return datetime clauses according to the given value
MaahMein
ChaarAnkVarsh
GhantaMinatPoorvahn
GhantaMinatAparanh
SankhyaPoorvahn
SankhyaAparanh

# given a datetime clause, the following operators modify the clause and return a datetime clause according to the modification
DinankKeBaadSamay
DinankParSamaySePhele
SamayDinankKePaas

# given either a number or the operators EkDo/Kuch, all the following operators return time unit values according to the given unit
DinoMein
GhantoMein
MinatoMein

# these operators can be used to create time unit values instead of using integer values
EkDo
Kuch

SthitiDikhayein  # enumeration of possible event statuses (Busy, OutOfOffice)

KaryakramBanao  # given multiple event clauses (such as InSahbhagiyonKeSaath, VishayHai, combined together with `Aur`), creates an event complying with those clauses
KaryakramDhoondho  # given multiple event clauses (such as InSahbhagiyonKeSaath, VishayHai, combined together with `Aur`), returns a list of events complying with those clauses
VartamanUpyogkarta  # returns the current user (person)

Aur  # combines multiple event clauses together
```"""


FULL_DD_WO_DO_FOR_STEP_BY_STEP = """Given the following data structures and functions:
```
DalKhojen  # given a person name or id, returns a pseudo-person representing the team of that person
ReportDhoondho  # given a person name or id, returns a pseudo-person representing the reports of that person
PrabandhakKhojen  # given a person name or id, returns the manager of that person

InSahbhagiyonKeSaath  # given a person name or id, returns a clause to match or create an event with that person as an attendee
InSahbhagiyonKeBina  # given a person name or id, returns an event clause to avoid that attendee when creating an event
VishayHai  # given a string, returns an event to match or create an event with that subject
IsSthanPar  # given a string, returns an event clause to match or create an event at that location
SePrarambh  # given a datetime clause, returns an event clause to match or create an event starting at that time
PeSamapt  # given a datetime clause, returns an event clause to match or create an event ending at that time
AvdhiHai  # given a time unit value, returns an event clause to match or create an event with that duration
SthitiHai  # given a ShowAsStatus value, returns an event clause to match or create an event with that status

# the following operators return datetime clauses and accept no arguments
DopaharBaad
Naashta
DerNashta
RaatKaBhojan
Jaldi
KaryaDivasSamapt
Shaam
MaahKaPuraMaah
VarshKaPurnaVarsh
PichleHafteNaya
Der
DerDopahar
DerSubah
DopaharKaBhojan
Subah
AglaMaah
AglaSaptahant
AgleHafteKiSuchi
AglaVarsh
Raat
Dopahar
Abhi
Patjhad
Vasant
Grishm
Shishir
IsHafte
IsSaptahant
Aaj
Kal
BitaKal

# general date time clauses
DinankSamayVarg  # given either a datetime clause representing a date and/or a time operator representing a time, returns a datetime clause
DinankVarg  # given a date or dayofweek, returns a date
SaptahKaVarshikDin  # given a day of week string, returns a time clause
AglaKaryaDiwas  # given a day of week string, returns a time clause for the next occurrence of that day of week
MahinaDin  # given a month and day as arguments, returns a date clause
MahinaDinVarsh  # given a month, day, and year as arguments, returns a date clause

# given a value, the following operators return datetime clauses according to the given value
MaahMein
ChaarAnkVarsh
GhantaMinatPoorvahn
GhantaMinatAparanh
SankhyaPoorvahn
SankhyaAparanh

# given a datetime clause, the following operators modify the clause and return a datetime clause according to the modification
DinankKeBaadSamay
DinankParSamaySePhele
SamayDinankKePaas

# given either a number or the operators EkDo/Kuch, all the following operators return time unit values according to the given unit
DinoMein
GhantoMein
MinatoMein

# these operators can be used to create time unit values instead of using integer values
EkDo
Kuch

SthitiDikhayein  # enumeration of possible event statuses (Busy, OutOfOffice)

KaryakramBanao  # given multiple event clauses (such as InSahbhagiyonKeSaath, VishayHai, combined together with `Aur`), creates an event complying with those clauses
KaryakramDhoondho  # given multiple event clauses (such as InSahbhagiyonKeSaath, VishayHai, combined together with `Aur`), returns a list of events complying with those clauses
VartamanUpyogkarta  # returns the current user (person)

Aur  # combines multiple event clauses together
```

Your task is to write DSL code for the given question.
Note:
1. Do not use any external libraries.
2. Strictly adhere to the provided data structures, classes, and enums. Use only the defined values and methods.
3. Make no assumptions beyond the provided information. Follow the general flow demonstrated in the examples.
"""
