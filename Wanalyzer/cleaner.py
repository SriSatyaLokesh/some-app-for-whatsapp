import pandas as pd
from itertools import chain, repeat
from string import digits
import re

chainer = chain.from_iterable
class Cleaner:
  def __init__(self,filename):
    self.filename = filename

  def _clean_data(self):
    """ 
    What it does?
    ----------------
      remove action messages and append new line without date format to previous message
      
      EXAMPLE : 

      17/07/19, 8:33 pm - +91 90633 88499: Sir,
      *We have a chance to write Cocubes exam later...?*

      CHANGED TO:

      17/07/19, 8:33 pm - +91 90633 88499: Sir, *We have a chance to write Cocubes exam later...?*
      
      Parameters:
      -----------
      df : dataframe
          
      Returns:
      --------
      raw_texts : list
                  list consists of all raw messages ignoring actions from the chat file
      
    """
    chat_file = self.filename
    with open(chat_file) as file:
      all_msgs = file.readlines()
      raw_texts = []
      for line in all_msgs:
        if re.match("^\d{2}/\d{2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap][m]",line):
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
    """ 
    What it does?
    ----------------
      Import whatsapp data and transform it to a dataframe
      
      Parameters:
      -----------
      -
          
      Returns:
      --------
      df : dataframe
          Dataframe of all messages with columns - ["raw_message","users"]
      
    """
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

  def _get_message(self,df):
    """ 
    What it does?
    ----------------
      new column is added to existing dataframe i.e clean_message which ignores datetime and user from the raw_message
      
      Parameters:
      -----------
      df : dataframe
          
      Returns:
      --------
      df : dataframe
          Dataframe of all messages with columns - ["users","raw_message","clean_message",]
      
    """
    df["clean_message"] = df.apply(lambda df : "".join(df['raw_message'].split(":")[2:]),axis=1)
    return df

  def _get_text_only_message(self,df):
    """ 
    What it does?
    ----------------
      new column is added to existing dataframe i.e text_only_message which ignores all emojis and numbers from the clean_message
      
      Parameters:
      -----------
      df : dataframe
          
      Returns:
      --------
      df : dataframe
          Dataframe of all messages with columns - ["users","raw_message","clean_message",text_only_message]
      
    """
    remove_digits = str.maketrans('', '', digits)
    df["text_only_message"] = df.apply(lambda df : df["clean_message"].encode('ascii', 'ignore').decode('ascii'),axis=1)     # removing emoji s from cleam_message
    df["text_only_message"] = df.apply(lambda df : df["text_only_message"].translate(remove_digits),axis=1)          # removing digits from clean_message

    df.loc[(df['text_only_message'] == " This message was deleted\n") | (df['text_only_message'] == " \n"),'text_only_message'] = "" # updating "This message was deleted\n" and  "\n" to ""(empty_string)

    return df

  def _remove_inactive_users(self,df):
    """ 
    What it does?
    ----------------
      removes inactive users i.e user with no of messages < 10 from dataframe
      
      Parameters:
      -----------
      df : dataframe
          
      Returns:
      --------
      df : dataframe
          Dataframe of all messages with columns - ["users","raw_message","clean_message",text_only_message]
          removing inactive users
      
    """
    df = df.groupby('user').filter(lambda x : len(x) > 10)
    return df

  def _get_user_media_counts(self,df):
    """ 
    What it does?
    ----------------
      it counts individual user media that is sent in the chat
      
      Parameters:
      -----------
      df : dataframe
          
      Returns:
      --------
      user_media_counts : dictionary
                          key as 'user' : value as 'media_count'
      
    """
    media_count = df[df['text_only_message'] == " <Media omitted>\n"].groupby('user').size()
    user_media_counts = media_count.to_dict()
    return user_media_counts
