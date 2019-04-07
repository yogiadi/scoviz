ls = ['one.two.three.four', 'one.six.seven.eight', 'five.nine.ten', 'twelve.zero','thirty.one','one.two.three.five','one.two.three.six']
#ls = ['one.two.three', 'one.six.seven']
tree = {}

for item in ls:
    t = tree
    sum=0
    for part in item.split('.'):
        if sum == len(item.split('.')) - 1:
            t = t.setdefault(part, {})
        else:    
            t = t.setdefault('subgraph cluster_'+str(sum)+'_'+part+'{label="'+part+'"', {}) 
        sum = sum + 1
print ('digraph G ' + str(tree).replace(': {\'',' ').replace('{}',' ').replace(':',' ').replace('\'',' ').replace(',',';'))
