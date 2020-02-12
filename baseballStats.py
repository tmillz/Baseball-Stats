#!/usr/bin/python
from __future__ import division
import argparse
import csv

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--player-id', help='Print the player id in the output. This is the default.', action='store_true')

parser.add_argument('-n', '--name', help='Print the player name as "nameFirst nameLast" instead of the player id', action='store_true')

parser.add_argument('-g', '--given-name', help='Print the player name as "nameGiven" instead of the player id', action='store_true')

parser.add_argument('-b', '--batting-avg', help='Print the player batting average This is the default.', action='store_true')

parser.add_argument('-a', '--at-bats-per-home-run', help='Print the player at bats per home run instead of batting average.', action='store_true')

parser.add_argument('-t', '--top', help='Print the top NUM players for the given statistic. The default is 5.', metavar='NUM', type=int, default=5)

parser.add_argument('-s', '--skip', help='Skip the top NUM players before printing. The default is 0.', metavar='NUM', type=int, default=0)

parser.add_argument('-m', '--minimum-at-bats', help="The minimum NUM of at bats for a player to have a qualifying score. The default is 3000.", metavar='NUM', type=int, default=3000)

args = parser.parse_args()

if not (args.name or args.given_name):
  args.player_id = True

if not (args.batting_avg or args.at_bats_per_home_run):
  args.batting_avg = True
elif (args.batting_avg and args.at_bats_per_home_run):
  print 'choose eather -b or -a'
  quit()

def formatPlayer(avg_dict, avg):
  if args.player_id:
    return globals()[avg_dict][avg]
  elif args.name:
    fn = people_dict[globals()[avg_dict][avg]][0]
    ln = people_dict[globals()[avg_dict][avg]][1]
    return (fn +' '+ ln)
  elif args.given_name:
    gn = people_dict[globals()[avg_dict][avg]][2]
    return gn

with open("Batting.csv", "r") as battingcsv:
  reader = csv.reader(battingcsv)
  stats_dict = {}
  next(battingcsv)

  for row in reader:
    ab = int(row[6])
    h = int(row[8])
    hr = int(row[11])

    if row[0] in stats_dict:
      stats_dict[row[0]] = [ stats_dict[row[0]][0]+ab, stats_dict[row[0]][1]+h, stats_dict[row[0]][2]+hr ]
    else:
      stats_dict.update( { row[0]:[ab,h,hr] } )

with open("People.csv", "r") as peoplecsv:
  reader = csv.reader(peoplecsv)
  people_dict = {}
  for row in reader:
    people_dict.update( { row[0]: [row[13],row[14],row[15]] } )

skip = args.skip
top = args.top

if (args.batting_avg == 0 or args.batting_avg > 0) and args.at_bats_per_home_run == 0:
  bat_avgs = {}  
  for s in stats_dict:
    ab = stats_dict[s][0]
    h = stats_dict[s][1]
    if h > 0 and ab > args.minimum_at_bats:
      bat_avgs.update( { h/ab:s } )

  s_bat_avg = sorted(bat_avgs)
  if (skip == 0 and top == 0) or (skip < top):
    for x in range(skip,top):
      print formatPlayer('bat_avgs', s_bat_avg[x]), s_bat_avg[x]
  else:
    print 'skip must be less than top'

elif args.at_bats_per_home_run > 0 and args.batting_avg == 0:
  at_bat_avgs = {}
  for s in stats_dict:
    ab = stats_dict[s][0]
    hr = stats_dict[s][2]
    if hr > 0 and ab > args.minimum_at_bats:
      at_bat_avgs.update({ ab/hr:s })

  s_at_bat_avg = sorted(at_bat_avgs, reverse = True)
  if (skip == 0 and top == 0) or (skip < top):
    for x in range(skip,top):
      print formatPlayer('at_bat_avgs', s_at_bat_avg[x]), s_at_bat_avg[x]
  else:
    print 'skip must be less than top'

else:
  print 'found -a and -b'
  