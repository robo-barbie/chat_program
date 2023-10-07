##-----------------------------------------------------
## INFO 

# Welcome to simple chat simulator. This one is meant to emulate a Slack interface, 
# but can be used for Discord or other things with some tiny changes. 
# All setup code can be found in "chat_program.rpy"

# New messages appear on the screen "chat_messages_view". 

# To add a new message, use the function "chat_message(s, c, ot)""
# s = the string of the message, including the sender + a colon and space. 
# c = the channel (or dm) that you'd like the message to be sent in. 
# ot = the other people who may also be typing when this message is being typed. 

# To add a player choice, provide a list of tuples to "player_choice()", 
# where the first element of each tuple is what the player can select and 
# the second element of each tuple is the label it will jump to after the choice. 

# Some problems with this: 
# 1. I think the position of the scrollbar carries over from channel to channel as it is. 
#     Not a huge deal, but could be annoying to players. I don't remember what my workarounds
#     for that have been in the past lol. Scrolling might be weird in general. I remember it 
#     being a headache in my other projects (hence my tendency to use play/pause buttons to 
#     just stop the scrolling when players wanted)
# 2. A lot of it is manually sized in the screen because I am lazy, but should be easy to make a lot better
# 3. You do have to manually set who is typing. My other chat projects were made via spreadsheets 
#     that could look ahead to see what dialogue was next (and thus construct "who is typing"), but 
#     I couldn't find a way to do that same thing in just normal renpy. If someone knows how, I would 
#     love that info tho cuz manually setting who is typing is really tedious. You can also ignore
#     that feature entirely and just show the current speaker as typing, which works for some cases. 
# 4. I'm sure there's a lot of others. I barely tested this. LOL 

# I offer no real support on this. If you catch me you catch me. Good luck soldier 




##-----------------------------------------------------
## DEMO 

label start:

    $ reset_chats() 

label choose_name: 
    $ player_fname = renpy.input("First name?")
    if player_fname in character_names.keys(): 
        "... not that one."
        jump choose_name
    $ player_lname = renpy.input("Last name?")
    $ character_names[player_fname] = player_lname 
    window hide 

label cont: 
    ## show chat screen + disable rollback when in chat view 
    $ _rollback = False 
    window hide 
    show screen chat_messages_view 

    ## in team chat 
    $ chat_message("Jerri: LOOOOSSSEERRR LOSER LOSER LOSER", ot="Felix") 
    $ chat_message("Jerri: KEEP TYPING LOOOOOOOOOSER", ot="Felix") 
    $ chat_message("Felix: Holy fucking shit")
    $ player_choice([
        ("Huh? What?", "cont_1"), 
        ("Can you both calm down", "cont_2")
    ])

label cont_1: 
    $ chat_message("Felix: You're telling me")
    jump cont_3 

label cont_2: 
    $ chat_message("Jerri: NO!!!!") 
    jump cont_3

label cont_3: 
    ## in felix chat 
    $ chat_message("Felix: Can you believe this bullshit", c="Felix")

    ## in jerri chat (new chat!)
    $ chat_message("Jerri: Tell that asshole he can eat fucking dirt", c="Jerri")
    pause 2 
    $ chat_message("Jerri: Actually", c="Jerri")
    $ chat_message("Jerri: Don't dirty your hands king", c="Jerri")

    ## more nonsense to demo 
    $ chat_message("Jerri: @Felix eat fucking dirt")
    $ chat_message("Felix: You first")
    $ chat_message("Jerri: BROOOOOOOOO")

    $ chat_message("Jerri: He's actually the worst isn't he", c="Jerri")
    $ chat_message("Jerri: Like", c="Jerri")
    $ chat_message("Jerri: What the hell is his problem", c="Jerri")

    $ chat_message("Major: ?")
    $ chat_message("Sungho: lol what we miss")
    $ chat_message("Jerri: Felix being an absolute dickbag")
    $ chat_message("Jerri: lol", ot="Felix,Sungho,Major")
    $ chat_message("Major: he what", ot="Sungho,Felix")
    $ chat_message("Felix: she's LYING", ot="Sungho")
    $ chat_message("Sungho: HAHAHAHAHA")

    $ renpy.pause(hard=True)
