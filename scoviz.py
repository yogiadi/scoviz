
# coding: utf-8

# In[ ]:


import inspect as ins
import sklearn as sk
import os
import glob
from os import walk


# In[ ]:


def basedir(filepath):
    li=filepath.split('/')
    del li[-1]
    bdir='/'.join(li)
    return bdir


# In[ ]:


def allrecfiles(dirpath,extfile=None):
    filenames = []
    for dirs , subdir , files in os.walk(dirpath):
        for name in files:
            filename = os.path.join(dirs,name)
            if extfile == None:
                filenames.append(filename)
            else:
                if filename.endswith(extfile):
                    filenames.append(filename)
    return filenames


# In[ ]:


def removeext(filename,extfile=None):
    li=filename.split(extfile)
    return li[0]


# In[ ]:


def bottompath(filename):
    li=filename.split('/')
    if li[-1] == '':
        return li[-2]
    else:
        return li[-1]


# In[ ]:


def dirdepth(dirpath):
    li=dirpath.split('/')
    if li[-1] == '':
        return len(li) - 1
    else:
        return len(li)


# In[ ]:


def baseroot(dirpath,dirpath1):
    dep=dirdepth(dirpath)
    arr=dirpath1.split('/')
    new_arr=[]
    for i in range(dep,len(arr)):
        new_arr.append(arr[i])
    return new_arr


# In[11]:


baseroot('/usr/local/lib/python3.6/dist-packages/','/usr/local/lib/python3.6/dist-packages/sklearn/multioutput')


# In[ ]:


def getselmem(obj,pred=None):
    li=[]
    for j in pred:
        li.append(ins.getmembers(obj,j))
    final_list=[]
    for i in li:
        for j in i:
            final_list.append(j)
    return final_list


# In[ ]:
import os
import networkx as nx
path = '/usr/local/lib/python3.6/dist-packages/sklearn/'
base_name = '/usr/local/lib/python3.6/dist-packages'
G1 = nx.DiGraph()
root = os.path.basename(path)
G1.add_node(root)
for dirpath, dirname, filenames in os.walk(path):
    #print(dirpath)
    if os.path.basename(dirpath) == '__pycache__':
        continue
    if '__pycache__' in dirname:
        dirname.remove('__pycache__')
    for dirs in dirname:
        G1.add_node(dirs)
        G1.add_edge(root, dirs, weight=1)
    t = baseroot(base_name, dirpath)
#     print(t)
    import_str = '.'.join([x for x in t if x != ''])
    print(import_str)
    for file in filenames:
        file = removeext(file, '.')
        G1.add_node(file)
        if len(import_str) != 0:
          exec('import '+ import_str)
        G1.add_edge(root, file, weight=0.5)
        
    root = os.path.basename(dirpath)


def main(allfiles):
    di={}
    for i in allfiles:
        i=removeext(i,'.py')
        li=baseroot('/usr/local/lib/python3.6/dist-packages/',i)
        importstr=('.').join(li)
        str1= 'import ' + importstr 
        str2='di[\'' + importstr + '\']=getselmem(' + importstr +  ',[ins.isfunction,ins.ismethod,ins.isclass])'
        try:
            exec(str1)
            exec(str2)
        except:
            pass
    return di


# In[ ]:


allfiles=allrecfiles('/usr/local/lib/python3.6/dist-packages/sklearn/','.py')


# In[15]:


t=main(allfiles)
print(t)


# In[ ]:


class node:
    def __init__(self, key, name=None):
        self.key = key
        self.name = ('Dummy_node' if not name else name)
        
    def __str__(self):
        return self.key
        


# In[17]:


import networkx as nx
# from graphviz import Digraph
G = nx.DiGraph()
# G = Digraph()
for i in t.keys():
    #node_num = 0
    G.add_node(i)
    j=t[i]
    for k in j:
        G.add_node(ins.getmodule(k[1]).__name__ + '.' + k[0])
        print(f"node_name={ k[0]}, and type={type(ins.getmodule(k[1]).__name__ + '.' + k[0])}")
        if i == ins.getmodule(k[1]).__name__ :
            G.add_edge(i,ins.getmodule(k[1]).__name__ + '.' + k[0], weight=1)
        else:
            G.add_edge(ins.getmodule(k[1]).__name__ + '.' + k[0],i, weight=1)
    #G = nx.relabel.convert_node_labels_to_integers(G)


# In[ ]:


import matplotlib.pyplot as plt


# In[ ]:


def sub_graph(node,G):
    li=[]
    for j in G.predecessors(node):
        li.append(j)
    for j in G.successors(node):
        li.append(j)
    li.append(node)
    return G.subgraph(li)


# In[22]:


#plt.subplot(121)
# nx.draw_shell(sub_graph('sklearn.cross_decomposition.pls_',G), with_labels=True, font_weight='bold')
nx.node_link_data(sub_graph('sklearn.cross_decomposition.pls_',G))


# In[ ]:


# !pip install nxviz


# In[ ]:


# type(nx.node_link_data(sub_graph('sklearn.cross_decomposition.pls_',G)))
import json
# json.dump(nx.node_link_data(sub_graph('sklearn.cross_decomposition.pls_',G)))
Gsub=sub_graph('sklearn.cross_decomposition.pls_',G)
for n in Gsub:
    Gsub.nodes[n]['name'] = n
from networkx.readwrite import json_graph
d = json_graph.node_link_data(Gsub)


# In[ ]:


from networkx import convert_node_labels_to_integers
Gsub=sub_graph('sklearn.cross_decomposition.pls_',G)
Glab=convert_node_labels_to_integers(Gsub)


# In[ ]:


from networkx.readwrite import json_graph
d = json_graph.node_link_data(Glab)


# In[36]:


d


# In[ ]:


json.dump(d, open('force.json', 'w'))
# !ls
from google.colab import files
files.download('force.json')


# In[22]:


# list(G.predecessors('sklearn.cross_decomposition.pls_'))
s = sub_graph('sklearn.cross_decomposition.pls_',G)
pos = nx.drawing.spring_layout(s, scale=3300)
print(pos)
# print(G.nodes())
# plt.subplot(111)
# nx.draw(s,pos, with_labels=True,node_size = 15, node_color='#A0CBE2')
plt.subplot(122)
nx.draw_shell(s,with_labels=True, alpha=0.8, font_size=7)
plt.show()


# # New Section

# In[23]:


get_ipython().system('pip install bokeh')


# In[26]:


from bokeh.io import show, output_notebook
from bokeh.plotting import figure

output_notebook()
from bokeh.models.graphs import from_networkx
from bokeh.models import Range1d, Plot
from bokeh.models.graphs import NodesAndLinkedEdges
from bokeh.models import Circle, HoverTool, MultiLine

plot = Plot(x_range=Range1d(-1.1,1.1), y_range=Range1d(-1.1,1.1))

# graph = from_networkx(G, nx.spring_layout, scale=2, center=(0,0))
graph = from_networkx(sub_graph('sklearn.cross_decomposition.pls_',G), nx.spring_layout, scale=3, center=(0,0))
plot.renderers.append(graph)


# Blue circles for nodes, and light grey lines for edges
graph.node_renderer.glyph = Circle(size=25, fill_color='#2b83ba')
graph.edge_renderer.glyph = MultiLine(line_color="#cccccc", line_alpha=0.8, line_width=2)

# green hover for both nodes and edges
graph.node_renderer.hover_glyph = Circle(size=25, fill_color='#abdda4')
graph.edge_renderer.hover_glyph = MultiLine(line_color='#abdda4', line_width=4)

# When we hover over nodes, highlight adjecent edges too
graph.inspection_policy = NodesAndLinkedEdges()

plot.add_tools(HoverTool(tooltips=None))

show(plot)

