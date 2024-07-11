##-----------------------------------------------------
## INFO

# Welcome to simple chat simulator. This one is meant to emulate a Slack interface,
# but can be used for Discord or other things with some tiny changes.
# All setup code can be found in "chat_program.rpy"

# New messages appear on the screen "chat_messages_view".

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
## CHOICE SCREEN

# YOU MUST CHANGE YOUR CHOICE SCREEN TO BE SOMETHING LIKE THIS IN ORDER FOR
# CHOICES TO APPEAR ON THE CORRECT WINDOW AND FOR FORMATTING TO WORK

# screen choice(items, channel=active_window):
#     style_prefix "choice"

#     window:
#         area (851, 1129, 1349, 194)
#         background None
#         if active_window == current_window:
#             vbox:
#                 xalign 0.0
#                 spacing 0
#                 yalign 0.5
#                 for i in items:
#                     textbutton i.caption:
#                         if not i.kwargs.get("auto_send", True):
#                             action i.action
#                         else:
#                             action [Function(chat_message, mc, i.caption, channel, is_player =True), i.action] # change mc to the object name you defined for your player character
#                         xmaximum 1300
#                         background None
#                         text_xalign 0.0

# define gui.choice_button_width = None
# define gui.choice_button_height = None


##-----------------------------------------------------
## DEMO

## Set up characters that'll speak in chat
default mc = ChatCharacter("[player_fname] [player_lname]", is_player=True, icon="images/Player.png")
default j = ChatCharacter("Jerri Ngo", icon="images/Jerri.png", name_color="#48E443")
default f = ChatCharacter("Felix Doyle", icon="images/felix.png", name_color="#E4C443")
default m = ChatCharacter("Major", icon="images/Major.png")
default s = ChatCharacter("Sungho", icon="images/Sungho.png")

# If you want characters that use normal ADV/NVL visual novel textbox mode, just set it up the normal way with Character() instead of ChatCharacter()
# default mc_vnmode = Character("[player_fname]")

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
    ## show chat screen + disable rollback when in chat view
    $ _rollback = False # Can comment out this line if you want because rollback actually works by jumping back to the last chat choice
    window hide
    show screen chat_messages_view

    ## in team chat
    j "LOOOOSSSEERRR LOSER LOSER LOSER"  (c="#team-adoai", ot=f)
    j "KEEP TYPING LOOOOOOOOOSER" (ot=f)
    f "Holy fucking shit"

    menu:
        "Huh? What?":
            f "You're telling me"
        "Can you both calm down":
            j "NO!!!!"

    ## in felix chat
    f "Can you believe this bullshit" (c="Felix")
    menu:
        "tf are you talking about":
            pass

    ## in jerri chat (new chat!)
    j "Tell that asshole he can eat fucking dirt" (c="Jerri")
    pause 2
    j "Actually"
    j "Don't dirty your hands king"

    menu:
        "??????":
            pass

    ## more nonsense to demo
    j "@Felix eat fucking dirt" (c="#team-adoai")
    f "You first"
    j "BROOOOOOOOO"

    j "He's actually the worst isn't he" (c="Jerri")
    j "Like"
    j "What the hell is his problem"

    menu:
        "honestly you both seem to have a lot of problems":
            pass

    m "?" (c="#team-adoai")
    s "lol what we miss"(fastmode=0.2)
    j "Felix being an absolute dickbag"
    j "ITS TRUE DONT EVEN TRY TO DENY IT"(ot=[f, s, m])
    m "he what" (ot=[s, f])
    f "she's LYING" (ot=s)
    s "HAHAHAHAHA"

    menu:
        "wait hold on everyone look at my new icon and name color that i stole from Felix!" (auto_send=False):

            $ mc.icon = "images/Felix.png" # change icon image for mc
            $ mc.name_color = "#E4C443" # change name color for mc
            # You can do this for other characters mid-game as well with e.g. j.name_color = "#000"

            # If you put (auto_send=False) after the choice like above, then the choice message doesn't auto send itself after you press the choice button. You'll have to copy the line and add it like normal chat messages yourself
            # Mostly for cases like this where e.g. you have a icon/name/name_color change after the choice and you want the choice chat message to already reflect the changes
            # Or if your choice message is really long and you find it weird that MC would send a whole paragraph in one go, then you'd want to break it up into multiple mc "dialogue" lines
            # Basically like this example that illustrates both cases
            mc "wait hold on everyone"
            mc "look at my new icon and name color that i stole from Felix!"(fastmode=1, ot=[f, s])

    $ preferences.afm_enable = False
    $ renpy.pause(hard=True)
