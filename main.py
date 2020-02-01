from RugbyMatch import RugbyMatch
from DisplayController import DisplayController

match = RugbyMatch('EVP3013155')
display = DisplayController()

print(match.match_stats)
print(match.team_stats)

out = match.team_stats[0]['abbreviatedName'] + " 5 - 3 " + match.team_stats[1]['abbreviatedName']
display.display_txt(out)
