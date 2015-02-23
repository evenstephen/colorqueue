import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
from tornado.options import define, options
import random
import json
from collections import deque

define("port", default=8000, help="run on the give port", type=int)

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/", MainHandler), (r"/color/(\w+)", ColorHandler)]
        settings = dict( template_path = os.path.join(os.path.dirname(__file__), "templates"),
                         static_path = os.path.join(os.path.dirname(__file__), "static" ),
                         debug = True )
        self.color_queue_length = 100
        self.color_queue_refresh_pct = 0.2
        self.color_ints = range(0, 256)
        self.colors = deque(self.populate_colors())
        
        tornado.web.Application.__init__(self, handlers, **settings)

    def populate_colors(self, colors=deque([]) ):
        for i in range(len(colors), self.color_queue_length):
            red = random.choice(self.color_ints)
            blue = random.choice(self.color_ints)
            green = random.choice(self.color_ints)
            colors.appendleft( (red, green, green) )
        return colors

class ColorHandler(tornado.web.RequestHandler):
    def get(self, color_action):

        if color_action == "fetch":
            self.application.active_color = self.application.colors.pop()
            self.application.active_color_status = "fetch"
            self.write( {"red": self.application.active_color[0], 
                "green": self.application.active_color[1], 
                "blue": self.application.active_color[2], 
                "status": self.application.active_color_status} )
                
        elif color_action == "set":
            self.application.active_color_status = "set"
            self.write( {"red": self.application.active_color[0], 
                "green": self.application.active_color[1], 
                "blue": self.application.active_color[2], 
                "status": self.application.active_color_status} )
                
        elif color_action == "timeout":
            self.application.colors.appendleft(self.application.active_color)
            self.application.active_color_status = "timeout"
            self.write( {"status": self.application.active_color_status} )
            
        else:
            pass

        if len(self.application.colors) < self.application.color_queue_length * self.application.color_queue_refresh_pct:
            self.application.colors = self.application.populate_colors(self.application.colors)
            
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render(
            "index.html",
            page_title = "Steve's Color Queueing",
            header_text = "Welcome to Steve's Color Queueing!")

if __name__ == "__main__":
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()