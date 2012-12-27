import pprint
import simplejson

from flask_script import Manager, prompt_choices, Shell

class App:
    pass
app = App()

def create_app(config=None):
    app.debug = False
    app.config = {}
    print "CONFIG:", app.config

    if config is not None:
        print "Loading config from", config
        app.config.update(simplejson.load(open(config, "r")))
        print "CONFIG:", app.config

    return app

manager = Manager(create_app)


@manager.command
def dumpconfig():
    "Dumps config"
    pprint.pprint(app.config)


@manager.command
def output(name):
    "print something"
    print name
    print type(name)


@manager.command
def outputplus(name, url=None):
    "print name and url"
    print name, url


@manager.command
def getrolesimple():

    choices = ("member", "moderator", "admin")

    role = prompt_choices("role", choices=choices, default="member")
    print "ROLE:", role


@manager.command
def getrole():

    choices = (
        (1, "member"),
        (2, "moderator"),
        (3, "admin"),
    )

    role = prompt_choices("role", choices=choices, resolve=int, default=1)
    print "ROLE:", role


@manager.option('-n', '--name', dest='name', help="your name")
@manager.option('-u', '--url', dest='url', help="your url")
def optional(name, url):
    "print name and url"
    print name, url

manager.add_option("-c", "--config",
                   dest="config",
                   help="config file",
                   required=False)

manager.add_command("shell", Shell(make_context=lambda: {'app': app}))

if __name__ == "__main__":
    manager.run()
