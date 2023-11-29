import re
import pandas as pd


def preprocess(data):
    # pattern in chat (splitting DateTime & Messages
    pattern = '\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{1,2}\s\w+\s-\s'

    # All messages we have
    messages = re.split(pattern, data)[1:]  # Extract messages (start from index 1)

    # Get dates using regex
    dates = re.findall(pattern, data)

    # Split date and time
    date = [i.split(", ")[0] for i in dates]
    time = [i.split(", ")[1].replace('\u202f', '') for i in dates]

    # Create the DataFrame
    df = pd.DataFrame({
        'user_msg': messages,
        'date': date,
        'time': time
    })

    # Separate user name and message
    user = []
    msg = []
    for i in df['user_msg']:
        x = re.split('([\w\W]+?):\s', i)
        if len(x) >= 3:  # User name and message are present
            user.append(x[1])
            msg.append(x[2])
        else:  # Group notification or unrecognized message format
            user.append('Group Notification')
            msg.append(x[0])

    df['user'] = user
    df['msg'] = msg
    df.drop(columns=['user_msg'], inplace=True)

    # Convert the date into DateTime format

    df['date'] = pd.to_datetime(df['date'])
    # for date extract
    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    # for month num
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    # for day names
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    #for generating heatmap period
    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))
    df['period'] = period

    return df


#f = open('WhatsApp Chat with महात्मा फुले प्रतिष्ठान.txt', 'r', encoding='utf=8')
#data = f.read()
#output = preprocess(data)
#print(output)