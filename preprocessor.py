import re
import pandas as pd
def preprocess(data):#returns dataframe
    pattern='\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'
    messages=re.split(pattern,data)[1:]
    dates=re.findall(pattern,data)
    df=pd.DataFrame({'user_message':messages,'date':dates})
    #convert message_data type
    df['date']=pd.to_datetime(df['date'],format='%d/%m/%Y, %H:%M - ')

    users=[]
    messages=[]
    for message in df['user_message']:
        entry=re.split('([\w\W]+?):\s',message)
        if entry[1:]: #user name
            #print(entry[1])
            #print(entry[2])
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            #print(entry[0])
            messages.append(entry[0])
    df['user']=users
    df['message']=messages
    df.drop(columns=['user_message'],inplace=True)

    df['month']=df['date'].dt.month_name()
    df['month_num']=df['date'].dt.month
    df['day']=df['date'].dt.day
    df['day_name']=df['date'].dt.day_name()
    df['year']=df['date'].dt.year
    df['hour']=df['date'].dt.hour
    df['minutes']=df['date'].dt.minute

    period=[]
    for hour in df['hour']:
        if hour==23:
            period.append(str(hour)+"-"+ str('00'))
        else:
            period.append(str(hour)+"-"+str(hour+1))

    df['period']=period
    return df




    