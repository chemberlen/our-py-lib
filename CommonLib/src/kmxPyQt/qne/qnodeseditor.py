# Copyright (c) 2014, ALDO HOEBEN
# Copyright (c) 2012, STANISLAW ADASZEWSKI
#All rights reserved.
#
#Redistribution and use in source and binary forms, with or without
#modification, are permitted provided that the following conditions are met:
#    * Redistributions of source code must retain the above copyright
#      notice, this list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright
#      notice, this list of conditions and the following disclaimer in the
#      documentation and/or other materials provided with the distribution.
#    * Neither the name of STANISLAW ADASZEWSKI nor the
#      names of its contributors may be used to endorse or promote products
#      derived from this software without specific prior written permission.
#
#THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
#DISCLAIMED. IN NO EVENT SHALL STANISLAW ADASZEWSKI BE LIABLE FOR ANY
#DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
#(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
#LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
#ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


from PyQt5.QtCore import (Qt, QObject, QEvent, QSizeF, QRectF, QPointF)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsSceneMouseEvent)
from PyQt5 import QtGui

from kmxPyQt.qne.qneblock import QNEBlock
from kmxPyQt.qne.qneport import QNEPort
from kmxPyQt.qne.qneconnection import QNEConnection
import sip

class QNodesEditor(QObject):

	def __init__(self, parent):
		super(QNodesEditor, self).__init__(parent)
		
		self.selBlock = None
		self.connection = None
		
		self.callBackConnAdded = None
		self.callBackConnRemoved = None

		self.callBackBlockRemoved = None
		self.callBackBlockSelected = None
		self.callBackBlockDeSelected = None
	
	def install(self, scene):
		self.scene = scene
		self.scene.installEventFilter(self)
	
	
	def itemAt(self, position):
		items = self.scene.items(QRectF( position - QPointF(1,1) , QSizeF(3,3) ))
		
		for item in items:
		    if item.type() > QGraphicsItem.UserType:
		        return item
		
		return None;
		
		
	def eventFilter(self, object, event):

		if event.type() == QEvent.GraphicsSceneMousePress:
			if event.button() == Qt.LeftButton:
				item = self.itemAt(event.scenePos())
				if item and item.type() == QNEPort.Type:
				    self.connection = QNEConnection(None)
				    self.scene.addItem(self.connection)
				
				    self.connection.setPort1(item)
				    self.connection.setPos1(item.scenePos())
				    self.connection.setPos2(event.scenePos())
				    self.connection.updatePath()
				
				    return True
				
				elif item and item.type() == QNEBlock.Type:
				    if self.selBlock and not sip.isdeleted(self.selBlock):
				        self.selBlock.setZValue(0)
				
				    item.setZValue(1)
				    self.selBlock = item
				    
				    if self.callBackBlockSelected:
				    	self.callBackBlockSelected(self.selBlock)
				
				else:
					self.selBlock = None
					if self.callBackBlockDeSelected:
						self.callBackBlockDeSelected()
		
			elif event.button() == Qt.RightButton:
				item = self.itemAt(event.scenePos())
				if item and item.type()==QNEBlock.Type:				
					p1 = item.ports()[0]
					if (p1.portName()=="Start" or p1.portName()=="End"): return True					
				if item and (item.type() == QNEConnection.Type or item.type() == QNEBlock.Type):
					if self.selBlock == item:
						self.selBlock = None
						if self.callBackBlockDeSelected:
							self.callBackBlockDeSelected()						
				if item and item.type() == QNEConnection.Type:
					item.port1().removeConnection(item)
					item.port2().removeConnection(item)
					if self.callBackConnRemoved:
						self.callBackConnRemoved(item)
					self.scene.removeItem(item)
				elif item and item.type() == QNEBlock.Type:
					for port in set(item.ports()):
						for connection in set(port.connections()):
							connection.port1().removeConnection(connection)
							connection.port2().removeConnection(connection)
							self.scene.removeItem(connection)
						self.scene.removeItem(port)
					if self.callBackBlockRemoved:
						self.callBackBlockRemoved(item)

					self.scene.removeItem(item)
				return True
		
		
		elif event.type() == QEvent.GraphicsSceneMouseMove:
		    if self.connection:
		        self.connection.setPos2(event.scenePos())
		        self.connection.updatePath()
		
		        return True
		
		
		elif event.type() == QEvent.GraphicsSceneMouseRelease:
		    if self.connection and event.button() == Qt.LeftButton:
		        item = self.itemAt(event.scenePos())
		        if item and item.type() == QNEPort.Type:
		            port1 = self.connection.port1()
		            port2 = item
		
		            if port1.block() != port2.block() and port1.isOutput() != port2.isOutput() and not port1.isConnected(port2):
		
		                self.connection.setPos2(port2.scenePos())
		                self.connection.setPort2(port2)
		                self.connection.updatePath()
		                self.connection = None
	                	if self.callBackConnAdded:
                			self.callBackConnAdded(self.connection)		                
		
		                return True
		
		        self.connection.port1().removeConnection(self.connection)
		        self.scene.removeItem(self.connection)
		        self.connection = None
		        return True
		
		return super(QNodesEditor, self).eventFilter(object, event)

