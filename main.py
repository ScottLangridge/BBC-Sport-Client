from time import sleep

from RugbyMatch import RugbyMatch

from DisplayController import DisplayController

match = RugbyMatch('EVP3013155')
display = DisplayController()

team_names = [team['displayName'] for team in match.team_stats]
scoreline = ""
while True:
    scores = [str(team['runningScore']) for team in match.team_stats]
    scores[0] = scores[0].rjust(2, ' ')
    scores[1] = scores[1].ljust(2, ' ')

    last_scoreline = scoreline
    scoreline = '%s %s - %s %s' % (team_names[0], scores[0], scores[1], team_names[1])
    if scoreline != last_scoreline:
        display.display_txt(scoreline)

    sleep(30)
    try:
       match.update()
    except:
        print("EXCEPTION!")

