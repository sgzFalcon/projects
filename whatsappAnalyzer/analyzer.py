import sys
import os
import pandas as pd
import numpy as np
import nltk
from textblob import TextBlob
import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style('white')
import re
import emoji

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
chatClean['Message'] = chatClean['Message'].replace(regex=True,
    to_replace=r"https*\S+", value = '')
chatClean.dropna(inplace=True)
    #Replace and drop omitted files

#Analysis

#Number of Messages and Words-------------------
senders = {}
for sender in chat['Sender'].unique():
    senders[sender] = chat[chat['Sender']==sender]['Sender'].count()
sendersDF = pd.DataFrame(list(senders.items()),columns=['Sender','All Messages'])

nSenders = sendersDF.shape[0]
#Anonymized names
if ('-a' in sys.argv) and nSenders > 11:
    sendersDF['Anon'] = ['F{:d}'.format(i) \
        for i in np.arange(1,nSenders+1)]
elif ('-a' in sys.argv):
    sendersDF['Anon'] = ['Friend {:d}'.format(i) \
        for i in np.arange(1,nSenders+1)]

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

#Natural language--------------
allWords = TextBlob(' '.join(chatClean['Message']))
lang = allWords[:10].detect_language()
print('Language detected ', lang.upper())
stopwordsDic = {'en': nltk.corpus.stopwords.words('english'),
        'es': nltk.corpus.stopwords.words('spanish')}
stopwords = stopwordsDic[lang]
moreStop = ['si','ver','q','pues']
stopwords.extend(moreStop)
listEmojis = list(emoji.UNICODE_EMOJI.keys())
moreEmojis = ['🤷🏻‍♂','😂😂😂']
listEmojis.extend(moreEmojis)
filtWords = TextBlob(' '.join(word for word in allWords.words.lower() \
        if (word not in stopwords) and (word not in listEmojis)))
#data = re.findall(r'\X',' '.join(chatClean['Message']))
filtEmojis = TextBlob(' '.join(word for word in allWords.words \
        if word in listEmojis))
dfW = pd.DataFrame(list(filtWords.word_counts.items()),
        columns=['word','word freq'])
dfE = pd.DataFrame(list(filtEmojis.word_counts.items()),
        columns=['emoji','emoji freq'])
wordsDF = pd.concat([dfW,dfE],axis=1)
#Time of the day---------------
#Day of the week
#Day with more activity

#Plotting
fsize = round((1+17*1.04**(-nSenders))/(1+1.04**(-nSenders)))

#Labels
if '-a' in sys.argv:
    labels = [[name \
                for name in sendersDF.sort_values('All Messages')['Anon']],
            [name \
                for name in sendersDF.sort_values('Text/All')['Anon']],
            [name \
                for name in sendersDF.sort_values('Words per message')['Anon']],
            [name \
                for name in sendersDF.sort_values('Number of Words')['Anon']]]
else:
    labels = [[name.split()[0] \
                for name in sendersDF.sort_values('All Messages')['Sender']],
            [name.split()[0] \
                for name in sendersDF.sort_values('Text/All')['Sender']],
            [name.split()[0] \
                for name in sendersDF.sort_values('Words per message')['Sender']],
            [name.split()[0] \
                for name in sendersDF.sort_values('Number of Words')['Sender']]]
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
#Proportion
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
#words per message
p5 = ax3.bar(sendersDF.index,
    sendersDF.sort_values('Words per message')['Words per message'],
    color=sendersDF.sort_values('Words per message')['cLight'])
l3 = ax3.axhline(sendersDF['Words per message'].mean(),ls='--',lw=.7,color='gray')
ax3.set_xticks(sendersDF.index)
ax3.set_xticklabels(labels[2],fontsize=fsize)


#number of words
p6 = ax4.bar(sendersDF.index,
    sendersDF.sort_values('Number of Words')['Number of Words'],
    color=sendersDF.sort_values('Number of Words')['cLight'])
l4 = ax4.axhline(sendersDF['Number of Words'].mean(),ls='--',lw=.7,color='gray')
ax4.set_xticks(sendersDF.index)
ax4.set_xticklabels(labels[3],fontsize=fsize)



#Text for fig1
plt.gcf().text(0.1, 0.93, "This group has {} participants, who sent {} text messages"
    "\nand {} images and videos. Altogether they wrote {} words.".format(
    sendersDF.shape[0],sendersDF['Text'].sum(),sendersDF['Media'].sum(),
    sendersDF['Number of Words'].sum(), fontsize=3, ha="center"))
ax1.legend((p1[-1],p2[-1],l1),('Text','Media', 'Mean'))
ax1.set_ylabel('Number of Messages')
ax2.set_title('Proportion Media/Text Messages', fontsize=12)
ax3.set_ylabel('Words per Message')
ax4.set_ylabel('Number of Words')
sns.despine()
#Second figure
fig2, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2, figsize=(12,9))

#ten most used words
ax1.bar(range(8),wordsDF.sort_values('word freq',
        ascending=False)['word freq'][:8],
        color=sns.color_palette('BuGn_r',8))
ax1.set_xticks(range(8))
wordLabel = [label.capitalize() for label in wordsDF.sort_values('word freq',
        ascending=False)['word'][:8]]
ax1.set_xticklabels(wordLabel,fontname='Segoe UI Emoji', fontsize=8)

ax2.bar(range(8),wordsDF.sort_values('emoji freq',
        ascending=False)['emoji freq'][:8],
        color=sns.color_palette('BuGn_r',8))
ax2.set_xticks(range(8))
emojiLabel = [label for label in wordsDF.sort_values('emoji freq',
        ascending=False)['emoji'][:8]]

ax2.set_xticklabels(emojiLabel,fontname='Segoe UI Emoji', fontsize=13)

ax3.axis('off')
ax4.axis('off')
#Test for fig2
plt.gcf().text(0.1, 0.90, "This group uses {} different words"
    " (excluded stopwords) and {} unique emojis. Altogether {}"
    " emojis where sent.".format(
    len(wordsDF['word']),len(wordsDF['emoji'].dropna()),
    int(wordsDF['emoji freq'].sum()),
    fontsize=16, ha="center"))
sns.despine()
if '-s' in sys.argv:
    plt.savefig(path[:-3]+'png')
plt.show()
