# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 00:00:32 2015

@author: zhengzhang
"""
from chat_utils import *
from reversi import *


class ClientSM:
    def __init__(self, s):
        self.state = S_OFFLINE
        self.peer = ''
        self.me = ''
        self.out_msg = ''
        self.s = s
        self.game = base()

    def set_state(self, state):
        self.state = state

    def get_state(self):
        return self.state

    def set_myname(self, name):
        self.me = name

    def get_myname(self):
        return self.me

    def connect_to(self, peer):
        msg = M_CONNECT + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_CONNECT + 'ok'):
            self.peer = peer
            self.out_msg += 'You are connected with ' + self.peer + '\n'
            return (True)
        elif response == (M_CONNECT + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_CONNECT + 'hey you'):
            self.out_msg += 'Cannot talk to yourself (sick)\n'
        else:
            self.out_msg += 'User is not online, try again later\n'
        return (False)

    def gaming_with(self, peer):
        msg = M_GAME + peer
        mysend(self.s, msg)
        response = myrecv(self.s)
        if response == (M_GAME + 'ok'):
            self.peer = peer
            self.out_msg += 'You are playing with ' + self.peer + '\n'
            return True
        elif response == (M_GAME + 'busy'):
            self.out_msg += 'User is busy. Please try again later\n'
        elif response == (M_GAME + 'hey you'):
            self.out_msg += 'Play with the AI\n'
            self.state = S_SOLO
        else:
            self.out_msg += response
        return False

    def disconnect(self):
        msg = M_DISCONNECT
        mysend(self.s, msg)
        self.out_msg += 'You are disconnected from ' + self.peer + '\n'
        self.peer = ''

    def proc(self, my_msg, peer_code, peer_msg):
        self.out_msg = ''
        # ==============================================================================
        # Once logged in, do a few things: get peer listing, connect, search
        # And, of course, if you are so bored, just go
        # This is event handling instate "S_LOGGEDIN"
        # ==============================================================================
        if self.state == S_LOGGEDIN:
            # todo: can't deal with multiple lines yet
            if len(my_msg) > 0:

                if my_msg == 'q':
                    self.out_msg += 'See you next time!\n'
                    self.state = S_OFFLINE

                elif my_msg == 'time':
                    mysend(self.s, M_TIME)
                    time_in = myrecv(self.s)
                    self.out_msg += "Time is: " + time_in

                elif my_msg == 'who':
                    mysend(self.s, M_LIST)
                    logged_in = myrecv(self.s)
                    self.out_msg += 'Here are all the users in the system:\n'
                    self.out_msg += logged_in

                elif my_msg[0] == 'c':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.connect_to(peer) == True:
                        self.state = S_CHATTING
                        self.out_msg += 'Connect to ' + peer + '. Chat away!\n\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'

                elif my_msg[0] == 'g':
                    peer = my_msg[1:]
                    peer = peer.strip()
                    if self.gaming_with(peer):
                        self.state = S_GAMING
                        self.out_msg += 'Connect to ' + peer + '\n'
                        self.out_msg += '-----------------------------------\n'
                    else:
                        self.out_msg += 'Connection unsuccessful\n'
                elif my_msg[0] == '?':
                    term = my_msg[1:].strip()
                    mysend(self.s, M_SEARCH + term)
                    search_rslt = myrecv(self.s)[1:].strip()
                    if (len(search_rslt)) > 0:
                        self.out_msg += search_rslt + '\n\n'
                    else:
                        self.out_msg += '\'' + term + '\'' + ' not found\n\n'

                elif my_msg[0] == 'p':
                    poem_idx = my_msg[1:].strip()
                    mysend(self.s, M_POEM + poem_idx)
                    poem = myrecv(self.s)[1:].strip()
                    if (len(poem) > 0):
                        self.out_msg += poem + '\n\n'
                    else:
                        self.out_msg += 'Sonnet ' + poem_idx + ' not found\n\n'

                else:
                    self.out_msg += menu

            if len(peer_msg) > 0:
                if peer_code == M_CONNECT:
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are connected with ' + self.peer
                    self.out_msg += '. Chat away!\n\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_CHATTING
                elif peer_code == M_GAME:
                    self.peer = peer_msg
                    self.out_msg += 'Request from ' + self.peer + '\n'
                    self.out_msg += 'You are playing with ' + self.peer
                    self.out_msg += '. enjoy gaming!\n\nType yes to confirm\n'
                    self.out_msg += '------------------------------------\n'
                    self.state = S_GAMING
                # ==============================================================================
                # Start chatting, 'bye' for quit
                # This is event handling instate "S_CHATTING"
                # ==============================================================================
        elif self.state == S_CHATTING:
            if len(my_msg) > 0:  # my stuff going out
                mysend(self.s, M_EXCHANGE + "[" + self.me + "] " + my_msg)
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len(peer_msg) > 0:  # peer's stuff, coming in
                if peer_code == M_CONNECT:
                    self.out_msg += "(" + peer_msg + " joined)\n"
                else:
                    self.out_msg += peer_msg

            # I got bumped out
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN

            # Display the menu again
            if self.state == S_LOGGEDIN:
                self.out_msg += menu

        elif self.state == S_GAMING:
            if len(my_msg) > 0:
                mysend(self.s, M_DEAL + "[" + self.me + "] " + my_msg)
                if my_msg == 'bye':
                    self.disconnect()
                    self.state = S_LOGGEDIN
                    self.peer = ''

            if len(peer_msg) > 0:  # peer's stuff, coming in
                if peer_code == M_GAME:
                    self.out_msg += "(" + peer_msg + " joined)\n"
                else:
                    self.out_msg += peer_msg
            if peer_code == M_DISCONNECT:
                self.state = S_LOGGEDIN
            if self.state == S_LOGGEDIN:
                self.out_msg += menu


        elif self.state == S_SOLO:
            count = 0
            ele = '●'

            while True:
                self.game.show()
                get = input()
                print(get)

                if get == 'bye':
                    self.state = S_LOGGEDIN
                try:

                    x = int(get[0]) - 1
                    y = int(get[-1]) - 1
                    if count % 2 == 0:
                        ele = '●'
                    else:
                        ele = '○'

                    if self.game.flap(ele, y, x):
                        count += 1
                        self.game.show()
                        if count % 2 == 0:
                            ele = '●'
                        else:
                            ele = '○'
                        self.game.ai(ele)
                        count += 1
                except:
                    self.out_msg += 'wrong type \n'
                # ==============================================================================
                # invalid state
                # ==============================================================================
        else:
            self.out_msg += 'How did you wind up here??\n'
            print_state(self.state)

        return self.out_msg
