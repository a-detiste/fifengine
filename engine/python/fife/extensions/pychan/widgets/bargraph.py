# -*- coding: utf-8 -*-

# ####################################################################
#  Copyright (C) 2005-2013 by the FIFE team
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

from fife import fifechan

from fife.extensions.pychan.attrs import BoolAttr, ColorAttr, IntAttr, PointAttr
from fife.extensions.pychan.properties import ColorProperty

from .widget import Widget


class BarGraph(Widget):
	""" A bar graph widget

	New Attributes
	==============

	  - bar_position: x and y coordinate
	  - bar_width': int: default 10
	  - bar_height: int: default 10
	  - opaque: bool: default False
	"""

	ATTRIBUTES = Widget.ATTRIBUTES + [ PointAttr('bar_position'),
									   IntAttr('bar_width'),
									   IntAttr('bar_height'),
									   BoolAttr('opaque')
									 ]
	DEFAULT_HEXPAND = False
	DEFAULT_VEXPAND = False

	DEFAULT_OPAQUE = False
	DEFAULT_BAR_POSITION = 0,0
	DEFAULT_BAR_WIDTH = 10
	DEFAULT_BAR_HEIGHT = 10

	def __init__(self,
				 parent = None,
				 name = None,
				 size = None,
				 min_size = None,
				 max_size = None,
				 fixed_size = None,
				 margins = None,
				 padding = None,
				 helptext = None,
				 position = None,
				 style = None,
				 hexpand = None,
				 vexpand = None,
				 font = None,
				 base_color = None,
				 background_color = None,
				 foreground_color = None,
				 selection_color = None,
				 border_color = None,
				 outline_color = None,
				 border_size = None,
				 outline_size = None,
				 position_technique = None,
				 is_focusable = None,
				 comment = None,
				 opaque = None,
				 bar_position = None,
				 bar_width = None,
				 bar_height = None):

		self.real_widget = fifechan.BarGraph()
		self.opaque = self.DEFAULT_OPAQUE
		self.bar_positon = self.DEFAULT_BAR_POSITION
		self.bar_width = self.DEFAULT_BAR_WIDTH
		self.bar_height = self.DEFAULT_BAR_HEIGHT

		super(BarGraph, self).__init__(parent=parent,
									   name=name,
									   size=size,
									   min_size=min_size,
									   max_size=max_size,
									   fixed_size=fixed_size,
									   margins=margins,
									   padding=padding,
									   helptext=helptext,
									   position=position,
									   style=style,
									   hexpand=hexpand,
									   vexpand=vexpand,
									   font=font,
									   base_color=base_color,
									   background_color=background_color,
									   foreground_color=foreground_color,
									   selection_color=selection_color,
									   border_color=border_color,
									   outline_color=outline_color,
									   border_size=border_size,
									   outline_size=outline_size,
									   position_technique=position_technique,
									   is_focusable=is_focusable,
									   comment=comment)

		if opaque is not None: self.opaque = opaque
		if bar_position is not None: self.bar_position = bar_position
		if bar_width is not None: self.bar_width = bar_width
		if bar_height is not None: self.bar_height = bar_height


	def clone(self, prefix):
		barGraphClone = BarGraph(None,
					self._createNameWithPrefix(prefix),
					self.size,
					self.min_size,
					self.max_size,
					self.fixed_size,
					self.margins,
					self.padding,
					self.helptext,
					self.position,
					self.style,
					self.hexpand,
					self.vexpand,
					self.font,
					self.base_color,
					self.background_color,
					self.foreground_color,
					self.selection_color,
					self.border_color,
					self.outline_color,
					self.border_size,
					self.outline_size,
					self.position_technique,
					self.is_focusable,
					self.comment,
					self.opaque,
					self.bar_positon,
					self.bar_width,
					self.bar_height)
		return barGraphClone

	def _setOpaque(self, opaque): self.real_widget.setOpaque(opaque)
	def _getOpaque(self): return self.real_widget.isOpaque()
	opaque = property(_getOpaque, _setOpaque)

	def _setBarPosition(self, bar_position): self.real_widget.setBarPosition(bar_position[0], bar_position[1])
	def _getBarPosition(self): return (self.real_widget.getBarX(), self.real_widget.getBarY())
	bar_position = property(_getBarPosition, _setBarPosition)

	def _setBarWidth(self, bar_width): self.real_widget.setBarWidth(bar_width)
	def _getBarWidth(self): return self.real_widget.getBarWidth()
	bar_width = property(_getBarWidth, _setBarWidth)
	
	def _setBarHeight(self, bar_height): self.real_widget.setBarHeight(bar_height)
	def _getBarHeight(self): return self.real_widget.getBarHeight()
	bar_height = property(_getBarHeight, _setBarHeight)

