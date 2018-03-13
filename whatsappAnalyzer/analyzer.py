import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import re

if len(sys.argv) < 2:
    path = os.path.join(input ('Provide a file path: '))
else:
    path = os.path.join(sys.argv[1])

if not os.path.exists(path):
    print('File not found')
    sys.exit()
chatFile = open(path,'r',encoding='UTF-8')
if chatFile.read(1) != '[': #Android
    regex = re.compile(r'(\d+/\d+/\d+,\s\d+:\d+)\s-\s([^:]*):\s(.*)')
    chatFile.seek(0)
else: #IOS
    regex = re.compile(r'(\[\d+/\d+/\d+\s\d+:\d+:\d+)\]\s([^:]*):\s(.*)')
results = regex.findall(chatFile.read())
chatFile.close()
chat = pd.DataFrame(results, columns=['Datetime','Sender','Message'])
#Clean data
chatClean = chat.copy()
chatClean['Message'] = chatClean['Message'].replace(regex=True,
    to_replace=r'<.\w+\s\w+>', value = r'') #Replace omitted files
punctuation = ['¿','?','!','.','¡','(',')','"']
chatClean['Message'] = chatClean['Message'].replace(to_replace=punctuation,
    value = '') #Replace punctuation
#Analysis
fig1 = plt.figure()
#Senders
#Number of Messages
senders = {}
for sender in chat['Sender'].unique():
    senders[sender] = chat[chat['Sender']==sender]['Sender'].count()
sendersDF = pd.DataFrame(list(senders.items()),columns=['Sender','Messages'])
fig1.add_subplot(2,2,1)
ax1 = sns.barplot(x='Sender',y='Messages',
    data=sendersDF.sort_values('Messages'))
ax1.set_xticklabels(ax1.get_xticklabels(), fontsize=7)
#Words by sender
senders = {}
for sender in chatClean['Sender'].unique():
    wordsList = chatClean[chatClean['Sender']==sender]['Message'].tolist()
    senders[sender] = ' '.join(wordsList).lower().split()
sendersDF['Words'] = senders.values()
#wordsBySender = pd.DataFrame(list(senders.items()),columns=['Sender','Words'])
for sender in senders.keys():
    senders[sender] = len(senders[sender])
sendersDF['Number of Words'] = senders.values()
sendersDF['Words per message'] = sendersDF['Number of Words']/sendersDF['Messages']
fig1.add_subplot(2,2,2)
ax2 = sns.barplot(x='Sender',y='Number of Words',
    data=sendersDF.sort_values('Number of Words'))
ax2.set_xticklabels(ax2.get_xticklabels(), fontsize=7)

fig1.add_subplot(2,2,3)
ax3 = sns.barplot(x='Sender',y='Words per message',
    data=sendersDF.sort_values('Words per message'))
ax3.set_xticklabels(ax3.get_xticklabels(), fontsize=7)

plt.show()
