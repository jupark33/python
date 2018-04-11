from slacker import Slacker

token = ".."
slack = Slacker(token)
slack.chat.post_message('#mms', 'seventh python message')
