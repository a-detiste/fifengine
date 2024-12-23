#!/usr/bin/env python

# -*- coding: utf-8 -*-

# ####################################################################
#  Copyright (C) 2005-2019 by the FIFE team
#  http://www.fifengine.net
#  This file is part of FIFE.
#
#  FIFE is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 2.1 of the License, or (at your option) any later version.
#
#  This library is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public
#  License along with this library; if not, write to the
#  Free Software Foundation, Inc.,
#  51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
# ####################################################################

from fife import fife
from fife.extensions import pychan
from fife.extensions.pychan.tools import callbackWithArguments as cbwa
from fife.extensions.fife_timer import Timer

import scripts.test as test

class KeyListener(fife.IKeyListener):
	def __init__(self, test):
		self._engine = test._engine
		self._test = test
		self._eventmanager = self._engine.getEventManager()
		
		fife.IKeyListener.__init__(self)

	def keyPressed(self, evt):
		keyval = evt.getKey().getValue()
		keystr = evt.getKey().getAsString().lower()
		if keystr == 't':
			r = self._test._camera.getRenderer('GridRenderer')
			r.setEnabled(not r.isEnabled())
		elif keystr == 'c':
			r = self._test._camera.getRenderer('CoordinateRenderer')
			r.setEnabled(not r.isEnabled())
		
	def keyReleased(self, evt):
		pass

class MouseListener(fife.IMouseListener):
	def __init__(self, test):
		self._engine = test._engine
		self._test = test
		self._eventmanager = self._engine.getEventManager()
		
		fife.IMouseListener.__init__(self)
		
	def mousePressed(self, event):
		if event.isConsumedByWidgets():
			return
			
		if event.getButton() == fife.MouseEvent.LEFT:
			self.select_begin = (event.getX(), event.getY())
			#self._test.rect_test(event.getX(), event.getY())
			
			clickpoint = fife.ScreenPoint(event.getX(), event.getY())
			self._test.movePlayer(clickpoint)
		
			event.consume()
				
	def mouseReleased(self, event):
		if event.getButton() == fife.MouseEvent.LEFT and hasattr(self, 'select_begin'):
			del self.select_begin
			r = fife.InstanceRenderer.getInstance(self._test._camera)
			r.removeAllColored()
			r.removeAllOutlines()
			
			genericrenderer = fife.GenericRenderer.getInstance(self._test._camera)
			genericrenderer.removeAll("selection")

	def mouseMoved(self, event):
		pass
		
	def mouseEntered(self, event):
		pass
		
	def mouseExited(self, event):
		pass
		
	def mouseClicked(self, event):
		pass
	
	def mouseWheelMovedUp(self, event):
		pass	
		
	def mouseWheelMovedDown(self, event):
		pass
		
	def mouseDragged(self, event):
		instancerenderer = fife.InstanceRenderer.getInstance(self._test._camera)
		instancerenderer.removeAllColored()
		instancerenderer.removeAllOutlines()
	
		if event.getButton() == fife.MouseEvent.LEFT and hasattr(self, 'select_begin'):
			do_multi = ((self.select_begin[0] - event.getX()) ** 2 + (self.select_begin[1] - event.getY()) ** 2) >= 10 # from 3px (3*3 + 1)
			genericrenderer = fife.GenericRenderer.getInstance(self._test._camera)
			genericrenderer.removeAll("selection")
			if do_multi:
				# draw a rectangle
				a = fife.Point(min(self.select_begin[0], event.getX()), \
											 min(self.select_begin[1], event.getY()))
				b = fife.Point(max(self.select_begin[0], event.getX()), \
											 min(self.select_begin[1], event.getY()))
				c = fife.Point(max(self.select_begin[0], event.getX()), \
											 max(self.select_begin[1], event.getY()))
				d = fife.Point(min(self.select_begin[0], event.getX()), \
											 max(self.select_begin[1], event.getY()))
				genericrenderer.addLine("selection", \
										fife.RendererNode(a), fife.RendererNode(b), 200, 200, 200)
				genericrenderer.addLine("selection", \
										fife.RendererNode(b), fife.RendererNode(c), 200, 200, 200)
				genericrenderer.addLine("selection", \
										fife.RendererNode(d), fife.RendererNode(c), 200, 200, 200)
				genericrenderer.addLine("selection", \
										fife.RendererNode(a), fife.RendererNode(d), 200, 200, 200)

			instances = self._test._camera.getMatchingInstances(\
				fife.Rect(min(self.select_begin[0], event.getX()), \
									min(self.select_begin[1], event.getY()), \
									abs(event.getX() - self.select_begin[0]), \
									abs(event.getY() - self.select_begin[1])) if do_multi else fife.ScreenPoint(event.getX(), event.getY()),
				self._test._actorlayer,
				0) # False for accurate

			for instance in instances:
				instancerenderer.addColored(instance, 250, 50, 250)
				instancerenderer.addOutlined(instance, 255, 255, 0, 2)


class SelectionTest(test.Test):

	def create(self, engine, application):
		self._application = application
		self._engine = engine
		self._running = False

		self._loader = fife.MapLoader(self._engine.getModel(), 
									self._engine.getVFS(), 
									self._engine.getImageManager(), 
									self._engine.getRenderBackend())

		self._eventmanager = self._engine.getEventManager()

	def destroy(self):
		#any left over cleanup here
		pass
		
	def run(self):
		self._running = True
		
		self._mouselistener = MouseListener(self)
		self._eventmanager.addMouseListener(self._mouselistener)
		
		self._keylistener = KeyListener(self)
		self._eventmanager.addKeyListener(self._keylistener)

		self._font = pychan.internal.get_manager().createFont("data/fonts/rpgfont.png")
		if self._font is None:
			raise InitializationError("Could not load font %s" % name)

		self.loadMap("data/maps/grassland.xml")

	def stop(self):
		self._running = False
		
		self._engine.getModel().deleteMap(self._map)
		self._engine.getModel().deleteObjects()
		
		self._eventmanager.removeMouseListener(self._mouselistener)
		self._eventmanager.removeKeyListener(self._keylistener)
		
		del self._mouselistener
		del self._keylistener
		
	def isRunning(self):
		return self._running

	def getName(self):
		return "SelectionTest"
		
	def getAuthor(self):
		return "prock"

	def getDescription(self):
		return "Simple test of selecting multiple instances at once using the mouse."

	def getHelp(self):
		return open( 'data/help/SelectionTest.txt', 'r' ).read()
		
	def pump(self):
		"""
		This gets called every frame that the test is running.  We have nothing
		to do here for this test.
		"""
		pass

	def loadMap(self, filename):
		"""
		Simple function to load and display a map file. We could of course 
		have passed in the map filename but I'll leave that up to you.
		
		@param filename The filename.
		"""
	
		self._mapfilename = filename
		
		if self._loader.isLoadable(self._mapfilename):
			self._map = self._loader.load(self._mapfilename)
			self._mapLoaded = True

		self._camera = self._map.getCamera("camera1")
		self._actorlayer = self._map.getLayer("item_layer")
		self._groundlayer = self._map.getLayer("ground_layer")
		self._player = self._actorlayer.getInstance("player")
		
		gridrenderer = self._camera.getRenderer('GridRenderer')
		gridrenderer.activateAllLayers(self._map)

		coordrenderer = fife.CoordinateRenderer.getInstance(self._camera)
		coordrenderer.setFont(self._font)
		coordrenderer.clearActiveLayers()
		coordrenderer.addActiveLayer(self._groundlayer)
		
		genericrenderer = fife.GenericRenderer.getInstance(self._camera)
		genericrenderer.activateAllLayers(self._map)
		genericrenderer.setEnabled(True)

		instancerenderer = fife.InstanceRenderer.getInstance(self._camera)
		instancerenderer.activateAllLayers(self._map)

	def rect_test(self, cursor_x, cursor_y):
		""" create a rect from ORIGIN to mouse cursor coordinates		
		
		@type 	cursor_x:	int
		@param	cursor_x:	x coordinate of the mouse cursor
		@type	cursor_y:	int
		@param	cursor_y:	y coordinate of the mouse cursor
		"""
		if self._camera is None: return
		if self._actorlayer is None: return
		
		ORIGIN = (0,0)
		x, y = ORIGIN
		layer = self._actorlayer
		
		rect = fife.Rect(x, y, cursor_x, cursor_y)
		
		instances = self._camera.getMatchingInstances(rect, layer, False)
		
		for instance in instances:
			print(instance, instance.getId())

	def getLocationAt(self, screenpoint):
		"""
		Query the main camera for the Map location (on the actor layer)
		that a screen point refers to.
		
		@param screenpoint A fife.ScreenPoint
		"""
		
		target_mapcoord = self._camera.toMapCoordinates(screenpoint, False)
		target_mapcoord.z = 0
		location = fife.Location(self._actorlayer)
		location.setMapCoordinates(target_mapcoord)
		return location

	def movePlayer(self, screenpoint):
		"""
		Simple function that moves the player instance to the given screenpoint.
		
		@param screenpoint A fife.ScreenPoint
		"""
		
		self._player.move('walk', self.getLocationAt(screenpoint), 4.0)
