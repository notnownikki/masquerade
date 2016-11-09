import threading
from crosshair import plugins
from crosshair import commands
from masquerade import configuration
from masquerade import dnsmasq


class MapCommand(commands.Command):
    lock = threading.Lock()

    def setup_parser(self):
        self.parser.add_argument(
            '--name', help='FQDN to map', required=True)
        self.parser.add_argument(
            '--ip', help='IP address to map to', required=True)

    def execute(self, channel):
        hosts_map = {}
        hosts_map_filename = configuration.get('hosts_map_filename')
        for line in open(hosts_map_filename, 'r').readlines():
            ip, name = line.strip().split(' ')
            hosts_map[name] = ip
        hosts_map[self.args.name] = self.args.ip
        try:
            self.lock.acquire()
            with open(hosts_map_filename, 'w') as hosts_file:
                for name in hosts_map:
                    hosts_file.write('%s %s\n' % (hosts_map[name], name))
            dnsmasq.send_sighup()
        finally:
            self.lock.release()
        channel.send('SUCCESS\n')


plugins.register_command_handler('map', MapCommand)
