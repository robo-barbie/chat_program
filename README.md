# Basic Usage
You can start from this repo to build your project, or just copy over the `chat_program.rpy` script + stuff in the `images` folder to get started. If you copy those two things over, it should still all work fine (there just might be some small formatting you'll have to do bc I forgor what I did in the screens section).

Please note that the examples we have below do not tie out to the demo in there! The demo is based on other characters / channel names, but the basics are the same. 


# Setting Up
The following variables need to be modified to suit your game before you start running the program. You can find these in the `reset_chats()` function in `chat_program.rpy`. 

## current_window / active_window
Set these to whatever your initial default channel name is. 
```
current_window = "#general"
active_window = "#general"
```

## character_names
This takes in first and last names as a dictionary. All characters must be in here. The framework will try to find files in the `images` folder by default that match the first names for the chat icons.
```
character_names = {
    "Robo" : "Barbie", 
    "Alex" : "Xela", 
    "Allie" : "Vera", 
    "Selen" : "Dri"
}
```
```
in folder /game/images/
Robo.png
Alex.png
Allie.png
Selen.png
```

## channels
This is a dictionary that holds all text for all channels. You need at least one channel in there. 
```
channels = {
  "#general" : []
}
```

## channel_images_on / channel_images
If you want your channels to have images displayed by their names, toggle this on and indicate what those names should be. 
```
channel_images_on = True
channel_images = {
    "#general" : "images/general_icon.png"
}
```

## channels_new_message
This is used to make tabs flash or light up buttons to tell the player a new message is in a window they might not be looking at currently. 
```
channels_new_message = {
    "#general" : False
}
```

## channels_last_sender 
This tells us who sent the last message and is used for deciding whether or not we should display a name above the message sent. 
```
channels_last_sender = {
    "#general" : ""
}
```


# Beginning of Script 
You can tweak this all you want, but you'll want to put something like this at the beginning of your script so your player can have a name and actually interact in chat. 
```
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
    $ _rollback = False # disable rollback (robo public enemy #1) 
    window hide # get rid of say screen 
    show screen chat_messages_view # show chat screen (main function of the game) 
```


# The Screen 
The chat UI is one screen within `chat_program.rpy` called `chat_messages_view`. It comes with the following as default: 
* a message window
* a sidebar for channels, and
* chat controls (play/pause, chat speed)

In order to use this without breaking out of the box, you'll need that images folder. 

At the top of the screen, there is a small `add` that puts the chat bg on the screen. You can swap out the image there. 

## The Message Window 
This is likely where you will do the most changes to suit your needs, since this is all about how those messages look to the player. 
```
    ## messages area 
    window: 
        padding (10,10)
        background None 
        area (842, 203, 1369, 880) # the place on screen the messages will go 
        vbox:
            spacing 20
            text current_window color "#FFFFFF"
            viewport  yadjustment yadj: 
                xmaximum 1369 
                scrollbars "vertical"
                mousewheel True 

                vbox: 
                    box_wrap True
                    for n in channels[current_window]: 
                        hbox: 
                            spacing 20 
                            if n.split(" ")[0].startswith("\n"):
                                vbox: 
                                    null height 50 # this i set after eyeballing how far to drop the icon 
                                    if n.split(" ")[0][4:] == player_fname: 
                                        add "Player.png"
                                    else:
                                        add n.split(" ")[0][4:] + ".png"
                            else: 
                                null width 70 # width of the icons 
                            text n:
                                size 30  
                                color "#FFFFFF"
                                line_spacing 10

            if current_window == active_window: 
                text who_is_typing color "#FFFFFF" size 20
```

## The Sidebar 
This shows available channels to the player, and is also super customizable. Similar logic can be used/adapted to show characters online. 
```
    ## sidebar 
    window: 
        padding (10,10)
        background None
        area(334, 200, 487, 1146) # where the sidebar will go 
        vbox: 
            spacing 20
            for l in channels.keys(): 
                hbox: 
                    if channel_images_on:
                        imagebutton: 
                            idle channel_images[l]
                    textbutton l:
                        if channels_new_message[l]:
                            text_color "#EAC119"
                        else: 
                            text_color "#FFFFFF"
                        text_hover_color "#D6FF1B"
                        action SetDict(channels_new_message, l, False), SetVariable("current_window", l)
```

## Chat Functions 
This is used to control the flow of the messages by the player. Mess with play/pause at ur own risk! 
```
    ## chat functions (speed, play/pause)
    hbox: 
        yalign 1.0
        xalign 0.0 
        spacing 50 

        null width 100 

        imagebutton: 
            if is_paused: 
                auto "images/chat ui/button_pause_%s.png"
                action SetVariable("is_paused", False),SetVariable("_preferences.afm_enable", True)
            else: 
                auto "images/chat ui/button_play_%s.png"
                action SetVariable("is_paused", True),SetVariable("_preferences.afm_enable", False)

        null width 100 
        
        imagebutton: 
            if chat_speed == 1: 
                idle "images/chat ui/button_speed_1_hover.png"
            else: 
                auto "images/chat ui/button_speed_1_%s.png"
            action SetVariable("chat_speed", 1)
        imagebutton: 
            if chat_speed == 2: 
                idle "images/chat ui/button_speed_2_hover.png"
            else: 
                auto "images/chat ui/button_speed_2_%s.png"
            action SetVariable("chat_speed", 2)
        imagebutton: 
            if chat_speed == 100: 
                idle "images/chat ui/button_speed_100_hover.png"
            else: 
                auto "images/chat ui/button_speed_100_%s.png"
            action SetVariable("chat_speed", 100) # this 100 is used to indicated super speed, do not change
```


# Writing the Script 
The chats rely on two main things to work. The `chat_message()` function, and the `player_choice()` function. The first is used to run all the things that happen when a message is sent, and the second is how we display options to chat to the player.

## chat_message()
`chat_message()` takes the following inputs: 
### s
**the chat message.** It must be formatted "NAME: MESSAGE", since it splits the name and text out via the colon.

### c 
**the channel.** This is simply the name of the channel you would like the message to be sent to. This has a default main chat it will send to if nothing is specified.
If you don't have the channel in any lists yet, it will automatically add the channel where it is needed in order to run. 

### ot 
**other typers.** This is a comma separated string of other names you would like to show up as typing while the current message is being typed.

### is_player 
**is this the player.** This is a boolean that tells us whether or not this message comes from the player. This is only used by the choice system.

### fastmode 
**quickness.** if you want to ignore the timing mechanics of how messages are sent, put a float in here to say how fast to send this message.

### !! Examples !!
A message sent in the main channel from "Robo". 
```
$ chat_message("Robo: Hello! How's everyone doing today?")
```
A reply from one person, with other people also typing responses. 
```
$ chat_message("Alex: Tired. I'm incredibly tired.", ot = "Allie, Selen")
```
Those other typers then reply, with one message showing up quickly to simulate them hitting send at the same time. 
```
$ chat_message("Allie: Personally I'm feeling stupendous.", ot = "Selen")
$ chat_message("Selen: I'm DYING guys.", fastmode = 0.1) 
```
One of the chatters starts a side chat in another channel. 
```
$ chat_message("Selen: CAN SOMEONE PLEASE LOG ON AND HELP ME WITH THIS BOSS.", c = "#game-chat")
```

## player_choice() 
You can either have only mutiple choices used by `player_choice` or also add in single choice points for immersion. 

### multiple choice 
You must have a label for each choice to jump to. In order to tie it back to the main story, you can add a jump at the end of those to get back to the main thread. 
```
label day1_start:
  $ chat_message("Robo: Hello! How's everyone doing today?")
  $ player_choice([
    ("I'm doing alright. Thanks for asking!", "day1_1"),
    ("Today sucks.", "day1_2")
  ])

label day1_1:
  $ chat_message("Robo: That's great to hear!")
  jump day1_3

label day1_2:
  $ chat_message("Robo: Aw, sorry to hear that.")
  jump day1_3

label day1_3:
  $ chat_message("Robo: Would anyone else like to share?")
```

### single choice 
For a single choice, you do not need a label to jump to. 
```
label day1_start:
  $ chat_message("Robo: Hello! How's everyone doing today?")
  $ player_choice([
    ("Just so-so, I think.", "")
  ])
  $ chat_message("Robo: Hopefully it gets better soon!") 
```

# Other Functions 
Some other functions to know about in case you want to tweak how they work are the following. 
* **set_is_typing()** controls the logic for how the chat timers work, and 
* **format_typers()** formats the string for who is typing.

# The Demo
Inside of `script.rpy` is a small demo of chats moving between channels + player choices with a diff set of characters than above. Should help show it all in action!
