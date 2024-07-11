# Basic Usage
You can start from this repo to build your project, or just copy over the `chat_program.rpy` script + choice screen code from screens.rpy + stuff in the `images` folder to get started. If you copy those three things over, it should still all work fine (there just might be some small formatting you'll have to do bc I forgot what I did in the screens section).

Please note that the examples we have below do not tie out to the demo in there! The demo is based on other characters / channel names, but the basics are the same.


# Setting Up
The following variables need to be modified to suit your game before you start running the program. You can find these in the `reset_chats()` function in `chat_program.rpy`.

## current_window / active_window
Set these to whatever your initial default channel name is.
```
current_window = "#general"
active_window = "#general"
```

## chat characters
Default all characters that will send messages in the chat as a ChatCharacter() object. You can pass arguments to it to specify the character's avatar icon and name color for display.
```
default mc = ChatCharacter("[player_fname] [player_lname]", is_player=True, icon="images/Player.png")
default r = ChatCharacter("Robobarbie", icon="images/Robo.png", name_color="#E4C443")
```

All attributes can be changed mid-game, so e.g. if you want to change a character's name color or icon at some point, you can do this in the script:
```
$ mc.icon = "images/New_Player.png"
$ r.name_color = "#000"
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
    "#general" : None
}
```


# Beginning of Script
You can tweak this all you want, but you'll want to put something like this at the beginning of your script so your player can have a name and actually interact in chat.
```
label start:
    $ reset_chats()

label choose_name:
    $ player_fname = renpy.input("First name?")
    if player_fname in all_npc_first_names:
        "... not that one."
        jump choose_name
    $ player_lname = renpy.input("Last name?")
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
    window:
        padding (10,10)
        background None
        area (842, 203, 1369, 880) # 2560 x 1440 screen
        has vbox
        spacing 20
        text current_window color "#FFFFFF"
        viewport yadjustment yadj:
            xmaximum 1369
            scrollbars "vertical"
            mousewheel True

            has vbox
            box_wrap True
            for chat in channels[current_window]:
                hbox:
                    spacing 20
                    if chat["include_icon"]: # if should include icon of sender
                        add chat["icon"]
                    else:
                        null width 70 # change this to the width of the icons

                    vbox:
                        if chat["include_name"]: # if should include name of sender
                            text chat["name"]: # sender name
                                size 30
                                color chat["name_color"] # By default, this uses name_color argument passed to the ChatCharacter(). If you want all characters to just use the same color, then just change this to color "#FFF" (replace "#FFF" with whatever your desired color hex value)
                                line_spacing 10
                                bold True
                                # You can change styling of the name here

                        text chat["message"]: # chat message
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
You can mostly write the script with normal Ren'Py script syntax.

Additional arguments can be passed to each chat message:
### c
**the channel.** This sets the channel that this message will be sent to. If not provided as argument, the chat message will default to being sent in the last used channel. So you only have to pass this argument for the first message whenever you switch to a new channel.

### ot
**other typers.** This is a single ChatCharacter() object or a list of ChatCharacter() objects, representing the other characters whose names would show up as typing while the current message is being typed.

### is_player
**is this the player.** This is a boolean that tells us whether or not this message comes from the player. This is usually set in the ChatCharacter() definition, so you should generally not need to pass it as argument to a specific line.

### fastmode
**quickness.** if you want to ignore the timing mechanics of how messages are sent, put a float in here to say how fast to send this message.

### !! Examples !!
Set up some characters that will speak in chat.
```
default r = ChatCharacter("Robobarbie", icon="images/Robo.png", name_color="#E4C443")
default a = ChatCharacter("Alex Xela", icon="images/Alex.png", name_color="#48E443")
default al = ChatCharacter("Allie Vera", icon="images/Allie.png", name_color="#90DFFF")
default s = ChatCharacter("Selen Dri", icon="images/Selen.png", name_color="#CCAEFF")
default w = ChatCharacter("Windchimes", icon="images/Windchimes.png", name_color="#FF7519")
```
A message sent in the main channel from "Robobarbie".
```
r "Hello! How's everyone doing today?"
```
A reply from one person, with other people also typing responses.
```
a "Tired. I'm incredibly tired." (ot = [al, s])
```
Those other typers then reply, with one message showing up quickly to simulate them hitting send at the same time.
```
al "Personally I'm feeling stupendous." (ot = s)
s "I'm DYING guys." (fastmode = 0.1)
```
One of the chatters starts a side chat in another channel. The next chat without a channel argument passed will continue to be sent in #game-chat channel.
```
w "CAN SOMEONE PLEASE LOG ON AND HELP ME WITH THIS BOSS." (c = "#game-chat")
w "I SWEAR THIS BOSS NEEDS A NERF"
```

## player choice menu
The syntax for showing choice menus is mostly the same as the Ren'Py default menu syntax.
```
r "Hello! How's everyone doing today?"

menu:
    "I'm doing alright. Thanks for asking!":
        r "That's great to hear!"
    "Today sucks.":
        r "Aw, sorry to hear that."
    "{i}Ignore Robo's chat{/i}" (auto_send=False):
        pass

w "Ughhh don't get me started"
r "Would anyone else like to share?"
```

As you can see in the above example for the third choice, it's possible to pass an argument to a choice **auto_send**
By default, clicking on the choice button will automatically send the chosen choice text as a chat message from the player. But there may be cases where you don't want that to happen — for example, in the above case, I want to have a choice where you ignore and don't send a reply. In those cases, you can pass (auto_send=False) to the choice so it doesn't automatically send the choice caption as chat message.

This can also be used for cases where you *do* want the chosen choice caption to be sent as a chat message from MC, but there are some additional reasons for wanting **(auto_send=False)**, e.g.
- you want a change in the character's attributes (name / avatar icon / name color) to reflect immediately upon choosing the choice in the chat message sent by MC, but the change is only set in the choice branch;
- the chosen choice message is too long, and you want the message to be broken up into multiple messages rather than sent by MC immediately all at once.

In those cases, you'd have to repeat the choice message caption as chat message lines from mc, along with adding **(auto_send=False)** to the choice.
```
menu:
    "hey everyone check out my cool new avatar!" (auto_send=False):
        $ mc.icon = "images/Cooler_Player.png"
        mc "hey everyone"
        mc "check out my cool new avatar!" (fastmode=1.5)
```

# Other Functions
Some other functions to know about in case you want to tweak how they work are the following.
* **set_is_typing()** controls the logic for how the chat timers work, and
* **format_typers()** formats the string for who is typing.

# Mixing with ADV Mode
If you want to mix in ADV mode segments, you should define separate characters for the ADV mode speakers using the default Ren'Py Character() class.
```
default mc_vnmode = Character("[player_fname]")
```

In script:
```
# Swap to ADV textbox mode - hide chat screen and turn off auto mode
$ preferences.afm_enable = False
hide screen chat_messages_view

mc_vnmode "Test VN mode line"
```

To show a choice menu in ADV mode, you can pass the argument **(chat_menu=False)** to the menu like this:
```
menu (chat_menu=False):
    "A normal ADV mode choice":
        mc_vnmode "I'm all out of lines."
    "A second choice":
        pass
```

You can style the ADV mode choice buttons and the chat mode choice buttons separately in the choice screen in screens.rpy.

# The Demo
Inside of `script.rpy` is a small demo of chats moving between channels + player choices with a diff set of characters than above. Should help show it all in action!


# Changelog
Last updated: Jul 11, 2024 by Windchimes
- Added a `ChatCharacter()` class so that chat messages can be added using Ren'Py script syntax rather than using `$ chat_message()` and `$ player_choice()` functions directly
- Removed `$ player_choice()` function as it's no longer needed
- Removed `character_names` dictionary. All names (with or without last name) for display should now be passed directly to `ChatCharacter()` definition
- Added ability to pass a specific file path to use as icon to the `ChatCharacter()` definition, rather than have the screen auto-find an icon from `images` folder that matches the character name. The `icon` attribute can be changed mid-script as well
- Added ability to pass `name_color` argument to the `ChatCharacter()` definition. This can be changed mid-script as well
- `ot` argument passed to a line now takes a single `ChatCharacter()` or a list of `ChatCharacter()` objects, rather than a string of character names
- Changed `chat_message()` function so that when adding a new chat message to the channel list for display, it passes a dictionary with separate entries for `name`, `message`, `icon`, `name_color`, `include_name` and `include_icon`, instead of a single string of "Name: message"
- Adjusted `chat_messages_view` screen code to accommodate for the above change, so that it's now possible to style the name and message differently much easier
- Changed behavior of the choice button in screens.rpy and `chat_message()` function so that user can control whether choosing a choice would automatically send the choice button caption as chat message from MC or not by passing `(auto_send=False)` to the choice as argument
- Added examples on how to swap between ADV mode and chatroom mode. Edited choice screen in screens.rpy so it can take menu argument `chat_menu` to determine which mode of choices to use, which can be styled differently
