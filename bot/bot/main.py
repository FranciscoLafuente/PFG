from cement import App, TestApp, init_defaults, Interface, Handler
from cement.core.exc import CaughtSignal

from core.exc import BotError
from interfaces.startbot import ScansInterface, ScansHandler
from interfaces.geo import GeoInterface, GeoHandler
from interfaces.nobita import NobitaInterface, NobitaHandler
from interfaces.shizuka import ShizukaInterface, ShizukaHandler
from interfaces.suneo import SuneoInterface, SuneoHandler
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

        # Funcion que llame al back para recuperar los handlers y los interfaces

        # register handlers
        handlers = [
            ScansHandler,
            GeoHandler,
            NobitaHandler,
            ShizukaHandler,
            SuneoHandler,
            GiganteHandler,
            SuneoWhoisHandler
        ]
        interfaces = [
            ScansInterface,
            GeoInterface,
            NobitaInterface,
            ShizukaInterface,
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
            # To compare dates
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Access to database
            c = app.handler.get('connectApiIf', 'connectApi', setup=True)
            # Get Scans of api
            type_bot, scans = c.get_scan()
            # Geo handler
            geo = app.handler.get('geoIf', 'geo', setup=True)

            for s in scans:
                list_to_send = []
                if s['executionTime'] < now and not s['done']:
                    for host in s['hosts']:
                        # Get the ip
                        ip = get_ip(host)
                        # Save data geo
                        data = geo.get_geo(ip, host)
                        list_to_send.append(data)
                        for tp in type_bot:
                            # Launch bot scan
                            app.log.info("BOT " + tp)
                            b = app.handler.get(tp + "If", tp, setup=True)
                            data = b.bot_scan(host, ip)
                            app.log.info("Scanning completed")
                            list_to_send.append(data)

                    # Send data to api
                    c.send_data(data=list_to_send, id=s['id'], domain=host)
                    data = s['id']
                    # Update done field in bots collection
                    c.update_done(data)

                elif s['done']:
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
