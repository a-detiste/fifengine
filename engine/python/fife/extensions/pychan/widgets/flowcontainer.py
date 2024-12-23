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

from fife import fife
from fife import fifechan

from fife.extensions.pychan.attrs import IntAttr, UnicodeAttr

from .containers import Container

class FlowContainer(Container):
	"""
	An implementation of a flow container that can contain other widgets.
	The widgets can be sorted vertical per row or horizontal per column.
	If the space in the container is too small to put all the components in one row or column,
	it uses multiple rows or columns.

	"""

	ATTRIBUTES = Container.ATTRIBUTES + [ IntAttr('alignment'), ]

	DEFAULT_LAYOUT = 'Horizontal'
	DEFAULT_ALIGNMENT = 4 # Center

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
				 background_image = None,
				 opaque = None,
				 layout = None,
				 spacing = None,
				 uniform_size = None,
				 _real_widget = None,
				 alignment = None):

		if _real_widget is None: _real_widget = fifechan.FlowContainer()
		
		super(FlowContainer,self).__init__(parent=parent,
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
										   comment=comment,
										   background_image=background_image,
										   opaque=opaque,
										   layout=layout,
										   spacing=spacing,
										   uniform_size=uniform_size,
										   _real_widget=_real_widget)

		if alignment is not None: self.alignment = alignment
		else: self.alignment = self.DEFAULT_ALIGNMENT

				
	def clone(self, prefix):
		containerClone = FlowContainer(None, 
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
						self.background_image,
						self.opaque,
						self.layout,
						self.spacing,
						self.uniform_size,
						None,
						self.alignment)
			
		containerClone.addChildren(self._cloneChildren(prefix))	
		return containerClone

	def _setAlignment(self, alignment): self.real_widget.setAlignment(alignment)
	def _getAlignment(self): self.real_widget.getAlignment()
	alignment = property(_getAlignment, _setAlignment)

	def adjustContent(self):
		self.real_widget.adjustContent()
