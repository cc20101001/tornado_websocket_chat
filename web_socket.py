#coding=utf-8
import functools
import tornado.web
import tornado.websocket
import tornado.httpserver
import tornado.ioloop
import hashlib

class Single(object):

    obj_list = {}

    def __call__(self, cls):
        @functools.wraps(cls)
        def wraper():
            obj_cls = self.obj_list.get(cls, "")
            if not obj_cls:
                obj_cls = cls()
                self.obj_list[cls] = obj_cls
            return self.obj_list[cls]
        return wraper


@Single()
class Mediator(object):

    def __init__(self):
        self.people_dict = {}

    def register_people(self, cookies_hash_id, brower_hash_id, brower):
        if not self.people_dict.get(cookies_hash_id, ""):
            self.people_dict[cookies_hash_id] = []
        brower_tag = {brower_hash_id: brower}
        self.people_dict[cookies_hash_id].append(brower_tag)

    def send(self, message, message_to_id=None):
        if not message_to_id:
            for id, people in self.people_dict.items():
                for one in people:
                    for key, value in one.items():
                        value.notify(message)
        else:
            brower_list = self.people_dict.get(message_to_id)
            if brower_list:
                for one in brower_list:
                    for key, value in one.items():
                        value.notify(message)

    def release_people(self, cookies_hash_id, brower_hash_id):
        brower_list = self.people_dict.get(cookies_hash_id, "")
        if brower_list:
            for index, brower in enumerate(brower_list):
                obj = brower.get(brower_hash_id, "")
                if obj:
                    brower_list.pop(index)
        print brower_list


class WebSocketHandler(tornado.websocket.WebSocketHandler):

    mediator = Mediator()

    def __init__(self, *args, **kwargs):
        super(WebSocketHandler, self).__init__(*args, **kwargs)

    def register_mediator(self, mediator):
        self.mediator = mediator

    def notify(self, message):
        self.write_message(u"Your message was: " + message)

    def send(self, message, message_to):
        self.mediator.send(message, message_to)

    def _print_socket_info(self):
        cookies_hash_id, brower_hash_id = self._get_hash_id()
        cookies_list = self.mediator.people_dict.get(cookies_hash_id, [])
        print "您现在的cookiesid为: {} ,目前打开了 {} 个浏览器标签".format(cookies_hash_id, len(cookies_list) + 1)

    def _get_hash_id(self):
        md5 = hashlib.md5()
        md5.update(self.cookies["user"].value)
        cookies_hash_id = md5.hexdigest()
        md5.update(str(id(self)))
        brower_hash_id = md5.hexdigest()
        return cookies_hash_id, brower_hash_id

    def _register_mediator(func):
        def wrapper(self):
            self._print_socket_info()
            cookies_hash_id, brower_hash_id = self._get_hash_id()
            self.mediator.register_people(cookies_hash_id, brower_hash_id, self)
            self.register_mediator(self.mediator)
            func(self)
        return wrapper

    def _release_mediator(func):
        def wrapper(self):
            cookies_hash_id, brower_hash_id = self._get_hash_id()
            self.mediator.release_people(cookies_hash_id, brower_hash_id)
            func(self)
        return wrapper


    @_register_mediator
    def open(self):
        print self.mediator.people_dict

    def on_message(self, message):
        message_list = message.split(":")
        message = message_list[0]
        if len(message_list) == 2 and message_list[1] == "":
            message_to_id = None
        else:
            message_to_id = message_list[1]
        self.mediator.send(message, message_to_id)
        # self.write_message(u"Your message was: " + message)

    @_release_mediator
    def on_close(self):
        pass


class IndexPageHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")


class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', IndexPageHandler),
            (r'/websocket', WebSocketHandler)
        ]

        settings = {
            'template_path': 'templates',
            "cookie_secret": "lkjwlkejrlkwejrwklejrwerwerwerwerwerqwkejrkwjerkj/324=",
        }
        tornado.web.Application.__init__(self, handlers, **settings)


if __name__ == '__main__':
    ws_app = Application()
    server = tornado.httpserver.HTTPServer(ws_app)
    server.listen(8080)
    tornado.ioloop.IOLoop.instance().start()