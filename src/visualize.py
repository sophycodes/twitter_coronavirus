#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_path',required=True)
parser.add_argument('--key',required=True)
parser.add_argument('--percent',action='store_true')
args = parser.parse_args()

# imports
import os
import json
from collections import Counter,defaultdict

# open the input path
with open(args.input_path) as f:
    counts = json.load(f)

# normalize the counts by the total values
if args.percent:
    for k in counts[args.key]:
        counts[args.key][k] /= counts['_all'][k]

# import matplotlib and set Agg backend so it saves to file instead of opening a window
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

# Korean
fm.fontManager.addfont('/usr/share/fonts/truetype/baekmuk/batang.ttf')
# Japanese
fm.fontManager.addfont('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf')
# Chinese
fm.fontManager.addfont('/usr/share/fonts/truetype/arphic/uming.ttc')

plt.rcParams['font.family'] = ['Baekmuk Batang', 'IPAexGothic', 'AR PL UMing CN']

# sort all counts low to high, then take only the last 10 (the top 10 highest)
items = sorted(counts[args.key].items(), key=lambda item: item[1], reverse=False)[-10:]

# separate the (key, value) pairs into two lists for the x and y axes
keys = [item[0] for item in items]
values = [item[1] for item in items]

# create the bar chart
plt.figure(figsize=(10,6))
plt.bar(keys, values)

# label the axes and title
plt.xlabel('Language/Country')
plt.ylabel('Count')
plt.title(f'{args.key} by {args.input_path}')

# rotate x-axis labels so they don't overlap
plt.xticks(rotation=45)

# adjust spacing so nothing gets cut off
plt.tight_layout()

# build output filename from hashtag and input file
output_file = 'img/' + args.key.replace('#','') + '_' + os.path.basename(args.input_path) + '.png'

# save the plot as a png file
plt.savefig(output_file)
print('saved to', output_file)
