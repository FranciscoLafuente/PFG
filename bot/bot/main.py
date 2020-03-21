
from cement import App, TestApp, init_defaults, Interface, Handler
from cement.core.exc import CaughtSignal

from controllers.banner import Nobita
from core.exc import BotError
from controllers.portscanner import PortScanner
from controllers.ipreverse import Shizuka
from interfaces.startbot import ScansInterface, ScansHandler
from interfaces.nobita import NobitaInterface, NobitaHandler

# configuration defaults
CONFIG = init_defaults('bot')


class Bot(App):
    """Mi BOT App primary application."""

    class Meta:
        label = 'bot'

        # configuration defaults
        config_defaults = CONFIG

        # call sys.exit() on close
        exit_on_close = True

        # load additional framework extensions
        extensions = [
            'yaml',
            'colorlog',
        ]

        # configuration handler
        config_handler = 'yaml'

        # configuration file suffix
        config_file_suffix = '.yml'

        # set the log handler
        log_handler = 'colorlog'

        # register handlers
        handlers = [
            Nobita,
            PortScanner,
            Shizuka,
            ScansHandler,
            NobitaHandler,
        ]
        interfaces = [
            ScansInterface,
            NobitaInterface,
        ]


class BotTest(TestApp, Bot):
    """A sub-class of Bot that is better suited for testing."""

    class Meta:
        label = 'bot'


def main():
    with Bot() as app:
        try:
            app.run()
            # Access to database
            g = app.handler.get('startbot', 'connect', setup=True)
            p = app.handler.get('nobita', 'portscan', setup=True)
            type_bot, scans = g.get_scan()
            # TODO: Tras el escaneo, hay que devolver los datos a la api y que esta los guarde.
            #  Ademas tiene que cambiar el campo 'done' a true
            for s in scans:
                if not s['done']:
                    # Start the scan with nobita bot
                    if 'Nobita' in type_bot:
                        g.send_scan(p.pscan(s['hosts']), s['_id'])
                    if 'Shuneo' in type_bot:
                        pass

        except AssertionError as e:
            print('AssertionError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except BotError as e:
            print('BotError > %s' % e.args[0])
            app.exit_code = 1

            if app.debug is True:
                import traceback
                traceback.print_exc()

        except CaughtSignal as e:
            # Default Cement signals are SIGINT and SIGTERM, exit 0 (non-error)
            print('\n%s' % e)
            app.exit_code = 0


if __name__ == '__main__':
    main()

