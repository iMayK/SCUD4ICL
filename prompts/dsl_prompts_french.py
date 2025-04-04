FULL_DD_WO_DO_FOR_STEP_BY_STEP = """Given the following data structures and functions:
```
TrouverÉquipeDe  # given a person name or id, returns a pseudo-person representing the team of that person
TrouverRapports  # given a person name or id, returns a pseudo-person representing the reports of that person
TrouverGestionnaire  # given a person name or id, returns the manager of that person

avec_participant  # given a person name or id, returns a clause to match or create an event with that person as an attendee
éviter_participant  # given a person name or id, returns an event clause to avoid that attendee when creating an event
a_sujet  # given a string, returns an event to match or create an event with that subject
à_emplacement  # given a string, returns an event clause to match or create an event at that location
commence_à  # given a datetime clause, returns an event clause to match or create an event starting at that time
se_termine_à  # given a datetime clause, returns an event clause to match or create an event ending at that time
a_durée  # given a time unit value, returns an event clause to match or create an event with that duration
a_statut  # given a ShowAsStatus value, returns an event clause to match or create an event with that status

# the following operators return datetime clauses and accept no arguments
AprèsMidi
PetitDéjeuner
Brunch
Dîner
Tôt
FinDeJournéeDeTravail
Soirée
MoisEntierDuMois
AnnéeComplèteDeL'Année
NouvelleDernièreSemaine
Tard
FinD'AprèsMidi
FinDeMatinée
Déjeuner
Matin
MoisProchain
WeekEndProchain
ListeProchaineSemaine
AnnéeProchaine
Nuit
Midi
Maintenant
Automne
Printemps
Été
Hiver
CetteSemaine
CeWeekEnd
Aujourd'hui
Demain
Hier

# general date time clauses
ClasseDateHeure  # given either a datetime clause representing a date and/or a time operator representing a time, returns a datetime clause
ClasseDate  # given a date or dayofweek, returns a date
ClasseJourDeSemaine  # given a day of week string, returns a time clause
ProchainJourOuvré  # given a day of week string, returns a time clause for the next occurrence of that day of week
MoisJour  # given a month and day as arguments, returns a date clause
MoisJourAnnée  # given a month, day, and year as arguments, returns a date clause

# given a value, the following operators return datetime clauses according to the given value
versMois
enAnnéeÀQuatreChiffres
HeureMinuteAM
HeureMinutePM
NombreAM
NombrePM

# given a datetime clause, the following operators modify the clause and return a datetime clause according to the modification
ÀDateAprèsHeure
ÀDateAvantHeure
AutourDateHeure

# given either a number or the operators EkDo/Kuch, all the following operators return time unit values according to the given unit
enJours
enHeures
enMinutes

# these operators can be used to create time unit values instead of using integer values
UnCouple
Quelques

AfficherCommeStatut  # enumeration of possible event statuses (Busy, OutOfOffice)

CréerÉvénement  # given multiple event clauses (such as avec_participant, a_sujet, combined together with `ET`), creates an event complying with those clauses
TrouverÉvénements  # given multiple event clauses (such as avec_participant, a_sujet, combined together with `ET`), returns a list of events complying with those clauses
UtilisateurActuel  # returns the current user (person)

ET  # combines multiple event clauses together
```

Your task is to write DSL code for the given question.
Note:
1. Do not use any external libraries.
2. Strictly adhere to the provided data structures, classes, and enums. Use only the defined values and methods.
3. Make no assumptions beyond the provided information. Follow the general flow demonstrated in the examples.
"""
