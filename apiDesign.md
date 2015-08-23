Scheduling REST api design
====================

/schedule
------

returns the complete schedule, all of it (in JSON format):

	[
		{
			"start":"2015-11-21T13:00:00Z",
			"end":"2015-11-21T13:05:00Z",
			"teamId":21234,
			"teamName":"superduperdodo's",
			"location":"table1",
			"activity":"match"
		},
		...
	]

Notes:

- array of single events
- start time required, end time may be optional
- times as iso8601 formatted string

/schedule?teamId=21234
------

returns all the events for particular team

/schedule?location=table1
-------

returns all the events for a particular location

/schedule?activity=match
--------

returns all the events of a particular activity (matches, judging, breaks, opening, etc...)

/schedule?time=2015-11-21T13:05:00Z
--------

returns all events that start or are in progress at the given time

/schedule?teamId=21234&activity=match
---------

query parameters can be combined to create stricter search queries. In this case all matches for team 21234

/schedule/now
--------

returns all events that occur now, may take additional query parameters as above (to filter on team, activity etc)

/schedule/due
--------

returns all events that are up next, may take additional query paramaters as above (to filter on team, activity, etc)

/teams
--------

returns just the set of all teams:

	[
		{"teamId":21234,"teamName":"superduperdodo's"}
		...
	]

/locations
---------

returns just the set of locations:

	[
		{"location":"table1"},
		{"location":"table2"},
		{"location":"main stage"}
	]

/activities
-----

returns just the set of activities:

	[
		{"activity":"match"},
		{"activity":"opening"},
		{"activity":"break"},
	]

mhub messages
==========

this needs some thinking. The system may send messages when

- the start time of an event commences
- the start time of an event is due in x minutes (10,5,0)
