import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_context("talk")
sns.set_style('white')
import re
plt.rcParams['figure.figsize'] = (18,9)

if len(sys.argv) < 2:
    path = os.path.join(input ('Provide a file path: '))
else:
    path = os.path.join(sys.argv[1])

if not os.path.exists(path):
    print('File not found')
    sys.exit()
chatFile = open(path,'r',encoding='UTF-8')

#Parse data
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
    to_replace=r'<.\w+\s\w+>', value = np.nan)
chatClean.dropna(inplace=True)
    #Replace and drop omitted files

#Analysis

#Number of Messages-------------------
#Individual stats
senders = {}
for sender in chat['Sender'].unique():
    senders[sender] = chat[chat['Sender']==sender]['Sender'].count()
sendersDF = pd.DataFrame(list(senders.items()),columns=['Sender','All Messages'])

senders = {}
for sender in chat['Sender'].unique():
    senders[sender] = chatClean[chatClean['Sender']==sender]['Sender'].count()
sendersDF['Text'] = senders.values()
sendersDF['Media'] = sendersDF['All Messages']-sendersDF['Text']
sendersDF['Text/All'] = sendersDF['Text']/sendersDF['All Messages']

#Words by sender
senders = {}
for sender in chatClean['Sender'].unique():
    wordsList = chatClean[chatClean['Sender']==sender]['Message'].tolist()
    senders[sender] = ' '.join(wordsList).lower().split() #Could use textblob
sendersDF['Words'] = senders.values()

for sender in senders.keys():
    senders[sender] = len(senders[sender])
sendersDF['Number of Words'] = senders.values()
sendersDF['Words per message'] = sendersDF['Number of Words']/sendersDF['Text']

#Group stats


#Time of the day---------------
#Day of the week
#Day with more activity


#Plotting
nSenders = sendersDF.shape[0]
ncols = 1
if nSenders >= 8:
    ncols = 2
fig1, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)
sendersDF['cLight'] = sns.husl_palette(nSenders)
sendersDF['dark'] = sns.husl_palette(nSenders,l=.5)

p1 = ax1.bar(sendersDF.index,
    sendersDF.sort_values('All Messages')['Text'],
    color=sendersDF.sort_values('All Messages')['cLight'])
p2 = ax1.bar(sendersDF.index,
    sendersDF.sort_values('All Messages')['Media'],
    bottom=sendersDF.sort_values('All Messages')['Text'],
    color=sendersDF.sort_values('All Messages')['dark'])
ax1.set_xticks(sendersDF.index)
labels = [name.split()[0] \
    for name in sendersDF.sort_values('All Messages')['Sender']]
ax1.set_xticklabels(labels, fontsize=85/nSenders)
ax1.legend((p1[-1],p2[-1]),('Text','Media'))
ax4.legend(p1[:],sendersDF.sort_values('All Messages')['Sender'],
    ncol=ncols) #Need to improve placement, drop one plot
ax1.set_ylabel('Number of Messages')

p3 = ax2.barh(sendersDF.index,
    sendersDF.sort_values('Text/All')['Text/All'],
    color=sendersDF.sort_values('Text/All')['cLight'])
p4 = ax2.barh(sendersDF.index,
    1 - sendersDF.sort_values('Text/All')['Text/All'],
    left=sendersDF.sort_values('Text/All')['Text/All'],
    color=sendersDF.sort_values('Text/All')['dark'])
ax2.set_yticks(sendersDF.index)
labels = [name.split()[0] \
    for name in sendersDF.sort_values('Text/All')['Sender']]
ax2.set_yticklabels(labels)

ax2.set_xticks(np.arange(0,1.2,0.2))
labels = ['{:.0f}%'.format(p*100) for p in np.arange(0,1.2,0.2)]
ax2.set_xticklabels(labels)

ax2.set_title('Proportion Media/Text Messages')

p5 = ax3.bar(sendersDF.index,
    sendersDF.sort_values('Words per message')['Words per message'],
    color=sendersDF.sort_values('Words per message')['cLight'])
ax3.set_xticks(sendersDF.index)
labels = [name.split()[0] \
    for name in sendersDF.sort_values('Words per message')['Sender']]
ax3.set_xticklabels(labels,fontsize=85/nSenders)

ax3.set_ylabel('Words per Message')

p6 = ax4.bar(sendersDF.index,
    sendersDF.sort_values('Number of Words')['Number of Words'],
    color=sendersDF.sort_values('Number of Words')['cLight'])
ax4.set_xticks(sendersDF.index)
labels = [name.split()[0] \
    for name in sendersDF.sort_values('Number of Words')['Sender']]
ax4.set_xticklabels(labels,fontsize=85/nSenders)

ax4.set_ylabel('Number of Words')

sns.despine()

plt.show()
