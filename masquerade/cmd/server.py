import argparse
import os
from crosshair import ssh
from crosshair import plugins
from masquerade import configuration


def main():
    parser = argparse.ArgumentParser(description='Additional hosts manager for dnsmasq')
    parser.add_argument('--addn-hosts', default='/etc/hosts.dnsmasq')
    parser.add_argument('--address', default='0.0.0.0')
    parser.add_argument('--port', default=9045, type=int)
    parser.add_argument('--keyspath', default='.')
    args = parser.parse_args()
    plugins.load('crosshair.commands')
    plugins.load('masquerade.commands')
    configuration['hosts_map_filename'] = args.addn_hosts
    server = ssh.SSHServer(
        host_key_fname = os.path.join(args.keyspath, 'host.key'),
        public_keys_path = os.path.join(args.keyspath, 'public_keys/'),
        address = (args.address, args.port))
    server.serve_forever()
