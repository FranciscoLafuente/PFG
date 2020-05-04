from cement import App, TestApp, init_defaults, Interface, Handler
from cement.core.exc import CaughtSignal

from core.exc import BotError

from importlib import import_module
import datetime
from os import scandir
import os
import socket

# configuration defaults
CONFIG = init_defaults('bot')
RUTA = '/home/fran/Escritorio/Proyecto/PFG/bot/bot/interfaces/'
hand_list = []
if_list = []


def get_ip(domain):
    """ get the ip from the domain """
    try:
        ip = socket.gethostbyname(domain)
        return ip
    except socket.gaierror as e:
        print(e)
        return


def ls(ruta=RUTA):
    """ Get all bots in the interfaces directory """
    return [arch.name for arch in scandir(ruta) if arch.is_file()]


def do_imports():
    files = ls()
    for file in files:
        if '__init__' not in file:
            s = file.replace('.py', '')
            upper = s.title()
            first = 'interfaces.' + s
            handler = upper + 'Handler'
            interface = upper + 'Interface'
            # Dynamic import
            i = dynamic_import(first, interface)
            h = dynamic_import(first, handler)
            # Add to list
            hand_list.append(h)
            if_list.append(i)


def dynamic_import(abs_module_path, class_name):
    module_object = import_module(abs_module_path)

    target_class = getattr(module_object, class_name)

    return target_class


class Bot(App):
    """ Mi BOT App primary application. """

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

        # Register handlers and interfaces
        handlers = hand_list
        interfaces = if_list


class BotTest(TestApp, Bot):
    """A sub-class of Bot that is better suited for testing."""

    class Meta:
        label = 'bot'


def main():
    with Bot() as app:
        try:
            app.run()
            do_imports()
            for e in if_list:
                app.interface.define(e)
            for e in hand_list:
                app.handler.register(e)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Access to database
            c = app.handler.get('manageIf', 'manage', setup=True)
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
                        id_db = c.send_geo(data=data, id=s['id'], domain=host)
                        for tp in type_bot:
                            # Launch bot scan
                            app.log.info("BOT " + tp)
                            b = app.handler.get(tp + "If", tp, setup=True)
                            data = b.bot_scan(host, ip)
                            d = dict({tp: data})
                            app.log.info("Scanning completed")
                            list_to_send.append(d)
                            # Send especific data to create a new collection
                            c.send_bot(bot=tp, domain=host, data=data, id=id_db['id'])

                    # Send data to api
                    c.send_data(url='data', data=list_to_send, id=id_db['id'])
                    scan_id = s['id']
                    # Update done field in bots collection
                    #c.update_done(scan_id)

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
