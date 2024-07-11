##-----------------------------------------------------
## chat program setup

## basic variables

default player_fname = ""
default player_lname = ""

# list of other npc names to check for conflict with player input name
default -1 all_npc_first_names = [ ]

# autoscroll vars
default yadjValue = float("inf")
default yadj = ui.adjustment()

# chat speed - you can make this changeable as a setting
default chat_speed = 1
default is_paused = False

# this is for formatting the text
default who_is_typing = ""
default who_was_typing_list = []
default last_sender = ""
default last_window = ""
default wait_time_prev = 0

# this is also for formatting
default current_window = ""
default active_window = ""

# chat groups
default channels = {}

# optional images for chat icons
default channel_images_on = False
default channel_images = {}

# indicator for when a new message arrives
default channels_new_message = {}

# who sent the last message in the channel
default channels_last_sender = {}

# what sounds will play for pinging
default ping_sound = "audio/ping.mp3"
default ping_sound_other_channel = "audio/ping_other.mp3"
# https://pixabay.com/sound-effects/search/ping/




init python:

    class ChatCharacter():
        """
        A class to make adding chat messages as similar to normal Ren'Py script syntax as possible.
        """

        def __init__(self, name, icon=None, name_color="#FFF", is_player=False):
            """
            name: string
            Character's name displayed in chat.

            icon: string
            Name of the icon image for the chat character.

            name_color: string
            Hex code of the color to use for the chat character's name when displayed.

            is_player: boolean
            True if it's MC/player's character. False if it's anyone else.
            """
            self.name = name
            self.icon = icon
            self.name_color = name_color
            self.is_player = is_player

            store.all_npc_first_names.append(self.name.split()[0])

        def __call__(self, what, c=None, ot=None, fastmode=-1,**kwargs):
            """Function that is called when a script dialogue line said by a ChatCharacter() object is processed"""

            # If there's a (c="#some-channel") channel say argument passed to the line, then use that channel and remember it for future lines until a new channel say argument is passed
            # In other words, it'll by default use the last channel for chat messages until a new channel is specified
            if c:
                channel = c
            else:
                channel = last_window or "#team-adoai" # TODO change this "#team-adoai" to your own default channel name

            # if ot isn't a list and is only a single element, turn it into a list for processing later
            if ot and not isinstance(ot, list):
                ot = [ot]

            chat_message(self, what, channel, ot, fastmode, self.is_player) # Send the chat message

    ## chat functions

    ### reset_chats() ###
    # function to call to reset/clear everything
    # you'll want to call this whenever you want
    # all the chats to clear.
    # it's good to do this at the beginning of a game,
    # or between days if you don't care about preserving
    # chat history.
    # you will need to remember to add variables to this
    # if they aren't included in the default setup!
    def reset_chats():
        global current_window
        global active_window
        global channels
        global channel_images_on
        global channel_images
        global channels_new_message
        global channels_last_sender
        global who_is_typing
        global who_was_typing_list
        global last_sender
        global last_window

        current_window = "#team-adoai"
        active_window = "#team-adoai"

        who_is_typing = ""
        who_was_typing_list = []
        last_sender = ""
        last_window = "X"
        wait_time_prev = 0

        # chat groups
        channels = {
            "#team-adoai" : [],
            "Felix" : []
        }

        # optional images for chat icons
        channel_images_on = False
        channel_images = {
            "#team-adoai" : "channel icons/_default.png",
            "Felix" : "channel icons/_default.png"
        }

        # indicator for when a new message arrives
        channels_new_message = {
            "#team-adoai" : False,
            "Felix" : False
        }

        # who sent the last message in the channel
        channels_last_sender = {
            "#team-adoai" : None,
            "Felix" : None
        }

    def chat_message(sender, message, c="#team-adoai", ot=None, fastmode=-1, is_player=False, icon=None):
        """
        sender: ChatCharacter() object
        ChatCharacter() object of the person who sends the message

        message: string
        The content of the chat message sent

        c: string
        Name of the channel where the chat message is sent

        ot: list of ChatCharacter() objects
        A list of ChatCharacter objects representing any other people who are also typing at the same time as the sender

        fastmode: number
        -1 by default where the chat message will be sent after a default calculated delay time. If set to a different number, the chat will be sent after that number in seconds.

        is_player: boolean
        True if it's the player sending this chat. False otherwise. Generally shouldn't have to worry about setting it since it takes from the ChatCharacter() is_player attribute automatically.
        """

        global chat_speed
        global channels
        global channel_images_on
        global channel_images
        global channels_new_message
        global channels_last_sender
        global current_window
        global active_window
        global who_is_typing
        global wait_time_prev
        global last_sender
        global last_window
        global yadj
        global yadjValue
        global is_paused

        # get new active channel
        active_window = c

        # pause briefly if we are swapping windows
        if last_window != active_window and not is_player:
            renpy.pause(1)

        # set the wait time of the current message (typing it out)
        wait_time = len(message)/5/chat_speed

        # change "who is typing"
        if is_player: # If this is the player

            if chat_speed != 100:
                who_is_typing = ""

            # If last message was also from player (most likely because it's from a choice with auto_send=False and you split up the choice caption into multiple chat messages to send manually)
            if channels_last_sender[c] == sender and last_window == active_window:

                # Set others typing if there was ot passed
                if ot and chat_speed != 100:
                    for i, typer in enumerate(ot):
                        if i == 0:
                            typers_string = typer.name
                        else:
                            typers_string = typers_string + ", " + typer.name
                    set_is_typing(typers_string, wait_time, wait_time_prev, fastmode, carry_over_prev_typers=False)

                # Otherwise, pause before sending so MC's messages don't all appear at once
                elif chat_speed != 100:
                    if fastmode == -1:
                        renpy.pause(wait_time)
                    else:
                        renpy.pause(fastmode)
        else:
            if chat_speed != 100:

                # Add the current message's sender name to who's typing
                typers_string = sender.name

                # Add names of others typing at the same time
                if ot:
                    for typer in ot:
                        typers_string = typers_string + ", " + typer.name

                set_is_typing(typers_string, wait_time, wait_time_prev, fastmode)

            else:
                who_is_typing = ""


        # set an additional wait time for the next message
        # this is to simulate people reading the previous message
        # before they reply. we take half of what the typing wait time
        # was for the message they are reading.
        wait_time_prev = wait_time/2

        # if we've never seen this channel before, add it
        if c not in channels.keys():
            channels[c] = []
            channels_last_sender[c] = ""
            if channel_images_on:
                channel_images[c] = "channel icons/" + c + ".png"

        # if not active in that channel, light up that button
        if current_window != c:
            channels_new_message[c] = True

        # send the message
        if channels_last_sender[c] == sender and last_window == active_window:
            # Last message was also sent by this same person. Don't include icon & name
            channels[c].append( {
                    "name": sender.name,
                    "message": message,
                    "icon": sender.icon,
                    "name_color": sender.name_color,
                    "include_icon": False,
                    "include_name": False
                }
            )
        else:
            channels[c].append( {
                    "name": sender.name,
                    "message": message,
                    "icon": sender.icon,
                    "name_color": sender.name_color,
                    "include_icon": True,
                    "include_name": True
                }
            )

        # play the sound
        if not is_player: # Don't play sound if it's the player sending the message
            if current_window == c:
                renpy.play(ping_sound)
            else:
                renpy.play(ping_sound_other_channel)

        # this will force the window to scroll down to the newest message
        # if the scrollbar is already at the bottom or
        # the message is from the player
        if yadj.value == yadj.range or is_player:
            yadj.value = float('inf')

        # update who the new last sender is
        # this is to reference whether or not
        # to append the name to the top of the message.
        channels_last_sender[c] = sender

        # update what the last window is
        # this is also to reference that
        last_window = c

        # handling play/pause
        # if player, immediately start up again (skip through renpy.pause)
        # by turning on auto-forward. this could cause issues later, so
        # you'll want to be aware of that happening.
        if is_paused and not is_player:
            renpy.pause()
            _preferences.afm_enable = True
            is_paused = False
        elif is_paused:
            _preferences.afm_enable = True
            is_paused = False


    ### set_is_typing(n, wt, wtp) ###
    # n = string containing typers
    # wt = typing wait time
    # wtp = previous wait time
    # carry_over_prev_typers = show previously typing names or not
    # show who is typing + logic for timing
    def set_is_typing(n, wt, wtp, fastmode=-1, carry_over_prev_typers=True):

        global who_is_typing
        global who_was_typing_list

        # create new "who is typing" string
        n_list = n.split(",")
        n_list.sort(key=lambda v: v.upper())

        # show only names that carry over from previous typing
        if carry_over_prev_typers:
            pre_typers = []
            for i in n_list:
                if i in who_was_typing_list:
                    pre_typers.append(i)
            if len(pre_typers) > 0:
                who_is_typing = format_typers(pre_typers)
            else:
                who_is_typing = ""
            if fastmode != -1:
                renpy.pause(wtp)

        # show new list of typers
        who_is_typing = format_typers(n_list)
        if fastmode == -1:
            renpy.pause(wt)
        else:
            renpy.pause(fastmode)

        # save off who was now typing + reset
        who_was_typing_list = n_list
        who_is_typing = ""


    # format logic for typing string
    # this is only showing one person for some reason
    def format_typers(n_list):

        if len(n_list) > 3:
            w = "Several people are typing..."
        else:
            w = ""
            for i in n_list:
                if i != n_list[-1]:
                    w = w + i + ", "
                else:
                    w = w + i + " "
            if len(n_list) > 1:
                w = w + "are typing..."
            else:
                w = w + "is typing..."
        return(w)


##-----------------------------------------------------
## screen

screen chat_messages_view:
    add "images/chat ui/chat_window.png"

    ## messages area
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


    ## sidebar
    window:
        padding (10,10)
        background None
        area(334, 200, 487, 1146)
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

