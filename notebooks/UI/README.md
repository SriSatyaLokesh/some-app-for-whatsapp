## Aim is to convert WhatsAppChatExport.txt into JSON

#### Typical JSON Objects looks like
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
    - Images         
    - GIFs         
    - Videos       
    - Stickers           
