## Aim is to convert WhatsAppChatExport.txt into JSON

message in chat looks like - 
> 25/10/2019, 3:38 pm - name_of_user: This the message sent by user
#### Typical JSON Object for above message looks like
```
  "1": {
    "datetime": "25/10/2019, 3:38 pm",
    "user": "name_of_user",
    "message": "This the message sent by user"
  },
```
We have two types of chats - 
  1. Personal Chat
  2. Group Chat            
But we are gonna parse both chats in a generalised way.

We do have 3 types of messages - 
  1. Messages         
    - Message sent by the user.           
    - This message was deleted.            
  2. Actions         
    - Someone created this group.       
    - Someone updated profile picture.         
    - Someone changed their phone number from x to y.         
    - Someone left from the group.         
    - Someone removed x person from the group.         
    - Someone deleted Profile picture          
    - Someone changed group description.           
    - Messages in this chat are end-to-end encrypted (once in a chat).        
  3. Media         
    - Usually we don't get the type of media user has sent. But here are some types of media we may get -      
        - Images         
        - GIFs         
        - Videos       
        - Stickers       
        - Documents      

JSON should have these fields according to type of message. Here are the formats for all 3 types of messages - 
  1. Nomral message -           
      ```
      "1": {
        "datetime": "25/10/2019, 3:38 pm",
        "isMessage" : true,
        "user": "name_of_user",
        "message": "This the message sent by user"
      },
      ```
  2. Action -          
      ```
      "2": {
        "datetime": "11/05/2019, 2:40 pm",
        "isAction": true,
        "action": "Stephen created group GROUP_NAME"
      }
      ```
  3. Media -
      ```
      "3": {
        "datetime": "25/10/2019, 3:30 pm",
        "user": "+91 81432 75536",
        "isMedia": true
      }
      ```
