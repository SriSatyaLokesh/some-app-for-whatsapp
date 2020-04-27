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
      raw_texts = []
      for line in all_msgs:
        if re.match("^\d{2}/\d{2}/\d{4},\s\d{1,2}:\d{2}\s[ap]m",line): #need to improve this RegEx
          date_split = line.split(' - ') #date and user
          user_split = date_split[1].split(':')
          if len(user_split) >= 2:
            raw_texts.append(line)
        else:
          try:
            raw_texts[-1] += line
          except Exception as err:
            print(line,raw_texts)
            print(err)

    return raw_texts 
      
  def _get_data(self):
    raw_texts = self._clean_data()
    raw_messages = dict()
    for line in raw_texts:
      date_split = line.split(' - ')
      user_split = date_split[1].split(':')
      user = user_split[0]
      if user not in raw_messages:
        raw_messages[user] = [line]
      else:
        raw_messages[user].append(line)

    df = pd.DataFrame({'user': list(chainer(repeat(k, len(v)) for k,v in raw_messages.items())),
                   'raw_message': list(chainer(raw_messages.values()))}) 
    return df
