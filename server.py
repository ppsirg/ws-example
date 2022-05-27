import asyncio
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.websocket
import tornado.options

from uuid import uuid4

LISTEN_PORT = 8000
LISTEN_ADDRESS = "127.0.0.1"

connection_pool = {}


async def rotate_key():
    while True:
        new_key = uuid4().hex
        print("new key", new_key)
        for key, conn in connection_pool.items():
            print(f"send {new_key} to connection {key}")
            conn.write_message({"new": new_key})
        await asyncio.sleep(2)


class ChannelHandler(tornado.websocket.WebSocketHandler):
    """
    Handler that handles a websocket channel
    """

    connection_name = None

    @classmethod
    def urls(cls):
        return [
            (r"/ws/", cls, {}),  # Route/Handler/kwargs
        ]

    def initialize(self):
        self.channel = None

    def open(self):
        """
        Client opens a websocket
        """
        self.connection_name = uuid4().hex
        connection_pool[self.connection_name] = self

    def on_message(self, message):
        """
        Message received on channel
        """
        if message == "get_name":
            self.write_message({"name": self.connection_name})
        else:
            self.write_message({"received": True})

    def on_close(self):
        """
        Channel is closed
        """
        print("closed message")

    def check_origin(self, origin):
        """
        Override the origin check if needed
        """
        return True


def main():
    # Create tornado application and supply URL routes
    app = tornado.web.Application(ChannelHandler.urls())

    # Setup HTTP Server
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(LISTEN_PORT, LISTEN_ADDRESS)

    # Start IO/Event loop
    lp = tornado.ioloop.IOLoop.instance()
    lp.add_callback(rotate_key)
    lp.start()


if __name__ == "__main__":
    main()
