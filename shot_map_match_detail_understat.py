# -*- coding: utf-8 -*-
"""Shot map Match Detail_Understat.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1oHwC8Z0fN4KKZj-914aw-r7MdNNnNepP
"""

# Commented out IPython magic to ensure Python compatibility.
# Data Handling & Analysis
import datetime

import numpy as np
import pandas as pd

# Data Visualisation
import matplotlib.pyplot as plt
# %config InlineBackend.figure_format='retina'  # enable retina display

import matplotlib.image as image

from matplotlib.patches import Arc
from matplotlib.offsetbox import AnnotationBbox, OffsetImage

# Web Scraping
import json
import requests

from bs4 import BeautifulSoup

def draw_pitch(x_min=0,
               x_max=105,
               y_min=0,
               y_max=68,
               pitch_color='w',
               line_color='grey',
               line_thickness=1.5,
               point_size=20,
               orientation='horizontal',
               aspect='full',
               ax=None):

    if not ax:
        raise TypeError('This function is intended to be used with an existing fig and ax in order to allow flexibility in plotting of various sizes and in subplots.')

    if orientation.lower().startswith('h'):
        first = 0
        second = 1
        arc_angle = 0

        if aspect == 'half':
            ax.set_xlim(x_max / 2, x_max + 5)

    elif orientation.lower().startswith('v'):
        first = 1
        second = 0
        arc_angle = 90

        if aspect == 'half':
            ax.set_ylim(x_max / 2, x_max + 5)

    else:
        raise NameError('You must choose one of horizontal or vertical')

    ax.axis('off')

    rect = plt.Rectangle((x_min, y_min),
                         x_max,
                         y_max,
                         facecolor=pitch_color,
                         edgecolor='none',
                         zorder=-2)

    ax.add_artist(rect)

    x_conversion = x_max / 100
    y_conversion = y_max / 100

    pitch_x = [0, 5.8, 11.5, 17, 50, 83, 88.5, 94.2, 100]  # pitch x markings
    pitch_x = [x * x_conversion for x in pitch_x]

    pitch_y = [0, 21.1, 36.6, 50, 63.2, 78.9, 100]  # pitch y markings
    pitch_y = [x * y_conversion for x in pitch_y]

    goal_y = [45.2, 54.8]  # goal posts
    goal_y = [x * y_conversion for x in goal_y]

    # side and goal lines
    lx1 = [x_min, x_max, x_max, x_min, x_min]
    ly1 = [y_min, y_min, y_max, y_max, y_min]

    # outer boxed
    lx2 = [x_max, pitch_x[5], pitch_x[5], x_max]
    ly2 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    lx3 = [0, pitch_x[3], pitch_x[3], 0]
    ly3 = [pitch_y[1], pitch_y[1], pitch_y[5], pitch_y[5]]

    # goals
    lx4 = [x_max, x_max + 2, x_max + 2, x_max]
    ly4 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    lx5 = [0, -2, -2, 0]
    ly5 = [goal_y[0], goal_y[0], goal_y[1], goal_y[1]]

    # 6 yard boxes
    lx6 = [x_max, pitch_x[7], pitch_x[7], x_max]
    ly6 = [pitch_y[2], pitch_y[2], pitch_y[4], pitch_y[4]]

    lx7 = [0, pitch_x[1], pitch_x[1], 0]
    ly7 = [pitch_y[2], pitch_y[2], pitch_y[4], pitch_y[4]]

    # Halfway line, penalty spots, and kickoff spot
    lx8 = [pitch_x[4], pitch_x[4]]
    ly8 = [0, y_max]

    lines = [
        [lx1, ly1],
        [lx2, ly2],
        [lx3, ly3],
        [lx4, ly4],
        [lx5, ly5],
        [lx6, ly6],
        [lx7, ly7],
        [lx8, ly8],
    ]

    points = [[pitch_x[4], pitch_y[3]]]

    circle_points = [pitch_x[4], pitch_y[3]]
    arc_points1 = [pitch_x[6], pitch_y[3]]
    arc_points2 = [pitch_x[2], pitch_y[3]]

    for line in lines:
        ax.plot(line[first],
                line[second],
                color=line_color,
                lw=line_thickness,
                zorder=-1)

    for point in points:
        ax.scatter(point[first],
                   point[second],
                   color=line_color,
                   s=point_size,
                   zorder=-1)

    circle = plt.Circle((circle_points[first], circle_points[second]),
                        x_max * 0.088,
                        lw=line_thickness,
                        color=line_color,
                        fill=False,
                        zorder=-1)

    ax.add_artist(circle)

    arc1 = Arc((arc_points1[first], arc_points1[second]),
               height=x_max * 0.088 * 2,
               width=x_max * 0.088 * 2,
               angle=arc_angle,
               theta1=128.75,
               theta2=231.25,
               color=line_color,
               lw=line_thickness,
               zorder=-1)

    ax.add_artist(arc1)

    arc2 = Arc((arc_points2[first], arc_points2[second]),
               height=x_max * 0.088 * 2,
               width=x_max * 0.088 * 2,
               angle=arc_angle,
               theta1=308.75,
               theta2=51.25,
               color=line_color,
               lw=line_thickness,
               zorder=-1)

    ax.add_artist(arc2)

    ax.set_aspect('equal')

    return ax

print('Function Defined! ✔️')

#ใส่ match ID ที่ต้องการลงไป
match_id = 21934
url = 'https://understat.com/match/{}'.format(match_id)

response = requests.get(url)
soup = BeautifulSoup(response.content, 'lxml')

# Retrieve all data with a <script> tag - Field data are in the second <script> group
script_data = soup.find_all('script')
field_stats = script_data[1].string

# Strip unnecessary symbols and get only JSON data
ind_start = field_stats.index("('") + 2
ind_end = field_stats.index("')")

json_data = field_stats[ind_start:ind_end]
json_data = json_data.encode('utf8').decode('unicode_escape')

# Convert string to json format
data = json.loads(json_data)

df_home = pd.DataFrame(data['h'])
df_away = pd.DataFrame(data['a'])

data.keys()

table = soup.find('div', {'class': 'scheme-block', 'data-scheme': 'stats'})

cols = [val.text for val in table.find_all('div', {'class': 'progress-title'})]
vals = [val.text for val in table.find_all('div', {'class': 'progress-value'})]

summary_dict = {}
j = 0
for i in range(len(cols)):
    summary_dict[cols[i]] = vals[j:j + 2]

    increment = 3 if i == 1 else 2
    j += increment

df_summary = pd.DataFrame(summary_dict, index=['Home', 'Away']).T
df_summary.drop(['CHANCES'], inplace=True)
df_summary.index = ['Teams', 'Goals', 'xG', 'Shots', 'On Target', 'DEEP', 'PPDA', 'xPTS']
df_summary

date = data['h'][0]['date'].split()[0]
date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
date = date.strftime('%d %B %Y')

print('Match Date: ', date)

headline = '{} {} - {} {}'.format(df_summary.loc['Teams', 'Home'],
                                  df_summary.loc['Goals', 'Home'],
                                  df_summary.loc['Teams', 'Away'],
                                  df_summary.loc['Goals', 'Away'])

print('Headline: ', headline)

teams_full = [
    'Manchester City', 'Liverpool', 'Chelsea', 'Arsenal', 'West Ham',
    'Tottenham', 'Manchester United', 'Wolverhampton Wanderers', 'Brighton',
    'Leicester', 'Crystal Palace', 'Brentford', 'Aston Villa', 'Southampton',
    'Everton', 'Leeds', 'Watford', 'Burnley', 'Newcastle United', 'Norwich',
    'Bournemouth', 'Nottingham Forest', 'Fulham','Burnley','Luton','Sheffield United'
]

teams_short = [
    'Man City', 'Liverpool', 'Chelsea', 'Arsenal', 'West Ham', 'Tottenham',
    'Man United', 'Wolves', 'Brighton', 'Leicester', 'Crystal Palace',
    'Brentford', 'Aston Villa', 'Southampton', 'Everton', 'Leeds', 'Watford',
    'Burnley', 'Newcastle', 'Norwich', 'AFC Bounce', 'Forest', 'Fulham','Burnley','Luton','Sheffield'
]

teams_short = [f'{string:^11}' for string in teams_short]

idx = [i for i, v in enumerate(teams_full) if v == df_summary.loc['Teams', 'Home']]
home_team_short = teams_short[idx[0]]

idx = [i for i, v in enumerate(teams_full) if v == df_summary.loc['Teams', 'Away']]
away_team_short = teams_short[idx[0]]

print('Short teams names\nHome: {} \nAway: {}'.format(home_team_short,
                                                      away_team_short))

url_home = '../content/{}.png'.format(df_summary.loc['Teams', 'Home'])
img_home = image.imread(url_home)

url_away = '../content/{}.png'.format(df_summary.loc['Teams', 'Away'])
img_away = image.imread(url_away)

float_cols = ['X', 'Y', 'xG']
for df in [df_home, df_away]:
    df[float_cols] = df[float_cols].astype('float64')

goals_home = df_home[df_home['result'] == 'Goal']
shots_home = df_home[df_home['result'] != 'Goal']

goals_away = df_away[df_away['result'] == 'Goal']
shots_away = df_away[df_away['result'] != 'Goal']

bg_color = '#0f253a'
goal_color = 'red'
edgecolor = 'Yellow'
plt.rcParams['text.color'] = 'White'

plt.rcParams['font.family'] = 'Century Gothic'
plt.rcParams.update({'font.size': 24})

fig, ax = plt.subplots(figsize=(18.48, 12), facecolor=bg_color)

draw_pitch(pitch_color=bg_color, line_color='lightgrey', ax=ax)

### 01 - Shots and Goals ###
for i, df in enumerate([shots_home, goals_home]):
    ax.scatter(x=105 - df['X'] * 105,
               y=68 - df['Y'] * 68,
               s=df['xG'] * 1024,
               lw=[2, 1][i],
               alpha=0.7,
               facecolor=[edgecolor, goal_color][i],
               edgecolor=edgecolor)

for i, df in enumerate([shots_away, goals_away]):
    ax.scatter(x=df['X'] * 105,
               y=df['Y'] * 68,
               s=df['xG'] * 1024,
               lw=[2, 1][i],
               alpha=0.7,
               facecolor=[edgecolor, goal_color][i],
               edgecolor=edgecolor)

### 02 - Title & Subtitle ###
ax.text(x=0, y=75, s=headline, size=35, weight='bold')
ax.text(x=0, y=71, s='Premier League 2023-24  |  {} | GW4'.format(date), size=20)


### 03 - Team Names ###
for i, team in zip([-1, 1], [home_team_short, away_team_short]):
    ax.text(x=105 / 2 + i * 14,
            y=63,
            s=team,
            size=35,
            ha='center',
            weight='bold')


### 05 - Stats ###
features = ['Goals', 'xG', 'Shots', 'On Target', 'DEEP','PPDA']
for i, feature in enumerate(features):
    if float(df_summary.loc[feature, 'Home']) > float(df_summary.loc[feature, 'Away']):
        weights = ['bold', 'normal']
    elif float(df_summary.loc[feature, 'Home']) < float(df_summary.loc[feature, 'Away']):
        weights = ['normal', 'bold']
    else:
        weights = ['normal', 'normal']

    ax.text(x=105 / 2,
            y=46 - i * 8,
            s=feature,
            size=22,
            ha='center',
            va='center',
            bbox=dict(facecolor='darkgray',
                      edgecolor=edgecolor,
                      alpha=0.85,
                      pad=0.6,
                      boxstyle='round'))

    ax.text(x=105 / 2 - 14,
            y=46 - i * 8,
            s=df_summary.loc[feature, 'Home'],
            size=20,
            ha='center',
            va='center',
            weight=weights[0],
            bbox=dict(facecolor='firebrick',
                      edgecolor='w',
                      alpha=0.6,
                      pad=0.6,
                      boxstyle='round'))

    ax.text(x=105 / 2 + 14,
            y=46 - i * 8,
            s=df_summary.loc[feature, 'Away'],
            size=20,
            ha='center',
            va='center',
            weight=weights[1],
            bbox=dict(facecolor='firebrick',
                      edgecolor='w',
                      alpha=0.6,
                      pad=0.6,
                      boxstyle='round'))

### 06 - Legend - Outcome ###
ax.text(x=105 / 4 + 0, y=-5, s='Outcome:', ha='center')
ax.text(x=105 / 4 - 8, y=-10, s='Shot', ha='center')
ax.text(x=105 / 4 + 8, y=-10, s='Goal', ha='center')

for i in range(2):
    ax.scatter(x=[105 / 4 - 14, 105 / 4 + 1.5][i],
               y=-8.8,
               s=500,
               lw=[2, 1][i],
               alpha=0.7,
               facecolor=[edgecolor, goal_color][i],
               edgecolor=edgecolor)

### 07 - Legend - xG value ###
ax.text(x=3 * 105 / 4, y=-5, s='xG Value:', ha='center')

for i in range(0, 5):
    ax.scatter(x=[69.8, 73.4, 77.7, 82.4, 87.5][i],
               y=-8.5,
               s=((i + 1) * 0.2) * 500,
               lw=2,
               color='Yellow',
               edgecolor=edgecolor)

### 08 - Legend - Credit ###
credit_text = 'Data: Opta | Saran DATAFPL'
ax.text(x=105, y=-14, s=credit_text, size=16, ha='right')

# plt.savefig('Figure.png')


### 10 - Team Logos ###
for i, img in zip([-1, 1], [img_home, img_away]):

    imagebox = OffsetImage(img, zoom=0.4)
    ab = AnnotationBbox(imagebox, (105 / 2 + i * 14, 56), frameon=False)
    ax.add_artist(ab)

plt.show()