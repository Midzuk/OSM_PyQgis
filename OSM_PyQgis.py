layer = iface.activeLayer()
feats = layer.getFeatures()

nodes = {}
nodeIdCount = 0
links = {}
#linkIdCount = 0
#linkInfo = {}
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
            
            #line = QgsGeometry.fromPolyline([vert1, vert2])
            #dist = line.length()
            dist = QgsDistanceArea()
            dist.setEllipsoid('WGS84')
            #dist.ellipsoid()
            pt1 = QgsPointXY(node1[0], node1[1])
            pt2 = QgsPointXY(node2[0], node2[1])
            
            linkInfo['distance'] = dist.measureLine([pt1, pt2])
            
            if feat['highway']:
                linkInfo['highway'] = feat['highway']
            else:
                linkInfo['highway'] = ''
            
            if feat['oneway']:
                linkInfo['oneway'] = feat['oneway']
            else:
                linkInfo['oneway'] = ''
            
            if feat['bridge']:
                linkInfo['bridge'] = feat['bridge']
            else:
                linkInfo['bridge'] = ''
 
            if feat['width']:
                linkInfo['width'] = feat['width']
            else:
                linkInfo['width'] = ''
                
            links[link] = linkInfo
        
        node1 = node2
        nodeId1 = nodeId2
        
nodeFile = open('C:/Users/Mizuki/Desktop/output/output_nodes.csv', 'w')

nodeFile.write('nodeId,x,y\n')
for (x, y), nodeId in nodes.items():
    nodeFile.write('%d,%f,%f\n' % (nodeId, x, y))

nodeFile.close()

linkFile = open('C:/Users/Mizuki/Desktop/output/output_links.csv', 'w')
linkFile.write('nodeIdOrg,nodeIdDest,distance,highway,oneway,bridge,width\n')
for (nodeId1, nodeId2), linkInfo in links.items():
    dist = linkInfo['distance']
    highway = linkInfo['highway']
    oneway = linkInfo['oneway']
    bridge = linkInfo['bridge']
    width = linkInfo['width']
    linkFile.write('%d,%d,%f,%s,%s,%s,%s\n' % (nodeId1, nodeId2, dist, highway, oneway, bridge, width))

linkFile.close()
#verts = []
#intersects = []
#for feat in feats:
#    geom = feat.geometry()
#    vertIter = geom.vertices()
#    while vertIter.hasNext():
#        vert = vertIter.next()
#        if vert in intersects:
#            pass
#        elif vert in verts:
#            intersects.append(vert)
#        else:
#            verts.append(vert)



#ptLayer = QgsVectorLayer(layer.source(), 'point', layer.providerType())
#prov = ptLayer.dataProvider()
#ptLayer.startEditing()
#prov.truncate()
#for intersect in intersects:
#    feat = QgsFeature()
#    geom = QgsGeometry.fromPointXY(QgsPointXY(intersect.x(), intersect.y()))
#    feat.setGeometry(geom)
#    prov.addFeatures([feat])
#
#ptLayer.commitChanges()
 
# Add the layer to the Layers panel
#QgsProject.instance().addMapLayer(ptLayer)