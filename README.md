# mtgx2nx

## Introduction

**[Maltego](https://www.maltego.com/)** is a powerful intelligence analysis tool. but sometimes, It looks like a galaxy when you have a graph contains millions of nodes and vertices. It's very difficult to analysis complex graph directly.  
**mtgx2nx** can transform mtgx file to networkx graph. **[networkx](https://networkx.org/)** is famous python package for complex network analysis.

Github: https://github.com/Woniuke/mtgx2nx

## Install
```
$ python setup.py install
```
or
```
pip install mtgx2nx
```

## Usage
This is example.  
mtgx_info / entities / graph
```python
>>> import mtgx2nx
>>> my_graph = mtgx2nx.Maltego('MyGraph.mtgx')

# Basic information of mtgx file.
>>> print(my_graph.mtgx_info)
{
    'maltego.mtz.version': '1.0', 
    'maltego.client.subtitle': '', 
    'maltego.client.version': '4.1.13.11516', 
    'maltego.pandora.version': '1.4.2', 
    'maltego.graph.version': '1.0', 
    'maltego.client.name': 'Maltego Community Edition'
}

# dict for entity info, node data struct.
>>> for entity in my_graph.entities:
    print(entity)
    
maltego.URL
maltego.X509Certificate
maltego.Domain
maltego.Phrase
maltego.Hash

# get details.
>>>my_graph.entities['maltego.URL']
{
 'attrib': # entity info
     {'id': 'maltego.URL', 
      'displayName': 'URL', 
      'displayNamePlural': 'URLs', 
      'description': 'An internet Uniform Resource Locator (URL)', 
      'category': 'Infrastructure', 
      'smallIconResource': 'URL', 
      'largeIconResource': 'URL', 
      'allowedRoot': 'true', 
      'conversionOrder': '90', 
      'visible': 'true'}, 
 'fields': [ # entity fields
     {'name': 'short-title', 'type': 'string', 'nullable': 'true', 'hidden': 'false', 'readonly': 'false', 'description': '', 'displayName': 'Short title'}, 
     {'name': 'url', 'type': 'url', 'nullable': 'true', 'hidden': 'false', 'readonly': 'false', 'description': '', 'displayName': 'URL'}, 
     {'name': 'title', 'type': 'string', 'nullable': 'true', 'hidden': 'false', 'readonly': 'false', 'description': '', 'displayName': 'Title'}
    ]
}

# list for graph in mtgx file, one mtgx file can contains one more graph.
>>> len(my_graph.graph)
1

>>> my_graph.graph[0]
{ 
'properties': { # properties
    'modified': '2021-10-15 17\\:23\\:13.734 +0800', 
    'author': '', 
    'created': '2020-12-28 10\\:21\\:14.260 +0800'}, 
'graph': # networkx MultiDiGraph
    <networkx.classes.multidigraph.MultiDiGraph object at 0x00000165CE533730>
}

>>> graph = my_graph.graph[0]['graph']

>>> graph.nodes['n0']
{ 
    'maltego_entity_type': 'maltego.URL', # maltego_entity_type, match in entities
    'short-title': None,                  # other fields seen in entity details.
    'url': 'http://www.test.com', 
    'title': None
}

```
