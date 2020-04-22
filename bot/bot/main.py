from cement import App, TestApp, init_defaults, Interface, Handler
from cement.core.exc import CaughtSignal

from core.exc import BotError
from interfaces.startbot import ScansInterface, ScansHandler
from interfaces.nobita import NobitaInterface, NobitaHandler
from interfaces.shizukaV2 import ShizukaV2Interface, ShizukaV2Handler
from interfaces.suneoV2 import SuneoV2Interface, SuneoV2Handler
from interfaces.gigante import GiganteInterface, GiganteHandler
from interfaces.suneowhois import SuneoWhoisInterface, SuneoWhoisHandler

import datetime
import os
import socket

# configuration defaults
CONFIG = init_defaults('bot')


def get_ip(domain):
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror as e:
        print(e)
        return


class Bot(App):
    """Mi BOT App primary application."""

    class Meta:
        label = 'bot'

        # configuration dir
        dir = os.path.realpath('tokens.conf')
        config_files = [dir]

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
            SuneoV2Handler,
            GiganteHandler,
            SuneoWhoisHandler
        ]
        interfaces = [
            ScansInterface,
            NobitaInterface,
            ShizukaV2Interface,
            SuneoV2Interface,
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
            # Get Scans of api
            type_bot, scans = g.get_scan()
            # Bots
            n = app.handler.get('nobitaIf', 'nobita', setup=True)
            shi = app.handler.get('shizukaV2If', 'shizukaV2', setup=True)
            su = app.handler.get('suneoV2If', 'suneoV2', setup=True)
            gi = app.handler.get('giganteIf', 'gigante', setup=True)
            sw = app.handler.get('suneowhoisIf', 'suneowhois', setup=True)
            # TODO: El bot gigante tiene que conectarse con la api para guardar sus resultados
            #  suneowhois hay que ver como buscar en libreborme con lo obtenido mediante ipwhois
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            for s in scans:
                if s['executionTime'] < now and not s['done']:
                    for host in s['hosts']:
                        # Get the ip
                        ip = get_ip(host)
                        if 'Nobita' in type_bot:
                            app.log.info("BOT NOBITA")
                            data = n.pscan(host, ip)
                            app.log.info("Scanning completed")
                            g.send_nobita(data)
                        if 'Shizuka' in type_bot:
                            app.log.info("BOT SHIZUKA")
                            data = shi.get_domain(host, ip)
                            app.log.info("Scanning completed")
                            g.send_shizuka(data)
                        if 'Suneo' in type_bot:
                            app.log.info("BOT SUNEO")
                            data = su.get_cms(host, ip)
                            app.log.info("Scanning completed")
                            g.send_suneo(data)
                        if 'Gigante' in type_bot:
                            app.log.info("BOT GIGANTE")
                            data = gi.check_ssh(host)
                            app.log.info("Scanning completed")
                        if 'SuneoWhois' in type_bot:
                            sw.get_target(host)
                            pass
                    # Update done field in bots collection
                    data = s['id']
                    g.update_done(data)
                if s['done']:
                    app.log.info("The scan already done")

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
