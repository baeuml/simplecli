import pprint
import simplejson

from flask_script import Manager, prompt_choices, Shell

def create_ctx(config=None, debug=False):
    print "Creating app context"
    context = {}
    context['debug'] = debug
    context['config'] = {}

    if config is not None:
        print "Loading config from", config
        context['config'].update(simplejson.load(open(config, "r")))

    print "context:", context
    return context

manager = Manager(create_ctx)


@manager.command
def dumpconfig():
    "Dumps config"
    context = manager.context()
    pprint.pprint(context["config"])


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
def outputoptional(name, url):
    "print name and url, but don't require either"
    print name, url

manager.add_option("-c", "--config",
                   dest="config",
                   help="config file",
                   required=False)
manager.add_option("--debug",
                   dest="debug",
                   help="debug mode",
                   action="store_true")

manager.add_command("shell", Shell(make_context=lambda: manager.context()))

if __name__ == "__main__":
    manager.run()
