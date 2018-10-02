path = r'C:\Users\tk46\Documents\GIS\output\\'
region = 'tohoku'

layer = iface.activeLayer()
feats = layer.getFeatures()

nodes = {}
nodeIdCount = 0
links = {}

for feat in feats:
    geom = feat.geometry()
    vertIter = geom.vertices()
    
    vert1 = vertIter.next()
    node1 = (vert1.x(), vert1.y())
    
    if node1 in nodes:
        nodeId1 = nodes[node1]
    else:
        nodes[node1] = nodeIdCount
        nodeId1 = nodeIdCount
        nodeIdCount += 1
    
    while vertIter.hasNext():
        vert2 = vertIter.next()
        node2 = (vert2.x(), vert2.y())
        
        if node2 in nodes:
            nodeId2 = nodes[node2]
        else:
            nodes[node2] = nodeIdCount
            nodeId2 = nodeIdCount
            nodeIdCount += 1
        
        link = (nodeId1, nodeId2)
        
        if link in links:
            print('error')
        else:
            linkInfo = {}
            
            dist = QgsDistanceArea()
            dist.setEllipsoid('WGS84')
            pt1 = QgsPointXY(node1[0], node1[1])
            pt2 = QgsPointXY(node2[0], node2[1])
            
            linkInfo['distance'] = dist.measureLine([pt1, pt2])
            
            if feat['fclass']:
                linkInfo['fclass'] = feat['fclass']
            else:
                linkInfo['fclass'] = ''
            
            if feat['oneway']:
                linkInfo['oneway'] = feat['oneway']
            else:
                linkInfo['oneway'] = ''
            
            if feat['bridge']:
                linkInfo['bridge'] = feat['bridge']
            else:
                linkInfo['bridge'] = ''
                
            links[link] = linkInfo
        
        node1 = node2
        nodeId1 = nodeId2
        
nodeFile = open('%s%soutput_nodes.csv' % (path, region), 'w')

nodeFile.write('nodeId,x,y\n')
for (x, y), nodeId in nodes.items():
    nodeFile.write('%d,%f,%f\n' % (nodeId, x, y))

nodeFile.close()

linkFile = open('%s%soutput_links.csv' % (path, region), 'w')
linkFile.write('nodeIdOrg,nodeIdDest,distance,highway,oneway,bridge\n')
for (nodeId1, nodeId2), linkInfo in links.items():
    dist = linkInfo['distance']
    fclass = linkInfo['fclass']
    oneway = linkInfo['oneway']
    bridge = linkInfo['bridge']
    linkFile.write('%d,%d,%f,%s,%s,%s\n' % (nodeId1, nodeId2, dist, fclass, oneway, bridge))

linkFile.close()