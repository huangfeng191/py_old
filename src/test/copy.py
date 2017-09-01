import sys
import web
urls = ('/', 'index')
app = web.application(urls, globals())
#根据class 查找对象
class index:
    def GET(self):
        return "Hello world11!"
def main(argv=None):
    app.run()
