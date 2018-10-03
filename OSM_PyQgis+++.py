path = 'C:/Users/tk46/Documents/GIS/output/'
region = 'tohoku'

nodeFile = open('%s%soutput_nodes.csv' % (path, region), 'w')
nodeFile.write('nodeId,x,y,layer\n')

linkFile = open('%s%soutput_links.csv' % (path, region), 'w')
linkFile.write('nodeIdOrg,nodeIdDest,distance,highway,oneway,bridge,tunnel\n')

l = iface.activeLayer()
feats = l.getFeatures()

nodes = {}
nodeIdCount = 0
links = []

da = QgsDistanceArea()
da.setEllipsoid('WGS84')

for feat in feats:
    geom = feat.geometry()
    vertIter = geom.vertices()
    
    layer = feat['layer']
    
    #add nodes
    vert1 = vertIter.next()
    node1 = (vert1.x(), vert1.y(), layer)
    
    if node1 in nodes:
        nodeId1 = nodes[node1]
    else:
        nodes[node1] = nodeIdCount
        nodeId1 = nodeIdCount
        nodeIdCount += 1
        
        nodeFile.write('%d,%f,%f,%i\n' % (nodeId1, vert1.x(), vert1.y(), layer))
    
    while vertIter.hasNext():
        vert2 = vertIter.next()
        node2 = (vert2.x(), vert2.y(), layer)
        
        if node2 in nodes:
            nodeId2 = nodes[node2]
        else:
            nodes[node2] = nodeIdCount
            nodeId2 = nodeIdCount
            nodeIdCount += 1
            
            nodeFile.write('%d,%f,%f,%i\n' % (nodeId2, vert2.x(), vert2.y(), layer))
        
        #add links
        link = (nodeId1, nodeId2)
        
        if link not in links:
            pt1 = QgsPointXY(node1[0], node1[1])
            pt2 = QgsPointXY(node2[0], node2[1])
            
            dist = da.measureLine([pt1, pt2])
            
            if feat['fclass']:
                fclass = feat['fclass']
            else:
                fclass = ''
            
            if feat['oneway']:
                oneway = feat['oneway']
            else:
                oneway = ''
            
            if feat['bridge']:
                bridge = feat['bridge']
            else:
                bridge = ''
                
            if feat['tunnel']:
                tunnel = feat['tunnel']
            else:
                tunnel = ''
            
            linkFile.write('%d,%d,%f,%s,%s,%s,%s\n' % (nodeId1, nodeId2, dist, fclass, oneway, bridge, tunnel))
            links.append(link)
        
        node1 = node2
        nodeId1 = nodeId2
        

nodeFile.close()
linkFile.close()