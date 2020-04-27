import pandas as pd
from itertools import chain, repeat
import re

chainer = chain.from_iterable
class Cleaner:
  def __init__(self,filename):
    self.filename = filename

  def _clean_data(self):
    chat_file = self.filename
    with open(chat_file) as file:
      all_msgs = file.readlines()
      clean_msgs = []
      for line in all_msgs:
        if re.match("^\d{2}/\d{2}/\d{2},\s\d{1,2}:\d{2}\s[ap]m",line):
          date_split = line.split(' - ')
          user_split = date_split[1].split(':')
          if len(user_split) >= 2:
            clean_msgs.append(line)
        else:
          clean_msgs[-1] += line

    return clean_msgs 
      
  def _get_data(self):
    cleaned_msgs = self._clean_data()
    user_msgs = dict()
    for line in cleaned_msgs:
      date_split = line.split(' - ')
      user_split = date_split[1].split(':')
      if user_split[0] not in user_msgs:
        user_msgs[user_split[0]] = []
        user_msgs[user_split[0]].append(line)
      else:
        user_msgs[user_split[0]].append(line)

    df = pd.DataFrame({'User': list(chainer(repeat(k, len(v)) for k,v in user_msgs.items())),
                   'Message': list(chainer(user_msgs.values()))}) 
    return df

