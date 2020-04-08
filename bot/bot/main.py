
from cement import App, TestApp, init_defaults, Interface, Handler
from cement.core.exc import CaughtSignal

from core.exc import BotError
from interfaces.startbot import ScansInterface, ScansHandler
from interfaces.nobita import NobitaInterface, NobitaHandler
from interfaces.shizukaV2 import ShizukaV2Interface, ShizukaV2Handler
from interfaces.suneo import SuneoInterface, SuneoHandler
from interfaces.gigante import GiganteInterface, GiganteHandler
from interfaces.suneowhois import SuneoWhoisInterface, SuneoWhoisHandler

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
            ScansHandler,
            NobitaHandler,
            ShizukaV2Handler,
            SuneoHandler,
            GiganteHandler,
            SuneoWhoisHandler
        ]
        interfaces = [
            ScansInterface,
            NobitaInterface,
            ShizukaV2Interface,
            SuneoInterface,
            GiganteInterface,
            SuneoWhoisInterface
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
            # Bots
            n = app.handler.get('nobitaIf', 'nobita', setup=True)
            shi = app.handler.get('shizukaV2If', 'shizukaV2', setup=True)
            su = app.handler.get('suneoIf', 'suneo', setup=True)
            gi = app.handler.get('giganteIf', 'gigante', setup=True)
            sw = app.handler.get('suneowhoisIf', 'suneowhois', setup=True)
            # Get Scans of api
            type_bot, scans = g.get_scan()
            # TODO: El bot gigante tiene que conectarse con la api para guardar sus resultados
            #  suneowhois hay que ver como buscar en libreborme con lo obtenido mediante ipwhois

            for s in scans:
                if not s['done']:
                    if 'Nobita' in type_bot:
                        data = n.pscan(s['hosts'])
                        g.send_nobita(data)
                    if 'Shizuka' in type_bot:
                        data = shi.get_domain(s['hosts'])
                        g.send_shizuka(data)
                    if 'Suneo' in type_bot:
                        data = su.get_target(s['hosts'])
                        g.send_suneo(data)
                    if 'Gigante' in type_bot:
                        data = gi.check_ssh(s['hosts'])
                        # g.select_action(data)
                    if 'SuneoWhois' in type_bot:
                        # sw.get_target('185.59.67.186')
                        pass

                    data = s['id']
                    g.update_done(data)

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

