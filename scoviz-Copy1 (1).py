
# coding: utf-8

# In[2]:


import inspect as ins
import sklearn as sk
import os
import glob
from os import walk
from networkx.readwrite import json_graph


# In[3]:


class node:
    def __init__(self,name):
        self.name = name
        self.children=[]
        self.parent=[]


# In[4]:


def nodeparent(parent,children):
    parent.children.append(children)
    children.parent.append(parent)


# In[5]:


def ifchildren(parent,children):
    if parent in children.parent:
        return True
    else:
        return False


# In[6]:


def ifparent(parent,children):
    if children in parent.children:
        return True
    else:
        return False


# In[7]:


def basedir(filepath):
    li=filepath.split('\\')
    del li[-1]
    bdir='\\'.join(li)
    return bdir


# In[8]:


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


# In[9]:


def removeext(filename,extfile=None):
    li=filename.split(extfile)
    return li[0]


# In[10]:


def bottompath(filename):
    li=filename.split('\\')
    if li[-1] == '':
        return li[-2]
    else:
        return li[-1]


# In[11]:


def dirdepth(dirpath):
    li=dirpath.split('\\')
    if li[-1] == '':
        return len(li) - 1
    else:
        return len(li)


# In[12]:


def baseroot(dirpath,dirpath1):
    dep=dirdepth(dirpath)
    arr=dirpath1.split('\\')
    new_arr=[]
    for i in range(dep,len(arr)):
        new_arr.append(arr[i])
    return new_arr


# In[13]:


baseroot('F:\\Anaconda\\Lib\\site-packages\\sklearn','F:\\Anaconda\\Lib\\site-packages\\sklearn\\multioutput')


# In[14]:


def getselmem(obj,pred=None):
    li=[]
    for j in pred:
        li.append(ins.getmembers(obj,j))
    final_list=[]
    for i in li:
        for j in i:
            final_list.append(j)
    return final_list


# In[15]:


def main(allfiles):
    di={}
    for i in allfiles:
        i=removeext(i,'.py')
        li=baseroot('F:\\Anaconda\\Lib\\site-packages',i)
        importstr=('.').join(li)
        str1= 'import ' + importstr 
        str2='di[\'' + importstr + '\']=getselmem(' + importstr +  ',[ins.isfunction,ins.ismethod,ins.isclass])'
        try:
            exec(str1)
            exec(str2)
        except:
            pass
    return di


# In[16]:


allfiles=allrecfiles('F:\\Anaconda\\Lib\\site-packages\\sklearn\\','.py')
# allrecfiles('F:\\Anaconda\\Lib\\site-packages\\sklearn\\','.py')


# In[19]:


# t=main(allfiles)
# print(t)
for i in t:
    print(i)


# In[49]:


for i in t.keys():
    x=i.split('.')
    if x[0] not in di['start']:
        dii={}
        dii[str(x[0])]=[]
        di['start'].append(dii)
    break
#     if x[1] not in di['start'][str(x[0])]:
#         di['start'][x[0]].append(str(x[1]))        


# In[53]:


def walk(node):
    """ iterate tree in pre-order depth-first search order """
    yield node
    for child in node.children:
        for n in walk(child):
            yield n


# In[54]:





# In[ ]:


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
        if i == ins.getmodule(k[1]).__name__ :
            G.add_edge(i,ins.getmodule(k[1]).__name__ + '.' + k[0])
        else:
            G.add_edge(ins.getmodule(k[1]).__name__ + '.' + k[0],i)
    #G = nx.relabel.convert_node_labels_to_integers(G)


# In[ ]:


json_graph.node_link_data(G)


# In[ ]:


def sub_graph(node,G):
    li=[]
    for j in G.predecessors(node):
        li.append(j)
    for j in G.successors(node):
        li.append(j)
    li.append(node)
    return G.subgraph(li)


# In[ ]:


Gsub=sub_graph('sklearn.naive_bayes',G)


# In[ ]:


H = nx.DiGraph()
H = Gsub.copy()   


# In[ ]:


for n in Gsub:
    arr = n.split('.')
    for i in range(len(arr)-1):
        H.add_node(arr[i])
    for i in range(len(arr)-1):
        if i != len(arr) - 2:
            H.add_edge(arr[i],arr[i+1])
        else:
            H.add_edge(arr[i],n)


# In[ ]:


for n in H:
    print(n)
    H.nodes[n]['name'] = n.split('.')[-1]
    print(H.nodes[n]['name'])


# In[ ]:


# type(nx.node_link_data(sub_graph('sklearn.cross_decomposition.pls_',G)))
# import json
# # json.dump(nx.node_link_data(sub_graph('sklearn.cross_decomposition.pls_',G)))
# # Gsub=sub_graph('sklearn.cross_decomposition.pls_',G)
# # for n in Gsub:
# #     Gsub.nodes[n]['name'] = n
# from networkx.readwrite import json_graph
for h in H:
    print(H.nodes[h]['name'])


# In[ ]:


# from networkx import convert_node_labels_to_integers
# Gsub=sub_graph('sklearn.cross_decomposition.pls_',G)
Glab=convert_node_labels_to_integers(H)
for i in Glab:
    print(i)


# In[ ]:


# from networkx.readwrite import json_graph
d=json_graph.node_link_data(Glab)


# In[ ]:


d


# In[ ]:


json.dump(d, open('force.json', 'w'))
# from google.colab import files
# files.download('force.json')


# # New Section

# In[ ]:


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

