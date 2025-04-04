USER_TEMPLATE = """original question: {}

code: {}

decomposition:
```json
{{"""

SYS_PROMPT = """In this task, your goal is to decompose complex event scheduling queries into simpler, self-contained sub-queries. Each sub-query should be represented as a key-value pair within a JSON object. The key is the sub-query, and the value is an object containing the corresponding Domain-Specific Language (DSL) code and any further decompositions.  
   
The primary objective is to ensure that the decompositions closely mirror the language used in the original query. This is to retain the natural language and idiosyncrasies of the user's input, which are crucial for understanding the context and intent of the query.  
   
Each sub-query should be able to stand on its own, without relying on the context of the original query. This means that the sub-queries should be clear and unambiguous, even when viewed independently of the original query."""

example1_user = """original question: Add engagement party to monday 9 pm with Abby kim and desi

code: CreateEvent( AND( with_attendee( Abby ) , with_attendee( Kim ) , with_attendee( Desi ) , has_subject( engagement party ) , starts_at( NextDOW( MONDAY ) ) , starts_at( NumberPM( 9 ) ) ) )

decomposition:
```json
{"""

example1_assistant = """
    "Add engagement party to monday 9 pm with Abby kim and desi": {
        "code": "CreateEvent( AND( with_attendee( Abby ) , with_attendee( Kim ) , with_attendee( Desi ) , has_subject( engagement party ) , starts_at( NextDOW( MONDAY ) ) , starts_at( NumberPM( 9 ) ) ) )",
        "decomposition": {
            "Add engagement party with Abby kim and desi": {
                "code": "CreateEvent( AND( with_attendee( Abby ) , with_attendee( Kim ) , with_attendee( Desi ) , has_subject( engagement party ) ) )",
                "decomposition": {
                    "Add event engagement party": {
                        "code": "CreateEvent( has_subject( engagement party ) )",
                        "decomposition": {}
                    },
                    "Add event with Abby kim and desi": {
                        "code": "CreateEvent( AND( with_attendee( Abby ) , with_attendee( Kim ) , with_attendee( Desi ) ) )",
                        "decomposition": {}
                    }
                }
            },
            "Add event to monday 9 pm": {
                "code": "CreateEvent( AND( starts_at( NextDOW( MONDAY ) ) , starts_at( NumberPM( 9 ) ) ) )",
                "decomposition": {}
            }
        }
    }
}
```"""

example2_user = """original question: Create a get-together on Mt. Denali for Saturday morning at 9

code: CreateEvent( AND( at_location( Mt. Denali ) , has_subject( get-together ) , starts_at( NextDOW( SATURDAY ) ) , starts_at( NumberAM( 9 ) ) ) )

decomposition:
```json
{"""

example2_assistant = """
    "Create a get-together on Mt. Denali for Saturday morning at 9": {
        "code": "CreateEvent( AND( at_location( Mt. Denali ) , has_subject( get-together ) , starts_at( NextDOW( SATURDAY ) ) , starts_at( NumberAM( 9 ) ) ) )",
        "decomposition": {
            "Create a get-together on Mt. Denali": {
                "code": "CreateEvent( AND( at_location( Mt. Denali ) , has_subject( get-together ) ) )",
                "decomposition": {
                    "Create a get-together": {
                        "code": "CreateEvent( has_subject( get-together ) )",
                        "decomposition": {}
                    },
                    "Create event on Mt. Denali": {
                        "code": "CreateEvent( at_location( Mt. Denali ) )",
                        "decomposition": {}
                    }
                }
            },
            "Create event for Saturday morning at 9": {
                "code": "CreateEvent( AND( starts_at( NextDOW( SATURDAY ) ) , starts_at( NumberAM( 9 ) ) ) )",
                "decomposition": {
                    "Create event for Saturday": {
                        "code": "CreateEvent( starts_at( NextDOW( SATURDAY ) ) )",
                        "decomposition": {}
                    },
                    "Create event for morning at 9": {
                        "code": "CreateEvent( starts_at( NumberAM( 9 ) ) )",
                        "decomposition": {}
                    }
                }
            }
        }
    }
}
```"""

example3_user = """original question: Remind me to ping rohit and his team .

code: do( Let( x0 , Rohit ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x1 ) ) , has_subject( ping ) ) )

decomposition:
```json
{"""

example3_assistant = """
    "Remind me to ping rohit and his team": {
        "code": "do( Let( x0 , Rohit ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , has_subject( ping ) ) ) )",
        "decomposition": {
            "Remind me to ping rohit": {
                "code": "do( Let( x0 , Rohit ) , CreateEvent( AND( with_attendee( $ x0 ) , has_subject( ping ) ) ) )",
                "decomposition": {
                    "Remind me to ping": {
                        "code": "CreateEvent( has_subject( ping ) )",
                        "decomposition": {}
                    },
                    "Remind me of rohit": {
                        "code": "do( Let( x0 , Rohit ) , CreateEvent( with_attendee( $ x0 ) ) )",
                        "decomposition": {}
                    }
                }
            },
            "Remind me to ping rohit's team": {
                "code": "do( Let( x0 , Rohit ) , CreateEvent( AND( with_attendee( FindTeamOf( recipient= $ x0 ) ) , has_subject( ping ) ) ) )",
                "decomposition": {
                    "Remind me to ping": {
                        "code": "CreateEvent( has_subject( ping ) )",
                        "decomposition": {}
                    },
                    "Remind me of rohit's team": {
                        "code": "do( Let( x0 , Rohit ) , CreateEvent( with_attendee( FindTeamOf( recipient= $ x0 ) ) ) )",
                        "decomposition": {}
                    }
                }
            }
        }
    }
}
```"""

example4_user = """original question: schedule pizza party after the game with Roma, her boss and their other team members

code: do( Let( x0 , Roma ) , CreateEvent( AND( with_attendee( FindManager( $ x0 ) ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , has_subject( pizza party ) , starts_at( :end( FindEvents( has_subject( game ) ) ) ) ) )

decomposition:
```json
{"""

example4_assistant = """
    "schedule pizza party after the game with Roma, her boss and their other team members": {
        "code": "do( Let( x0 , Roma ) , CreateEvent( AND( with_attendee( FindManager( $ x0 ) ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) , has_subject( pizza party ) , starts_at( :end( FindEvents( has_subject( game ) ) ) ) ) ) )",
        "decomposition": {
            "schedule pizza party after the game": {
                "code": "CreateEvent( AND( has_subject( pizza party ) , starts_at( :end( FindEvents( has_subject( game ) ) ) ) ) )",
                "decomposition": {
                    "schedule pizza party": {
                        "code": "CreateEvent( has_subject( pizza party ) )",
                        "decomposition": {}
                    },
                    "schedule event after the game": {
                        "code": "CreateEvent( starts_at( :end( FindEvents( has_subject( game ) ) ) ) )",
                        "decomposition": {}
                    }
                }
            },
            "schedule event with Roma, her boss and their other team members": {
                "code": "do( Let( x0 , Roma) , CreateEvent( AND( with_attendee( FindManager( $ x0 ) ) , with_attendee( FindTeamOf( recipient= $ x0 ) ) ) ) )",
                "decomposition": {
                    "schedule event with Roma": {
                        "code": "do( Let( x0 , Roma) , CreateEvent( with_attendee( $ x0 ) ) )",
                        "decomposition": {}
                    },
                    "schedule event with Roma's boss": {
                        "code": "do( Let( x0 , Roma) , CreateEvent( with_attendee( FindManager( $ x0 ) ) ) )",
                        "decomposition": {}
                    },
                    "schedule event with Roma's team members": {
                        "code": "do( Let( x0 , Roma) , CreateEvent( with_attendee( FindTeamOf( recipient= $ x0 ) ) ) )",
                        "decomposition": {}
                    }
                }
            }
        }
    }
}
```"""

example5_user = """original question: "Arrange a brainstorming session with Jordan and their direct reports next Wednesday afternoon."

code: do( Let( x0 , Jordan ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindReports( $ x0 ) ) , has_subject( brainstorming session ) , starts_at( DateTime( NextDOW( WEDNESDAY ) , Afternoon() ) ) ) ) )

decomposition:
```json
{"""

example5_assistant = """
    "Arrange a brainstorming session with Jordan and their direct reports next Wednesday afternoon": {
        "code": "do( Let( x0 , Jordan ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindReports( $ x0 ) ) , has_subject( brainstorming session ) , starts_at( DateTime( NextDOW( WEDNESDAY ) , Afternoon() ) ) ) ) )",
        "decomposition": {
            "Arrange a brainstorming session with Jordan and their direct reports": {
                "code": "do( Let( x0 , Jordan ) , CreateEvent( AND( with_attendee( $ x0 ) , with_attendee( FindReports( $ x0 ) ) , has_subject( brainstorming session ) ) ) )",
                "decomposition": {
                    "Arrange a brainstorming session with Jordan": {
                        "code": "do( Let( x0 , Jordan ) , CreateEvent( AND( with_attendee( $ x0 ) , has_subject( brainstorming session ) ) ) )",
                        "decomposition": {
                            "Arrange a brainstorming session": {
                                "code": "CreateEvent( has_subject( brainstorming session ) )",
                                "decomposition": {}
                            },
                            "Arrange event with Jordan": {
                                "code": "do( Let( x0 , Jordan ) , CreateEvent( with_attendee( $ x0 ) ) )",
                                "decomposition": {}
                            }
                        }
                    },
                    "Arrange a brainstorming session with Jordan's direct reports": {
                        "code": "do( Let( x0 , Jordan ) , CreateEvent( AND( with_attendee( FindReports( $ x0 ) ) , has_subject( brainstorming session ) ) ) )",
                        "decomposition": {
                            "Arrange a brainstorming session": {
                                "code": "CreateEvent( has_subject( brainstorming session ) )",
                                "decomposition": {}
                            },
                            "Arrange event with Jordan's direct reports": {
                                "code": "do( Let( x0 , Jordan ) , CreateEvent( with_attendee( FindReports( $ x0 ) ) ) )",
                                "decomposition": {}
                            }
                        }
                    }
                }
            },
            "Arrange event next Wednesday afternoon": {
                "code": "CreateEvent( starts_at( DateTime( NextDOW( WEDNESDAY ) , Afternoon() ) ) )",
                "decomposition": {
                    "Arrange event next Wednesday": {
                        "code": "CreateEvent( starts_at( NextDOW( WEDNESDAY ) ) )",
                        "decomposition": {}
                    },
                    "Arrange event in the afternoon": {
                        "code": "CreateEvent( starts_at( Afternoon() ) )",
                        "decomposition": {}
                    }
                }
            }
        }
    }
}
```"""

example6_user = """original question: ok mark me as busy from 8 : 30 to 10

code: do( Let( x0 , NextTime( time= HourMinuteAm( hours= 8 , minutes= 30 ) ) ) , CreateEvent( AND( starts_at( $ x0 ) , ends_at( AND( GE( $ x0 ) , NumberAM( 10 ) ) ) , has_status( ShowAsStatus( Busy ) ) ) ) )

decomposition:
```json
{"""

example6_assistant = """
    "ok mark me as busy from 8 : 30 to 10": {
        "code": "do( Let( x0 , NextTime( time= HourMinuteAm( hours= 8 , minutes= 30 ) ) ) , CreateEvent( AND( starts_at( $ x0 ) , ends_at( AND( GE( $ x0 ) , NumberAM( 10 ) ) ) , has_status( ShowAsStatus( Busy ) ) ) ) )",
        "decomposition": {
            "mark me as busy from 8 : 30": {
                "code": "do( Let( x0 , NextTime( time= HourMinuteAm( hours= 8 , minutes= 30 ) ) ) , CreateEvent( AND( starts_at( $ x0 ) , has_status( ShowAsStatus( Busy ) ) ) ) )",
                "decomposition": {
                    "mark me as busy": {
                        "code": "CreateEvent( has_status( ShowAsStatus( Busy ) ) )",
                        "decomposition": {}
                    },
                    "mark event from 8 : 30": {
                        "code": "do( Let( x0 , NextTime( time= HourMinuteAm( hours= 8 , minutes= 30 ) ) ) , CreateEvent( starts_at( $ x0 ) ) )",
                        "decomposition": {}
                    }
                }
            },
            "mark event to end at 10": {
                "code": "CreateEvent( ends_at( NumberAM( 10 ) ) )",
                "decomposition": {}
            }
        }
    }
}
```"""

FEW_SHOT_EXAMPLES = [
    (example1_user, example1_assistant),
    (example2_user, example2_assistant),
    (example3_user, example3_assistant),
    (example4_user, example4_assistant),
    (example5_user, example5_assistant),
    (example6_user, example6_assistant)
]

