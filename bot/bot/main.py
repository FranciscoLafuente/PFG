from cement import App, TestApp, init_defaults, Interface, Handler
from cement.core.exc import CaughtSignal

from core.exc import BotError
from interfaces.manage import ManageHandler, ManageInterface

from importlib import import_module
import datetime
from os import scandir
import os
import socket
import pika
import json
import time

# configuration defaults
CONFIG = init_defaults('bot')
RUTA = '/home/fran/Escritorio/Proyecto/PFG/bot/bot/interfaces/'
host_queue = 'localhost'
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
        if '__init__' not in file and 'manage' not in file:
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


def launch_scan(app, type_bots, scan):
    scan = json.loads(scan)
    # Start geolocation handler
    now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    geo = app.handler.get('geoIf', 'geo', setup=True)

    scan_list = []
    if not scan['launch']:
        app.log.info("The scan already done")
        return None
    elif scan['executionTime'] < now and scan['launch']:
        for host in scan['hosts']:
            results = []
            # Get the ip
            ip = get_ip(host)
            # Save data geolocation
            geo_data = geo.get_geo(ip, host)
            for tp in type_bots:
                # Launch bot scan
                app.log.info("BOT " + tp)
                b = app.handler.get(tp + "If", tp, setup=True)
                bot_data = b.bot_scan(host, ip)
                d = dict({tp: bot_data})
                app.log.info("Scanning completed")
                results.append(d)

            # All data in object for send
            scan_finished = geo_data
            scan_finished['results'] = results
            scan_list.append(scan_finished)
        return scan_list


def start_consumer(app, manage, type_bots):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=host_queue))
    channel = connection.channel()

    channel.queue_declare(queue='task_queue', durable=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        data = launch_scan(app, type_bots, body)
        if not data:
            return
        # Send data to api
        scan = json.loads(body)
        manage.send_data(url='data', data=data, id=scan['id'])
        # Update done field in bots collection
        manage.update_done(scan['id'])
        ch.basic_ack(delivery_tag=method.delivery_tag)

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='task_queue', on_message_callback=callback)

    channel.start_consuming()


class Bot(App):
    """ Mi BOT App primary application. """

    class Meta:
        label = 'bot'
        plugin_dirs = ['./plugins']

        # configuration dir
        dir = os.path.realpath('properties.conf')
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
        handlers = [ManageHandler] + hand_list
        interfaces = [ManageInterface] + if_list


class BotTest(TestApp, Bot):
    """A sub-class of Bot that is better suited for testing."""

    class Meta:
        label = 'bot'


def main():
    with Bot() as app:
        try:
            app.run()
            # Create the handler that it will make the calls to api
            manage = app.handler.get('manageIf', 'manage', setup=True)
            # Load all bots and scans and then do imports in the interface dir
            type_bots, scans = manage.get_scan()
            x = 1
            n_bots = len(type_bots)
            for bot in type_bots:
                app.log.info("Downloading %d of %d files" % (x, n_bots))
                manage.download_files(type_bot=bot)
                app.log.info("File %d downloaded" % x)
                x += 1
            do_imports()
            for e in if_list:
                app.interface.define(e)
            for e in hand_list:
                app.handler.register(e)

            # ---- Start consumer ----
            start_consumer(app, manage, type_bots)

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
