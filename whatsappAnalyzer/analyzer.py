import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
#sns.set_context("talk")

sns.set_style('white')
import re

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

#Number of Messages and Words-------------------
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
for sender in chat['Sender'].unique():
    wordsList = chatClean[chatClean['Sender']==sender]['Message'].tolist()
    senders[sender] = ' '.join(wordsList).lower().split() #Could use textblob
sendersDF['Words'] = senders.values()

for sender in senders.keys():
    senders[sender] = len(senders[sender])
sendersDF['Number of Words'] = senders.values()
sendersDF['Words per message'] = sendersDF['Number of Words']/sendersDF['Text']

sendersDF['coefSpam']=sendersDF['All Messages']/sendersDF['Words per message']**3
sendersDF['coefSpam']=sendersDF['coefSpam']/sendersDF['coefSpam'].max()

#Add Group stats in plots or comments

#Natural language--------------
#Time of the day---------------
#Day of the week
#Day with more activity


#Plotting
nSenders = sendersDF.shape[0]
fsize = round((1+17*1.04**(-nSenders))/(1+1.04**(-nSenders)))

#Labels
labels = [[name.split()[0] \
            for name in sendersDF.sort_values('All Messages')['Sender']],
        [name.split()[0] \
            for name in sendersDF.sort_values('Text/All')['Sender']],
        [name.split()[0] \
            for name in sendersDF.sort_values('Words per message')['Sender']],
        [name.split()[0] \
            for name in sendersDF.sort_values('Number of Words')['Sender']]]
#Anonymized names
if '-a' in sys.argv:
    labels = [['Friend {:d}'.format(i) for i in np.arange(1,nSenders+1)] \
                for l in range(4)]
#Colors
sendersDF['cLight'] = sns.husl_palette(nSenders)
sendersDF['dark'] = sns.husl_palette(nSenders,l=.5)

#First figure number of Messages
fig1, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2, figsize=(12,9))
p1 = ax1.bar(sendersDF.index,
    sendersDF.sort_values('All Messages')['Text'],
    color=sendersDF.sort_values('All Messages')['cLight'])
p2 = ax1.bar(sendersDF.index,
    sendersDF.sort_values('All Messages')['Media'],
    bottom=sendersDF.sort_values('All Messages')['Text'],
    color=sendersDF.sort_values('All Messages')['dark'])
l1 = ax1.axhline(sendersDF['All Messages'].mean(),ls='--',lw=.7,color='gray')
ax1.set_xticks(sendersDF.index)

ax1.set_xticklabels(labels[0], fontsize=fsize)

p3 = ax2.barh(sendersDF.index,
    sendersDF.sort_values('Text/All')['Text/All'],
    color=sendersDF.sort_values('Text/All')['cLight'])
p4 = ax2.barh(sendersDF.index,
    1 - sendersDF.sort_values('Text/All')['Text/All'],
    left=sendersDF.sort_values('Text/All')['Text/All'],
    color=sendersDF.sort_values('Text/All')['dark'])
l2 = ax2.axvline(sendersDF['Text/All'].mean(),ls='--',lw=.7,color='gray')
ax2.set_yticks(sendersDF.index)
ax2.set_yticklabels(labels[1], fontsize=fsize*1.05)

ax2.set_xticks(np.arange(0,1.2,0.2))
percentLabel = ['{:.0f}%'.format(p*100) for p in np.arange(0,1.2,0.2)]
ax2.set_xticklabels(percentLabel)

p5 = ax3.bar(sendersDF.index,
    sendersDF.sort_values('Words per message')['Words per message'],
    color=sendersDF.sort_values('Words per message')['cLight'])
l3 = ax3.axhline(sendersDF['Words per message'].mean(),ls='--',lw=.7,color='gray')
ax3.set_xticks(sendersDF.index)
ax3.set_xticklabels(labels[2],fontsize=fsize)



p6 = ax4.bar(sendersDF.index,
    sendersDF.sort_values('Number of Words')['Number of Words'],
    color=sendersDF.sort_values('Number of Words')['cLight'])
l4 = ax4.axhline(sendersDF['Number of Words'].mean(),ls='--',lw=.7,color='gray')
ax4.set_xticks(sendersDF.index)
ax4.set_xticklabels(labels[3],fontsize=fsize)



#Text for fig1
plt.gcf().text(0.1, 0.94, "This group has {} participants, who sent {} text messages"
    "\nand {} images and videos. Altogether they wrote {} words.".format(
    sendersDF.shape[0],sendersDF['Text'].sum(),sendersDF['Media'].sum(),
    sendersDF['Number of Words'].sum(), fontsize=10, ha="center"))
ax1.legend((p1[-1],p2[-1],l1),('Text','Media', 'Mean'))
ax1.set_ylabel('Number of Messages')
ax2.set_title('Proportion Media/Text Messages')
ax3.set_ylabel('Words per Message')
ax4.set_ylabel('Number of Words')
#Second figure
#fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)


sns.despine()
#plt.savefig(path[:-3]+'png')
plt.show()
