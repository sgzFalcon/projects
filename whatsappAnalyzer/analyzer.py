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
    chatFile.seek(1)
results = regex.findall(chatFile.read())
chatFile.close()
chatFrame = pd.DataFrame(results, columns=['Datetime','Sender','Message'])

#Analysis
#Senders
senders = {}
for sender in chatFrame['Sender'].unique():
    senders[sender] = chatFrame[chatFrame['Sender']==sender]['Sender'].count()
sendersFrame = pd.DataFrame(list(senders.items()),columns=['Sender','Messages']) \
                .sort_values('Messages')
ax = sns.barplot(x='Sender',y='Messages',data=sendersFrame.iloc[:-20])
ax.set_xticklabels(ax.get_xticklabels(), fontsize=7)
plt.show()
