##-----------------------------------------------------
## chat program setup  

## basic variables 

default player_fname = ""
default player_lname = ""

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

# character info 
default character_names = {}

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
        global character_names 
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

        # character info 
        character_names = {
            "Felix" : "Doyle", 
            "Jerri" : "Ngo", 
            "Major" : "Alstone", 
            "Sungho" : "Go", 
            "Player" : "Name"
        }

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
            "#team-adoai" : "", 
            "Felix" : ""
        }

    ### player_choice(l) ### 
    # player makes a choice.
    # l = a list of tuples. 
    # the first element is the text, and 
    # the second element is the label that choice jumps to. 
    # if there is only one choice option, it will 
    # ignore the jump to label and will continue in 
    # the current label. 
    def player_choice(l): 
        global active_window
        global player_fname

        selected = renpy.display_menu(l)
        x = "_"
        for i in l: 
            if i[1] == selected: 
                x = i[0]
        chat_message(player_fname + ": " + x, c = active_window, is_player = True)
        if len(l) > 1: 
            renpy.jump(selected)

    ### chat_message(s, c, ot, is_player, fastmode) ### 
    # s = "character_name: message sent"
    # c = where to send message 
    # ot = who else is typing 
    # is_player = is the player sending this 
    # fastmode = should this message send fast at this speed (in seconds)
    # new message sent. 
    # this will likely be what is customized the most to your needs! 
    def chat_message(s, c="#team-adoai", ot="", is_player = False, fastmode=-1): # string, channel, others typing, is player
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
        global character_names
        global yadj 
        global yadjValue
        global is_paused

        # split into name / content, get new active channel  
        n = s.split(': ', 1)[0]
        t = s.split(': ', 1)[1]
        active_window = c 

        # pause briefly if we are swapping windows 
        if last_window != active_window: 
            renpy.pause(2)

        # set the wait time of the current message (typing it out)
        wait_time = len(t)/5/chat_speed

        # change "who is typing" 
        if not is_player:
            if ot != "" and chat_speed != 100: 
                set_is_typing(n + ", " + ot, wait_time, wait_time_prev, fastmode)
            elif chat_speed != 100:
                set_is_typing(n, wait_time, wait_time_prev, fastmode)
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
        # this method appends the name directly to the message, 
        # but if you want to do more intense formatting / separate the 
        # name out, you can always append the name to its own list. 
        if channels_last_sender[c] == n and last_window == active_window: 
            channels[c].append(t)
        else: 
            channels[c].append("\n{b}" + n +  " " + character_names[n] +  "{/b}\n" + t)

        # play the sound 
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
        channels_last_sender[c] = n

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
    # show who is typing + logic for timing 
    def set_is_typing(n, wt, wtp, fastmode=-1): # names 
        #global who_is_typing 
        global who_is_typing
        global who_was_typing_list 

        # create new "who is typing" string 
        n_list = n.replace(" ", "").split(",")
        n_list.sort(key=lambda v: v.upper())

        # show only names that carry over from previous typing 
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
        global character_names 

        if len(n_list) > 3: 
            w = "Several people are typing..."
        else:
            w = ""
            for i in n_list: 
                if i != n_list[-1]:
                    w = w + i + " " + character_names[i] + ", " 
                else: 
                    w = w + i + " " + character_names[i] + " "
            if len(n_list) > 1: 
                w = w + " are typing..."
            else: 
                w = w+ " is typing..."
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

