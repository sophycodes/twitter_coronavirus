#!/usr/bin/env python3

# command line args
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--hashtags', nargs='+', required=True)
args = parser.parse_args()

# imports
import os
import json
import glob
from collections import defaultdict
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.ticker as ticker

# Korean
fm.fontManager.addfont('/usr/share/fonts/truetype/baekmuk/batang.ttf')
# Japanese
fm.fontManager.addfont('/usr/share/fonts/opentype/ipaexfont-gothic/ipaexg.ttf')
# Chinese
fm.fontManager.addfont('/usr/share/fonts/truetype/arphic/uming.ttc')

plt.rcParams['font.family'] = ['Baekmuk Batang', 'IPAexGothic', 'AR PL UMing CN']

# dictionary to store counts for each hashtag over time
# structure: {hashtag: {day: count}}
counts = defaultdict(dict)

# get all .lang files sorted by date
input_files = sorted(glob.glob('outputs/geoTwitter20*.lang'))

# loop over each daily file
for path in input_files:
    # extract the date from the filename e.g. geoTwitter20-01-01.zip.lang -> 01-01
    date = os.path.basename(path).split('geoTwitter20-')[1][:5]

    # load the file
    with open(path) as f:
        data = json.load(f)

    # for each hashtag, sum up all language counts to get total tweets that day
    for hashtag in args.hashtags:
        if hashtag in data:
            # sum all language counts for this hashtag on this day
            total = sum(data[hashtag].values())
        else:
            # hashtag not found in this day's data, so count is 0
            total = 0
        counts[hashtag][date] = total

# get sorted list of dates for x-axis
dates = sorted(set(date for hashtag_counts in counts.values() for date in hashtag_counts))

# plot a line for each hashtag
plt.figure(figsize=(16,6))
for hashtag in args.hashtags:
    values = [counts[hashtag].get(date, 0) for date in dates]
    plt.plot(dates, values, label=hashtag)

# format the plot
plt.xlabel('Day of Year')
plt.ylabel('Number of Tweets')
plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
plt.title('Hashtag Usage Over Time in 2020')
plt.legend()

# only show every 30th date label so x-axis isn't too crowded
plt.xticks(dates[::30], rotation=45)
plt.tight_layout()

# save the plot
plt.savefig('img/alternative_reduce.png')
print('saved to img/alternative_reduce.png')
