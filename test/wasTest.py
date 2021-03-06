#!/usr/bin/env python


import os,re,sys
import unittest, uuid

from Tools.testing import *
from Tools.xpath import *
from Tools.parser import *
from Tools.pretty import *

import WebSphere

class WebSphere_Test(unittest.TestCase):
    """xmi module test"""

    def setUp(self):
        """called before each test"""
        setUp(self)
        return

    def tearDown(self):
        """called after each test"""
        return

    def test_01_SetupClasses(self):
        """build a WebSphere library with a set of classes."""
        tree = WebSphere.Tree()
        self.assertIsNotNone(tree)

        cell = WebSphere.Cell()
        cell.id = 'idCell'
        cell.name = 'myCell'
        self.assertIsNotNone(cell)
        tree.cells.append(cell)
        self.assertIn(cell,tree.cells)

        cluster = WebSphere.Cluster()
        cluster.id = 'idCluster'
        cluster.name = 'myCluster'
        self.assertIsNotNone(cluster)
        cell.clusters.append(cluster)
        self.assertIn(cluster,cell.clusters)

        node = WebSphere.Node()
        node.id = 'idNode'
        node.name = 'myNode'
        self.assertIsNotNone(node)
        cell.nodes.append(node)
        self.assertIn(node,cell.nodes)

        server = WebSphere.Server()
        server.id = 'idServer'
        server.name = 'myServer'
        self.assertIsNotNone(server)
        node.servers.append(server)
        self.assertIn(server,node.servers)

        member = WebSphere.Member()
        member.id = 'idMember'
        member.name = 'myMember'
        member.weight = 2
        self.assertIsNotNone(member)
        cluster.members.append(member)
        self.assertIn(member,cluster.members)

        vhost = WebSphere.VirtualHost()
        vhost.id = 'idVHost'
        vhost.name = 'myVHost'
        vhost.host = 'localhost'
        vhost.port = 1234
        self.assertIsNotNone(vhost)
        cell.virtualHosts.append(vhost)
        self.assertIn(vhost,cell.virtualHosts)

        prettyPrint(tree)

if __name__ == '__main__':
    unittest.main()
