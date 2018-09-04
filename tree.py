
# coding: utf-8

# In[1]:


allnodes=[]
import weakref
class node:
    instances = []
    def __init__(self,name):
        self.__class__.instances.append(weakref.proxy(self))
        self.name = name
        self.children=[]
        self.parent=[]    


# In[2]:


def nodeparent(parent,children):
    parent.children.append(children)
#     children.parent.append(parent)


# In[3]:


def ifparent(parent,children):
    if children in parent.children:
        return True
    else:
        return False


# In[4]:


def ifchildren(parent,children):
    if parent in children.parent:
        return True
    else:
        return False


# In[5]:


A=node('A')
B=node('B')
C=node('C')


# In[6]:


nodeparent(A,B)
nodeparent(B,C)


# In[7]:


def todict(obj, classkey=None):
    if isinstance(obj, dict):
        data = {}
        for (k, v) in obj.items():
            data[k] = todict(v, classkey)
        return data
    elif hasattr(obj, "_ast"):
        return todict(obj._ast())
    elif hasattr(obj, "__iter__") and not isinstance(obj, str):
        return [todict(v, classkey) for v in obj]
    elif hasattr(obj, "__dict__"):
        print(obj.__dict__)
        data = dict([(key, todict(value, classkey)) 
            for key, value in obj.__dict__.items() 
            if not callable(value) and not key.startswith('_')])
        if classkey is not None and hasattr(obj, "__class__"):
            data[classkey] = obj.__class__.__name__
        return data
    else:
        return obj


# In[8]:


todict(A)


# In[ ]:


for i in node.instances:
    print(i.name)


# In[ ]:


x='sklearn.add.addr'
for i in x.split('.'):
    if i 

