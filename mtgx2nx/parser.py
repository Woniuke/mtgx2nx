import os
import xml.etree.cElementTree as ElementTree
import zipfile

import networkx as nx


class Maltego:
    def __init__(self, file_path):
        self.entities = dict()
        self.graph = list()
        self.mtgx_info = dict()
        self.__parser_mtgx(file_path)

    def __get_entity(self, xml_entity):
        name = xml_entity.attrib['id']
        entity = {
            'attrib': xml_entity.attrib,
            'fields': list()
        }
        for field in xml_entity.find('Properties').find('Fields'):
            field_info = field.attrib.copy()
            default_value = field.find('DefaultValue')
            if default_value:
                field_info['default_value'] = default_value.text
            sample_value = field.find('SampleValue')
            if sample_value:
                field_info['sample_value'] = sample_value.text
            entity['fields'].append(field_info)
        self.entities[name] = entity

    @staticmethod
    def __get_graph(xml_entity):

        def parser_node(node_xml):
            mtg_ns = 'http://maltego.paterva.com/xml/mtgx'
            node_id = node_xml.attrib['id']
            node = dict()
            for data in node_xml:
                maltego_entity = data.find(f'{{{mtg_ns}}}MaltegoEntity')
                if maltego_entity:
                    node['maltego_entity_type'] = maltego_entity.attrib['type']
                    for field in maltego_entity.find(f'{{{mtg_ns}}}Properties'):
                        name = field.attrib['name']
                        node[name] = field.find(f'{{{mtg_ns}}}Value').text
                    break
                else:
                    continue
            return node_id, node

        def parser_edge(edge_xml):
            mtg_ns = 'http://maltego.paterva.com/xml/mtgx'
            source = edge_xml.attrib['source']
            target = edge_xml.attrib['target']
            edge = dict()
            for data in edge_xml:
                maltego_entity = data.find(f'{{{mtg_ns}}}MaltegoLink')
                if maltego_entity:
                    edge['type'] = maltego_entity.attrib['type']
                    for field in maltego_entity.find(f'{{{mtg_ns}}}Properties'):
                        name = field.attrib['name']
                        edge[name] = field.find(f'{{{mtg_ns}}}Value').text
                    break
                else:
                    continue
            return source, target, edge

        graph_ns = 'http://graphml.graphdrawing.org/xmlns'
        graph = xml_entity.find(f'{{{graph_ns}}}graph')
        if 'edgedefault' in graph.attrib:
            graph_type = graph.attrib['edgedefault']
        else:
            graph_type = 'directed'
        if graph_type == 'directed':
            nx_graph = nx.MultiDiGraph()
        else:
            nx_graph = nx.MultiGraph()

        nodes = graph.findall(f'{{{graph_ns}}}node')
        edges = graph.findall(f'{{{graph_ns}}}edge')

        nx_graph.add_nodes_from(list(map(parser_node, nodes)))
        nx_graph.add_edges_from(list(map(parser_edge, edges)))

        return nx_graph

    @staticmethod
    def __get_properties_info(version_file):
        info = dict()
        for line in version_file.splitlines():
            if line[0] != '#':
                k, v = line.split('=')
                info[k] = v
        return info

    def __parser_mtgx(self, file_path):
        zip_handler = zipfile.ZipFile(file_path)
        for file in zip_handler.filelist:
            filename = file.filename
            if filename == 'version.properties':
                self.mtgx_info.update(self.__get_properties_info(zip_handler.read(filename).decode('utf-8')))
            elif filename[:6] == 'Graphs':
                name = os.path.split(filename)[-1]
                fname, ext = os.path.splitext(name)
                if ext == '.graphml':
                    properties = self.__get_properties_info(
                        zip_handler.read(f'Graphs/{fname}.properties').decode('utf-8'))
                    graph = self.__get_graph(
                        ElementTree.fromstring(zip_handler.read(f'Graphs/{fname}.graphml').decode('utf-8'))
                    )
                    self.graph.append({
                        'properties': properties,
                        'graph': graph
                    })
            elif filename[:8] == 'Entities':
                self.__get_entity(
                    ElementTree.fromstring(zip_handler.read(filename).decode('utf-8'))
                )
            else:
                continue
