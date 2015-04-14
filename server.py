#!/usr/bin/env python

import logging
import tornado.escape
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import os.path
import uuid

from battleline.game import Game
from battleline.player import Player

from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", LobbyHandler),
            (r"/new", NewGameHandler),
            (r"/login", LoginHandler),
            (r"/logout", LogoutHandler)
        ]
        settings = dict(
            cookie_secret="Fyffy3w8S1ChMNezHsWVl9161PtRKkwtrMH0+8Sn6YA=",
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            login_url="/login",
            xsrf_cookies=True,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

games = []
users = {}
loader = tornado.template.Loader(os.path.join(os.path.join(os.path.realpath(__file__) + '/../'), 'templates'))

class BaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
            return self.get_secure_cookie("user")

class LoginHandler(BaseHandler):
    def get(self):
        self.render('login_form.html')
    def post(self):
        self.set_secure_cookie("user", self.get_argument("name"))
        if not users.has_key(self.get_argument('name')):
            users[self.get_argument('name')] = {}
        self.redirect("/")

class LogoutHandler(BaseHandler):
    def get(self):
        self.set_secure_cookie("user", "")
        self.redirect('/')


class LobbyHandler(BaseHandler):
    @tornado.web.authenticated
    def get(self):
        print users
        if not users.has_key(self.get_current_user()):
            self.redirect('/logout')
            return
        # THIS IS SO PEOPLE CAN JUMP RIGHT INTO GAMES THAT ARE ONGOING
        # if users[self.get_current_user()].has_key('game'):
        #     game = users[self.get_current_user()]['game']
        #     player = users[self.get_current_user()]['player']
        #     self.redirect('/' + str(id(game)) + '/' + str(id(player)))
        #     return
        self.write(loader.load('lobby.html').generate(user=self.get_current_user(), games=games))

class NewGameHandler(BaseHandler):
    def get(self):
        game = Game(self.get_current_user())
        game.url = '/' + str(id(game))
        games.append(game)
        app.add_handlers(r'.*$', [(r'/' + str(id(game)), JoinGameHandler, {'game': game})])
        self.redirect('/' + str(id(game)))

class JoinGameHandler(BaseHandler):
    def initialize(self, game):
        self.game = game

    def get(self):
        player = Player(self.get_current_user())
        app.add_handlers(r'.*$', [(self.request.uri + '/' + str(id(player)),
             PlayerWebSocket, {'player': player})])
        self.redirect(self.request.uri + '/' + str(id(player)))


class PlayerWebSocket(tornado.websocket.WebSocketHandler):
    def __init__(self, *args, **kwargs):
        print 'wattttt'
        self.player = kwargs.pop('player')
        print 'Creating a new playersocket for %s' % self.player.name
        self.player.socket = self
        super(PlayerWebSocket, self).__init__(*args, **kwargs)
        self.write(loader.load('ingame.html').generate(user=self.get_current_user()))

    def open(self):
        print '%s joined' % (self.player.name)
        self.write(loader.load('ingame.html').generate(user=self.get_current_user()))

    def on_close(self):
        print '%s left' % (self.player.name)
        self.write(loader.load('lobby.html').generate(user=self.get_current_user(), games=games))

    def on_message(self, message):
        print '%s received "%s"' % (self.player.name, message)
        # try:
        #     params = message.split(' ')
        #     self.player.callbacks[params[0]](message=' '.join(params[1:]))
        # except Exception, e:
        #     self.player.socket.write_message('Uncaught:' + str(e))
        #     traceback.print_exc()

if __name__ == "__main__":
    tornado.options.parse_command_line()
    app = Application()
    app.listen(options.port)
    tornado.ioloop.IOLoop.current().start()
