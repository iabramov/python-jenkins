from async_server import AsyncHTTPServer
import signal

httpd = AsyncHTTPServer(False)

# class GracefulKiller:
#     httpd = None
#     def __init__(self):
#         signal.signal(signal.SIGINT, self.exit_gracefully)
#         signal.signal(signal.SIGTERM, self.exit_gracefully)
#         self.httpd = AsyncHTTPServer(False)

#     def exit_gracefully(self, signum, frame):
#         self.httpd.stop()

# # if __name__ == '__main__':
# killer = GracefulKiller()
