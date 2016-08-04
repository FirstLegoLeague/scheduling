
# Overview
An application that can provide an overview of which team is expected where (ie. which event), that can be queried to obtain specific information for a person or team. The goal of this application is to provision schedule information to other applications, such as mobile websites for teams, event displays and 

# Schedule elements:
- Activity: an activity that the team needs to complete (robot match 1, Project judging session, etc)
- TeamId / TeamName: who is completeing the activity (team 1)
- Location: where the activity take place (Judging room A, table 6, Pit Area A5)
- Start / End: when the activity is scheduled to take place (times as iso8601 formatted string: 2015-11-21AT13:05:00Z)

Note that activities can also be:
- Ceremonies that apply to all: opening ceremonies, award ceremony
- Breaks: either for a team, or for all teams,

# Functions: 
## Before the tournament: create / import the schedule:
Before the tournament the event organizer generates a schedule with one of the existing tools, or manually creates it in a spreadsheet program. This file is imported and parsed to fill the database ahead of the event.

1. Receive or generate schedule in one of the existing tools.
2. Launch schedule application, select import function. Select the generator (origin) of the schedule, so the tool knows how to parse it.
3. Copy/paste schedule from Excel. 
4. Optionally: manually assign columns to schedule elements (in case of a unknown or manual format) 
5. Records are created for each (possible) event.
6. Optionally: do some checking:
  - Duplicate records
  - Team scheduled to be in more than place

*Use case 1*: The event organizer has used the FLL tournament scheduler tool,

## API
Once the events are loaded, the information can be accessed by different modules through an API. Other modules / applications should be able to make the following API calls: [Api Design](https://github.com/FirstLegoLeague/scheduling/blob/master/apiDesign.md)
 
*Use case 1*: A mobile website for teams features a dropdown list. The team select their own team/name number and the site performs the following api call: `/schedule?teamId=21234`. The schedule module returns the events for the events for this team, including the location sorted by time.

*Use case 2*: In the scoring application, the referee can select their table (A), the scoring application performs the following call: `/schedule?location=table1`. The scoring application filters down the upcoming and next teams and displays them to the referee.

*Use case 3*: A display in the pit area shows the upcoming events, the display application requests `/schedule/due` or `/schedule?time=2015-11-21T13:05:00Z`. The returned data shows the next events which are displayed on the screen.

## Live event & Mhub 
In addition the API, the application should also push messages on the message hub. This allows the trigger of events in other applications. For example trigger a notification in a team application about delays in the schedule. 
 
- Shift the schedule
 1. Ask for a delay in minutes, and confirmation
 2. Trigger a message on the MHub: ``
 3. Recalculate the 'real time' field: real time + delay
- Move team to different location /time
 1. Select team and activity, show original team and location
 2. Select new location and/or time
 3. Check for conflicts: location in use, team not available
 4. Confirm change and publish MHub message: ``
 
*Use case 1:* 

*Use case 2:* 
 
# Output
- Provide website that can be accessed/published by the visitors, ahead of and during the event.
  - Select a specific team and retrieve schedule
  - Select a specific location and show the schedule
  - Now & Next: show current activities and the next 10 minutes
  - What is happening at xxx: show the events schedule. 
- Printouts, generate PDFs with the schedule...
  - Per team
- Per location
  - Per activity
  - Per time (period)

*Use case 1:* 

# TODOS:
- Agreement on the import format from Excel.
- Discuss how to allow generation and application setup on a device ahead of the event and to be run on a different device during the event (could for example be a zip file, or export function)
- Prevent or work with multiple schedule servers at the event
