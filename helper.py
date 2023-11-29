
from urlextract import URLExtract
from wordcloud import WordCloud

import pandas as pd
from collections import Counter

import emoji


extract = URLExtract()

def fetch_stats(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]

    # Fetch total number of messages
    num_messages = df.shape[0]

    # Fetch total number of words
    words = []
    for message in df['msg']:
        words.extend(message.split(' '))

    # Fetch total number of media messages
    num_media_messages = df[df['msg'] == '<Media omitted>\n'].shape[0]

    # Fetch number of links shared with urlextract lib
    links = []
    for message in df['msg']:
        links.extend(extract.find_urls(message))

    return num_messages, len(words), num_media_messages, len(links)




def most_busy_user(df) :
    x = df['user'].value_counts().head()

    #for total user messages and repected percentage of each and perform rename
    df = round((df['user'].value_counts() / df.shape[0]) * 100, 2 ).reset_index().rename( columns ={'index' : 'name', 'user': 'percent'})

    return x, df


def create_wordcloud(selected_user, df):

    f = open("stop_hinglish.txt", 'r')
    stop_word = f.read()


    if selected_user != "Overall":
        df = df[df['user'] == selected_user]

    temp = df[df['user'] != 'group_notifiction']
    temp = temp[temp['msg'] != '<Media omitted>\n']

    def remove_stop_words(message) :
        y  =[]
        for word in message.lower().split() :
            if word not in stop_word :
                y.append(word)

        return " ". join(y)

    wc = WordCloud(width=500, height=500,min_font_size=14,background_color='gray')
    temp['msg'] = temp['msg'].apply(remove_stop_words)
    df_wc = wc.generate(temp['msg'].str.cat(sep= " "))
    return df_wc


#Most common word in chat

def most_common_words(selected_user,df) :
    f =open("stop_hinglish.txt", 'r')
    stop_word =f.read()

    if selected_user != "Overall" :
        df = df[df['user']  == selected_user]
    temp = df[df['user'] != 'group_notifiction']
    temp = temp[temp['msg'] != '<Media omitted>\n']

    words = []

    for message in temp['msg'] :
        for word in message.lower().split() :
            if word not in stop_word :
                words.append(word)
    most_common_df = pd.DataFrame(Counter(words).most_common(20))
    return most_common_df


#function for emojies

def emoji_helper(selected_user,df) :

    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    emojis = []
    for message in df['msg'] :
        emojis.extend([c for c in message if c in emoji.UNICODE_EMOJI['en']])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))

    return emoji_df


#TimeLine Proceess function Monthly timeline

def monthly_timeline(selected_user, df) :
    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    timeline = df.groupby(['year', 'month_num', 'month']).count()['msg'].reset_index()

    time = []

    for i in range (timeline.shape[0]) :
        time.append(timeline['month'][i] + "-" + str(timeline['year'][i]))
    timeline['time'] = time
    return timeline

#daily time Line

def daily_timeline(selected_user, df) :
    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]

    daily_timeline = df.groupby('only_date').count()['msg'].reset_index()

    return daily_timeline

#Weekly Timeline 

def week_activity_map(selected_user, df) :
    if selected_user != 'Overall' :
        df = df[df['user'] == selected_user]
    
    return df['day_name'].value_counts()

#Monthly  Timeline

def monthly_activity_map(selected_user, df):
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
        
    return df['month'].value_counts()    


#HeatMap Code

def activity_heatmap(selected_user, df) :
    if selected_user != 'Overall':
        df = df[df['user'] == selected_user]
    #write code for pivote table
    user_heatmap = df.pivot_table(index='day_name', columns='period',values='msg',aggfunc='count').fillna(0)

    return user_heatmap




'''
 above is altername code for this long code
   if selected_user == "Overall" :
        #1. fetch number of messages
        num_messages = df.shape[0]
        #2. ftech number of total words
        words = []
        for message in df['message'] :
            words.extend(message.split())

        return num_messages, len(words)
    else:
        new_df = df[df['user'] == selected_user]
        num_messages = new_df.shape[0]
        words = []
        for message in new_df['message']:
            words.extend(message.split())

        return num_messages, len(words)
        
'''

'''
to count the reaptation of words not including stop words 
#remove group notification messages
temp = df[df['user'] !== "group_notifiction"
#remove media omitted messages
temp = temp[temp['msg] != '<media omitted>\n']
#remove stop words
f = open("stop_hinglish.txt",'r')
stop_word = f.read()
print(stop_word)

words = []
for message in temp['msg'] :
    for word in message.lower().split() :
        if word not in stop_word :
            words.append(word)
    
from Collection import Counter
Counter(words).most_common(20)      #with the help of this instruction we get top 20 reapetated words with its count including stop words


    
'''



