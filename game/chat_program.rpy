##-----------------------------------------------------
## chat program setup 

init python: 

    ## basic variables 

    player_fname = ""
    player_lname = ""

    # autoscroll vars
    yadjValue = float("inf")
    yadj = ui.adjustment()

    # chat speed - you can make this changeable as a setting 
    chat_speed = 1 

    # this is for formatting the text 
    who_is_typing = ""
    who_was_typing_list = []
    last_sender = ""
    last_window = ""

    # this is also for formatting 
    current_window = ""
    active_window = ""

    # character info 
    character_names = {}

    # chat groups 
    channels = {}

    # optional images for chat icons
    channel_images_on = True
    channel_images = {}

    # indicator for when a new message arrives 
    channels_new_message = {}

    # who sent the last message in the channel 
    channels_last_sender = {}


    ## chat functions 

    # function to call to reset/clear everything 
    # this is where the variable basics are laid out 
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
        last_window = "X"

        who_is_typing = ""
        who_was_typing_list = []
        last_sender = ""

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
        channel_images_on = True
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

    # player makes a choice 
    def player_choice(l): 
        global active_window
        global player_fname

        selected = renpy.display_menu(l)
        x = "_"
        for i in l: 
            if i[1] == selected: 
                x = i[0]
        chat_message(player_fname + ": " + x, c = active_window, is_player = True)
        renpy.jump(selected)

    # new message
    def chat_message(s, c="#team-adoai", ot="", is_player = False): # string, channel, others typing, is player
        global chat_speed 
        global channels
        global channel_images_on
        global channel_images
        global channels_new_message
        global channels_last_sender
        global current_window
        global active_window 
        global who_is_typing
        global last_sender
        global last_window 
        global character_names
        global yadj 
        global yadjValue

        # split into name / content, get new active channel  
        n = s.split(': ', 1)[0]
        t = s.split(': ', 1)[1]
        active_window = c 

        # pause briefly if we are swapping windows 
        if last_window != active_window: 
            renpy.pause(2)

        if not is_player:
            # pause before displaying the message + change who is typing 
            wait_time = len(t)/10/chat_speed
            if ot != "": 
                set_is_typing(n + ", " + ot, wait_time)
            else: 
                set_is_typing(n, wait_time)

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
        if channels_last_sender[c] == n and last_window == active_window: 
            channels[c].append(t)
        else: 
            channels[c].append("\n{b}" + n +  " " + character_names[n] +  "{/b}\n" + t)

        if yadj.value == yadj.range:
            yadj.value = float('inf')
        #yadj.value = yadjValue

        # update who the new last sender is 
        channels_last_sender[c] = n

        # update what the last window is 
        last_window = c 

    # show who is typing + logic for timing 
    def set_is_typing(n, wt): # names 
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
        renpy.pause(wt * 0.25) # 1/4 of the pause time 

        # show new list of typers 
        who_is_typing = format_typers(n_list)
        renpy.pause(wt * 0.75) # 3/4 of the pause time 

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
    add "#372C3E" 

    ## messages area 
    window: 
        padding (20,20)
        background None 
        area(750, 200, 1560, 1040) # 2560 x 1440 screen 
        vbox:
            spacing 20
            text current_window color "#FFFFFF"
            viewport  yadjustment yadj: 
                xmaximum 1500 
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
                text who_is_typing color "#FFFFFF" size 20 yalign 1.0 
                        
    
    ## sidebar 
    window: 
        padding (20,20)
        background "#262029"
        area(250, 200, 400, 1040)
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
