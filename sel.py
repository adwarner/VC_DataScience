# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#
#from selenium import webdriver
#
#driver = webdriver.Firefox(executable_path = 
#                           '/Users/adamwarner/Documents/VC Soccer/geckodriver.exe')


import re
from textblob import TextBlob
import numpy as np 
import pandas as pd
import builtins

import sys 
#reload(sys)
#sys.setdefaultencoding("utf-8")


from bs4 import BeautifulSoup
import urllib
import datetime

### We need to get the starters
### Create a matrix of players name, on/off, goal scored, assist, goal against. 

## Have to do this header business to get the HTML code out

headers = { 'User-Agent' : 'Mozilla/5.0' }

## home_away function finds out where VCMS is located on the website whether it 
## is the right or the left side 

def home_away(base_url):
    req = urllib.request.Request(base_url, None, headers)
    r = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(r)
    #test = soup.find_all("div",class_ = 'sidearm-responsive-tabs ui-tabs ui-widget ui-widget-content ui-corner-all')
    test2 = soup.find("div",{'id':'ctl00_contentDiv'})
        
    ## We want to find the table inside the HTML code     
    first_half = test2.find( "table", {"class":"sidearm-table play-by-play"})
    
    # Store the home and away group
    home = []
    away = []
    for row in first_half.thead.findAll('tr'):
        #first_column = row.findAll('th')[0].contents
        home.extend(row.findAll('th')[1].contents)
        away.extend(row.findAll('th')[5].contents)
    return home[0]
    

## Score --> tells us about times the goals were scored. 
def score(base_url):
    req = urllib.request.Request(base_url, None, headers)
    r = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(r)
    #test = soup.find_all("div",class_ = 'sidearm-responsive-tabs ui-tabs ui-widget ui-widget-content ui-corner-all')
    html = soup.find("div",{'id':'ctl00_contentDiv'})
    
    score_table = html.find( "table", {"class":"sidearm-table overall-stats hide-caption highlight-hover no-margin"})
    time = []
    score_board = []
    
    try:
    
        for row in score_table.tbody.findAll('tr'):
            time.extend(row.findAll('th')[0].contents)
            score_board.extend(row.findAll('td')[0].contents)
        
        
        score = []
         
        
        home_team = 0
        away_team = 0
        for i in score_board: 
            try:
                if str(i).strip().index("VCMS") == 10:
                    home_team += 1
                    score.append(str(home_team) + '-' + str(away_team))
                    
            except ValueError:
                try: 
                    if str(i).strip().index("alt") == 5: #and str(i).strip()[10] != 'V':
                        away_team += 1
                        #away_score.append(away_team)
                    score.append(str(home_team) + '-' + str(away_team))
                except ValueError:  
                    pass
        df = pd.DataFrame(data = score,index = time, columns = ['Score'])
        
        ## This part tells us that it is 0-0 until insert minute. 
        q = df.index[0].split(':')[0]+ \
        ':'+str(int(df.index[0].split(':')[1])-1)
        
        dfq = pd.DataFrame(data = ['0-0'], index = [q], columns = ['Score'])
        
        df = pd.concat([dfq,df],0)
        
        keys  = df.index.tolist()
        values = df['Score'].tolist()
        
        dictionary = builtins.dict(zip(keys, values))
    except AttributeError:
        df = pd.DataFrame(data = ['0-0'], index = ['00:00'], columns = ['Score'])
        
        keys  = df.index.tolist()
        values = df['Score'].tolist()
        
        dictionary = builtins.dict(zip(keys, values))
    
    
    return dictionary
            
            
    #return time,score

def scrap_play_by_play(base_url):

    req = urllib.request.Request(base_url, None, headers)
    r = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(r)
    #test = soup.find_all("div",class_ = 'sidearm-responsive-tabs ui-tabs ui-widget ui-widget-content ui-corner-all')
    test2 = soup.find("div",{'id':'ctl00_contentDiv'})
    
    first_half = test2.find( "table", {"class":"sidearm-table play-by-play"})
    
    try:
        if home_away(base_url).index('VCMS') == 0: 
            z = 1
    except ValueError:
         z = 5
    
    first_half_data = []
    first_half_time = []
    score_first_half = []
    score_first_half_part2 = []
    
    for row in first_half.tbody.findAll('tr'):
        #first_column = row.findAll('th')[0].contents
        first_half_data.extend(row.findAll('td')[z].contents)
        first_half_time.extend(row.findAll('td')[0].contents)
        score_first_half.extend(row.findAll('td')[2].contents)
        score_first_half_part2.extend(row.findAll('td')[4].contents)
        
        #print(third_column)
    
    
    plays_first_half = []
    first_time_array = []

    
    for i in first_half_data:
        j = str(i)#.replace('\r','')
        j = " ".join(j.split())
        
        plays_first_half.append(j)
        
    for i in first_half_time:

        time = str(i).rstrip()
        time = "".join(time.split())
        first_time_array.append(time)
    
    df_1 = pd.DataFrame(data = [plays_first_half]).T
    df_1.index = [first_time_array]
    
    
    #### Second Half 
    
    second_half = soup.find("caption", text="Period 2 Plays").find_parent("table")
    second_half_data = []
    second_half_time = []

    score_second_half = []
    score_second_half_part2 =[]
    
    
    for row in second_half.tbody.findAll('tr'):
        #first_column = row.findAll('th')[0].contents
        #third_column = row.findAll('td')[1].contents
        second_half_data.extend(row.findAll('td')[z].contents)
        second_half_time.extend(row.findAll('td')[0].contents)
        score_second_half.extend(row.findAll('td')[2].contents)
        score_second_half_part2.extend(row.findAll('td')[4].contents)
        #print(third_column)
        
        
    plays_second_half = []
    second_time_array = []

    
    for i in second_half_data:
        j = str(i)#.replace('\r','')
        j = " ".join(j.split())
        
        plays_second_half.append(j)
        
    for i in second_half_time:

        time = str(i).rstrip()
        time = "".join(time.split())
        second_time_array.append(time)
        
    df = pd.DataFrame(data = [plays_second_half]).T
    df.index = [second_time_array]
    
    final_game = pd.concat([df_1,df])
    
    
    #return {'Time':second_time_array,'Plays':plays_second_half}
    return final_game


def subs_in_out(play_by_play):
    try:
        test_word = 'substitution:'
        # I truncated your sentence
        test_words = play_by_play.lower().split()
        correct_case = play_by_play.split() # this will preserve the case of the original words
        # and it will be identical in length to test words with each word in the same position
        position = test_words.index(test_word)
        player_in = ' '.join(correct_case[position+1:position+3])
            
        player_out = ' '.join(correct_case[position+4:position+6])
        player_out = player_out.rstrip('.')
        
        try:
            if player_in.index('Hayden') == 0:
                player_in = ' '.join(correct_case[position+1:position+4])
                player_out = ' '.join(correct_case[position+5:position+7])
                player_out = player_out.rstrip('.')
        except ValueError:
            pass
        
        try:
            if player_out.index('Hayden') == 0:
                player_out = ' '.join(correct_case[position+4:position+7])
                player_out = player_out.rstrip('.')
        except ValueError:
            pass
        
        return player_in, player_out
    
    except ValueError:
        pass



def In_Out(game_data):

    in_out = game_data[0].apply(subs_in_out).dropna()
    
    In = []
    Out = []
    for i in in_out: 
        In.append(i[0])
        Out.append(i[1])
        
    Time = in_out.index.tolist()   
    df = pd.DataFrame(data = [In, Out,Time]).T
    df.index = in_out.index
    df.columns = ['In','Out','Time']
    return df


def map_score_to_time(time, scores):
    score_at_sub = '0-0'
    for score_time, score in sorted(scores.items(), key=lambda kv: kv[1]):
        if time > score_time or time == score_time:
            score_at_sub = score
    return score_at_sub


def date(base_url):
    req = urllib.request.Request(base_url, None, headers)
    r = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(r)
    #test = soup.find_all("div",class_ = 'sidearm-responsive-tabs ui-tabs ui-widget ui-widget-content ui-corner-all')
    html = soup.find("section",{'id':'box-score'})
    
    date_table = html.find( "dl", {"class":"text-center inline"})
    date = []
    for row in date_table.find('dd'):
        date.append(row)
    
    return date

def time_map(s): 
    try: 
        mapped_time = int(s.split(':')[0])+int(s.split(':')[1])/60
    except ValueError: 
        mapped_time = int(s.split(':')[1])/60
    return mapped_time

def final_dataframe(base_url):
    Subs = In_Out(scrap_play_by_play(base_url))
    Score = score(base_url)
    
    req = urllib.request.Request(base_url, None, headers)
    r = urllib.request.urlopen(req).read()
    
    soup = BeautifulSoup(r)
    #test = soup.find_all("div",class_ = 'sidearm-responsive-tabs ui-tabs ui-widget ui-widget-content ui-corner-all')
    html = soup.find("section",{'id':'box-score'})
    
    date_table = html.find( "dl", {"class":"text-center inline"})
    date = []
    for row in date_table.find('dd'):
        date.append(row)
    
    try: 
        Subs['score'] = Subs['Time'].apply(map_score_to_time, scores=Score)
    except AttributeError:
        Subs['score'] = ['0-0']*len(Subs)
    

    Subs['Date'] = [datetime.datetime.strptime(date[0],"%m/%d/%Y")]*len(Subs)
    Subs['Mapped_Time'] = Subs['Time'].apply(time_map)

    final_df = Subs
    return final_df
                             

#def get_roster(base_url):
#    
#    req = urllib.request.Request(base_url, None, headers)
#    r = urllib.request.urlopen(req).read()
#    
#    soup = BeautifulSoup(r,'html5lib')
#    #test = soup.find_all("div",class_ = 'sidearm-responsive-tabs ui-tabs ui-widget ui-widget-content ui-corner-all')
#    test2 = soup.find("div",{'id':'ctl00_contentDiv'})
#    
#    roster_table = test2.find("table", {"class":"default_dgrd roster_dgrd"})
#
##    
#    #return roster_table
#    names = []
#    for row in roster_table.tbody.findAll('tr'):
#        #first_column = row.findAll('th')[0].contents
#        #third_column = row.findAll('td')[1].contents
#        names.extend(row.findAll('td')[0].contents)
#    
#       
#    roster = []
#    for i in names:
#
#        player = str(i).rstrip()
#        player = "".join(player.split())
#        roster.append(player)
#        
#    return roster

#tabs = get_roster('http://www.vassarathletics.com/roster.aspx?path=msoc')
    
#VCMS_Manhattanville = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7810') 
#VCMS_Skidmore = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7816')






#Game_6 = 



##### Everybody has unique coordinates 
#import numpy as np
import matplotlib.pyplot as plt

#from matplotlib.sankey import Sankey

def plotting(data,player_name,in_out):
    player = []
    player_of_interest_x = 1
    
    
    x = 5
    y = 1
    for j in range(len(data)):
        for index, row in data[j].iterrows():
            if (row[in_out]) == player_name:
                if in_out == 'Out':
                    player.append([row['In'],row['Time'],row['score'],x,y])
                else: 
                    player.append([row['Out'],row['Time'],row['score'],x,y])
                #x += 0
                y += 20
    k = y
    y = [] 
    text = []
    for i in player:
        y.append(i[4])
        text.append(i[0] + '    ' + ' Min: ' +  i[1] + '  ' + 'Score: '+ i[2])
    
    fig = plt.figure(figsize=(6,10), dpi=100)

    for i in range(len(y)):
        plt.plot([1, 5], [2,y[i]], 'k--')
#        plt.annotate(text[i], xy=(5, y[i]), xytext=(5, y[i] + 0.25),
#                arrowprops=builtins.dict(facecolor='black', shrink=0.03),
#                )
        plt.annotate(text[i], xy=(1, k/2), xycoords='data', xytext=(5, y[i]+2),
                     textcoords='data',
                     
                #arrowprops=builtins.dict(
                             #            arrowstyle="-|>",linestyle = 'dashed',
                            #connectionstyle="arc3"),horizontalalignment='left',
                        #va = 'bottom'
                )
#        xy=(0.2, 0.2), xycoords='data',
#            xytext=(0.8, 0.8), textcoords='data',
#            arrowprops=dict(arrowstyle="->",
#                            connectionstyle="arc3")
    
    #    plt.annotate('local max', xy=(2, i), xytext=(3, 1.5),
    #            arrowprops=dict(facecolor='black', shrink=0.05),
    #            )
    player_of_interest_y = 2
    plt.annotate(player_name + ' Subs ' + in_out  + ' For', xy=(1, 2), xytext=(0, -20)),
                #)#arrowprops=builtins.dict(facecolor='black', shrink=0.03),

    plt.plot([player_of_interest_x],[player_of_interest_y],'bs')    
    #plt.plot([x]*len(player), y, 'ro')
    #plt.title(player_name + ' Subs ' + in_out  + ' For')
    plt.xlim([0.4,13])
    plt.ylim([-25,k + 3])
    #plt.axis('off')
    plt.axis('off')
    #fig.axes.get_xaxis().set_visible(False)
    #fig.axes.get_yaxis().set_visible(False)
    plt.savefig(player_name + ' Subs ' + in_out  + ' For')  

    return plt.show()


import matplotlib.dates as mdates
def plot_ts(data,player_name,in_out):
    
    player = []
    for j in range(len(data)):
        for index, row in data[j].iterrows():
                if (row[in_out]) == player_name:
                    if in_out == 'Out':
                        player.append([row['In'],row['Mapped_Time'],row['score'],row['Date']])
                    else: 
                        player.append([row['Out'],row['Mapped_Time'],row['score'],row['Date']])
                    #x += 0
                    #y += 20
    time = []
    date = []
    for i in range(len(player)):
        time.append(player[i][1])
        date.append(player[i][3])
    
    ts = pd.Series(time, date)
    
    
    
    #k = y
    #y = [] 
    text = []
    for i in player:
        #y.append(i[4])
        text.append(i[0].split(' ')[0] + '\n' + 'Score:' + '\n'+ i[2])
        
    plt.figure(figsize=(6,8), dpi=100)
    plt.plot(ts,'o')
    
    for i in range(len(text)):
        #plt.plot([1, 5], [2,y[i]], 'k--')
#        plt.annotate(text[i], xy=(5, y[i]), xytext=(5, y[i] + 0.25),
#                arrowprops=builtins.dict(facecolor='black', shrink=0.03),
#                )
        plt.annotate(text[i], xy=(date[i], time[i]), xycoords='data', xytext=(date[i]-datetime.timedelta(days=2), time[i]+2),
                     textcoords='data',size = 7
                     
                #arrowprops=builtins.dict(
                             #            arrowstyle="-|>",linestyle = 'dashed',
                            #connectionstyle="arc3"),horizontalalignment='left',
                        #va = 'bottom'
                )
    
    plt.ylim([-5,110])
    #plt.xlabel(ts.index)
    #plt.xticks(np.arange(min(x), max(x)+1, 1.0))
    #fig = plt.figure(
    
    #ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=range(1,32))) 
    plt.xticks(rotation = 90)
    plt.title(player_name + ' Subs ' + in_out  + ' For')
    plt.ylabel('Minutes')
    plt.xlabel('Dates')
    plt.savefig('Time Series' + player_name + ' Subs ' + in_out  + ' For') 
    
    return plt.show()#,ts

Game_1 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7808')
Game_2 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7809')
Game_3 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7810')
Game_4 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7811')
Game_5 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7812')
Game_6 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7813')
Game_7 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7814')
Game_8 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7815')
Game_9 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7816')
Game_10 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7817')
Game_11 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7818')
Game_12 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7819')
Game_13 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7820')
Game_14 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7821')
Game_15 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7822')
Game_16 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7823')
Game_17 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7824')
Game_18 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7825')
Game_19 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=7826')
Game_20 = final_dataframe('http://www.vassarathletics.com/boxscore.aspx?path=msoc&id=8413')



data = (Game_1,Game_2,Game_3,Game_4,Game_5,Game_6,Game_7,
        Game_8,Game_9,Game_10,
        Game_11,Game_12,Game_13,Game_14,Game_15,Game_16,
        Game_17,Game_18,Game_19,Game_20)


