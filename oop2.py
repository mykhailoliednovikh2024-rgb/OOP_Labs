import random
import asyncio
import time
import networkx as nx
import matplotlib.pyplot as plt

# 1
class Node:
    def __init__(self, name):
        self.name = name
        self.connections = []

    def connect(self, other_node):
        if other_node not in self.connections:
            self.connections.append(other_node)

    def show_con(self):
        print(f"{self.name} connected to: ", end="")
        for node in self.connections:
            print(node.name, end=" ")
        print()

class StarTopology:
    def __init__(self, hub_name):
        self.hub = Node(hub_name)
        self.nodes = []

    def add_node(self, name):
        node = Node(name)
        self.nodes.append(node)
        node.connect(self.hub)
        self.hub.connect(node)

    def show_network(self):
        print("Hub connections:")
        self.hub.show_con()

# 2
class RingTopology:
    def __init__(self):
        self.nodes = []

    def add_node(self, name):
        new_node = Node(name)
        if self.nodes:
            last_node = self.nodes[-1]
            last_node.connect(new_node)
            new_node.connect(last_node)
        self.nodes.append(new_node)

    def close_ring(self):
        if len(self.nodes) > 1:
            first = self.nodes[0]
            last = self.nodes[-1]
            last.connect(first)
            first.connect(last)

    def show_network(self):
        for node in self.nodes:
            node.show_con()

# 3 (Packet definition)
class Packet:
    def __init__(self, src, dest, size, protocol):
        self.src = src
        self.dest = dest
        self.size = size
        self.protocol = protocol
        self.visited = []

# 4
class UnstablePacket(Packet):
    def send_packet(self):
        if random.random() > 0.9:
            print("Packet lost!")
        else:
            print(f"Packet sent from {self.src.name} to {self.dest.name}")
            self.dest.receive_packet(self.size)

# 5
class TCPProtocol:
    name = "TCP"
    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(200, 500), "TCP")
        await src.send(packet, network)

class UDPProtocol:
    name = "UDP"
    @staticmethod
    async def transmit(src, dest, network):
        packet = Packet(src, dest, random.randint(50, 200), "UDP")
        await src.send(packet, network)

# 6
class Network:
    def __init__(self):
        self.nodes = []
        self.loss_rate = random.uniform(0.10, 0.15)
        self.packets_sent = 0
        self.packets_lost = 0
        self.total_time = 0

    async def simulate(self, protocol, packets=5):
        print(f"\n--- Protocol: {protocol.name} ---")
        for _ in range(packets):
            src, dest = random.sample(self.nodes, 2)
            start = time.time()
            self.packets_sent += 1
            await protocol.transmit(src, dest, self)
            self.total_time += time.time() - start

    def analyze(self):
        if self.packets_sent == 0:
            return
        avg_time = self.total_time / self.packets_sent
        loss_percent = (self.packets_lost / self.packets_sent) * 100
        successful_packets = self.packets_sent - self.packets_lost
        bandwidth = successful_packets / self.total_time if self.total_time > 0 else 0
        print("\n--- Statistics ---")
        print(f"Avg Latency: {avg_time:.4f} s")
        print(f"Loss Rate: {loss_percent:.2f}%")
        print(f"Throughput: {bandwidth:.2f} pkt/s")

    def visualize(self, title="Network Topology"):
        G = nx.Graph()
        for node in self.nodes:
            for conn in node.connections:
                G.add_edge(node.name, conn.name)
        plt.figure(figsize=(8, 6))
        nx.draw(G, with_labels=True, node_color="green", 
                node_size=2000, font_size=12, font_weight="bold")
        plt.title(title)
        plt.show()

# 7
async def send(self, packet, network):
    await asyncio.sleep(random.uniform(0.05, 0.2))  
    if random.random() < network.loss_rate:
        network.packets_lost += 1
        print("Packet lost!")
        return
    await self.forward(packet, network)

async def forward(self, packet, network):
    if self == packet.dest:
        print(f"{self.name} received packet!")
        return
    if self in packet.visited:
        return
    packet.visited.append(self)
    for node in self.connections:
        await node.send(packet, network)

Node.send = send
Node.forward = forward

# 8 
async def main():
    net = Network()
    hub = Node("HUB")
    nodes = [Node(f"N{i}") for i in range(1, 5)]
    net.nodes = [hub] + nodes
    
    for n in nodes:
        hub.connect(n)
        n.connect(hub)

    await net.simulate(TCPProtocol, packets=10)
    net.analyze()
    net.visualize("Star Topology")

if __name__ == "__main__":
    asyncio.run(main())