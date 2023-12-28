from urlextract import URLExtract
extractor=URLExtract()
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from collections import Counter
import pandas as pd
import emoji
import seaborn as sns
def fetch_stats(selected_user,df):
    num_media=df[df['message']=='<Media omitted>\n']
    if selected_user=='Overall':
        num_messages= df.shape[0]
        words=[]
        for message in df['message']:
            words.extend(message.split())
        links=[]
        for message in df['message']:
            links.extend(extractor.find_urls(message))
        return num_messages,len(words),len(num_media),len(links)
        
    else:
        new_df=df[df['user']==selected_user]
        num_messages=new_df.shape[0]
        words=[]
        for message in new_df['message']:
            words.extend(message.split())
        links=[]
        for message in new_df['message']:
            links.extend(extractor.find_urls(message))
        return num_messages,len(words),len(num_media),len(links)
def most_busy_users(df):
    x=df['user'].value_counts()
    df=round((df['user'].value_counts()/df.shape[0])*100,2).reset_index().rename(columns={'index':'name','user':'percent'})
    name=x.index
    count=x.values
    return x,df
 
def create_wordcloud(selected_user,df):

    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    wc=WordCloud(width=500,height=500,min_font_size=10,background_color='white')
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    temp['message']=temp['message'].apply(remove_stop_words)
    df_wc=wc.generate(temp['message'].str.cat(sep=""))
    return df_wc

def most_used_words(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    temp=df[df['user']!='group_notification']
    temp=temp[temp['message']!='<Media omitted>\n']
    f=open('stop_hinglish.txt','r')
    stop_words=f.read()
    
    words=[]
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)
    x=pd.DataFrame(Counter(words).most_common(20))
    return x

def emoji_helper(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    emojis=[]
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])
    x=pd.DataFrame(Counter(emojis).most_common(len(Counter(emojis))))
    return x

def monthly_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['month_num']=df['date'].dt.month
    timeline=df.groupby(['year','month_num','month']).count()['message'].reset_index()
    time=[]
    for i in range(timeline.shape[0]):
        time.append(timeline['month'][i]+"-"+str(timeline['year'][i]))
    timeline['time']=time
    return timeline

def daily_timeline(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    df['only_date']=df['date'].dt.date
    daily_timeline=df.groupby('only_date').count()['message'].reset_index()
    plt.figure(figsize=(18,10))
    plt.plot(daily_timeline['only_date'],daily_timeline['message'])
    return daily_timeline

def week_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def month_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]

    return df['month'].value_counts()

def day_activity_map(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    return df['day_name'].value_counts()

def activity_heat_maap(selected_user,df):
    if selected_user!='Overall':
        df=df[df['user']==selected_user]
    x=df.pivot_table(index='day_name',columns='period',values='message',aggfunc='count').fillna(0)
    return x






