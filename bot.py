#!/bin/python3
from twisted.internet import reactor
from quarry.net.proxy import DownstreamFactory, Bridge
import auth
import sys

token = sys.environ["TOKEN"]

class BotBridge(Bridge):
    def packet_upstream_player_position(self, buff):
        (x,y,z,onground) = buff.unpack("dddb")
        x = int(x*100)/100
        z = int(z*100)/100
        newpkt = buff.pack("dddb", x,y,z,onground)
        print((x*1000)%10,(z*1000)%10)
        self.upstream.send_packet("player_position", newpkt)

    def packet_upstream_player_position_and_look(self, buff):
        (x,y,z,yaw,pitch,onground) = buff.unpack("dddffb")
        x = int(x*100)/100
        z = int(z*100)/100
        print((x*1000)%10,(z*1000)%10)
        newpkt = buff.pack("dddffb", x,y,z,yaw,pitch,onground)
        self.upstream.send_packet("player_position_and_look", newpkt)

    def make_profile(self):
        return auth.make_profile(token)

class BotDownstreamFactory(DownstreamFactory):
    bridge_class = BotBridge
    motd = "Proxy Server"


def main(argv):
    # Parse options
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--listen-host", default="", help="address to listen on")
    parser.add_argument("-p", "--listen-port", default=25565, type=int, help="port to listen on")
    parser.add_argument("-b", "--connect-host", default="127.0.0.1", help="address to connect to")
    parser.add_argument("-q", "--connect-port", default=25565, type=int, help="port to connect to")
    args = parser.parse_args(argv)

    # Create factory
    factory = BotDownstreamFactory()
    factory.connect_host = args.connect_host
    factory.connect_port = args.connect_port

    # Listen
    factory.listen(args.listen_host, args.listen_port)
    reactor.run()


main(sys.argv[1:])
