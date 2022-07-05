#!/usr/bin/env python3

import os
import sys
import requests
import pandas as pd

home = os.path.expanduser("~")

cache_dir = '/.cache/dm-aria'

if not os.path.exists(home + cache_dir):
    os.makedirs(home + cache_dir)

os.system('dmenu -p Search <&- > ~/.cache/dm-aria/dmenu_out.txt')
dmenu_out_file = open(home + cache_dir + '/dmenu_out.txt')
dmenu_out = dmenu_out_file.read().replace('\n', '')
dmenu_out_file.close()

if dmenu_out == '':
    sys.exit(0)

webpage_source_list = requests.get('https://thepiratebay.party/search/' + dmenu_out + '/1/99/0').text.splitlines()
titles = []
magnet_uris = []
sizes = []
seeders = []
leechers = []
for i in range(1, len(webpage_source_list)):
    if webpage_source_list[i].startswith('<td><a href="https://thepiratebay.party/torrent/'):
        titles.append(webpage_source_list[i])
    elif webpage_source_list[i].startswith('<td><nobr><a href="magnet:?xt=urn:btih:'):
        magnet_uris.append(webpage_source_list[i])
        sizes.append(webpage_source_list[i+1])
        seeders.append(webpage_source_list[i+2])
        leechers.append(webpage_source_list[i+3])

if len(titles) == 0:
    print('No titles found')
    sys.exit(0)

if len(titles) != len(magnet_uris):
    print('Title / magnet link length mismatch; check source code')
    sys.exit(1)

pretty_titles = []
pretty_sizes = []
pretty_seeders = []
pretty_leechers = []
magnet_uris_cleaned = []
for i in range(len(titles)):
    pretty_titles.append(titles[i].partition('">')[2].rpartition('</a>')[0])
    pretty_sizes.append(sizes[i].partition('">')[2].rpartition('</td>')[0].replace('&nbsp;', ' '))
    pretty_seeders.append(seeders[i].partition('">')[2].rpartition('</td>')[0])
    pretty_leechers.append(leechers[i].partition('">')[2].rpartition('</td>')[0])
    magnet_uris_cleaned.append(magnet_uris[i].partition('href="')[2].rpartition('" title="Download')[0])

row_nums_df = pd.DataFrame(range(1, len(titles)+1))
titles_df = pd.DataFrame(pretty_titles)
sizes_df = pd.DataFrame(pretty_sizes)
seeders_df = pd.DataFrame(pretty_seeders)
leechers_df = pd.DataFrame(pretty_leechers)

selection_df = pd.concat([row_nums_df, titles_df, sizes_df, seeders_df, leechers_df], axis=1)
selection_df.columns = ['Num', 'Title', 'Size', 'Seeders', 'Leechers']

cache_file = open(home + cache_dir + '/dmenu_out.txt', 'w+')
cache_file.writelines(selection_df.to_string(header=True, index=False))
cache_file.close()

os.system('cat ' + home + cache_dir + '/dmenu_out.txt | dmenu -i -l 50 -p Selection > ' + home + cache_dir + '/selection.txt')

selection_file = open(home + cache_dir + '/selection.txt')
selection = selection_file.read()

if selection == '':
    sys.exit(0)

selection = selection.replace(' ', '')[0]

selection_file.close()

magnet_uris_file = open(home + cache_dir + '/magnet_uris.txt', 'a')
magnet_uris_file.write(magnet_uris_cleaned[int(selection)-1] + '\n')
magnet_uris_file.close()

