/***************************************************************************
 *   Copyright (C) 2005-2007 by the FIFE Team                              *
 *   fife-public@lists.sourceforge.net                                     *
 *   This file is part of FIFE.                                            *
 *                                                                         *
 *   FIFE is free software; you can redistribute it and/or modify          *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 *   This program is distributed in the hope that it will be useful,       *
 *   but WITHOUT ANY WARRANTY; without even the implied warranty of        *
 *   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         *
 *   GNU General Public License for more details.                          *
 *                                                                         *
 *   You should have received a copy of the GNU General Public License     *
 *   along with this program; if not, write to the                         *
 *   Free Software Foundation, Inc.,                                       *
 *   59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.             *
 ***************************************************************************/

#ifndef FIFE_MODULES_H
#define FIFE_MODULES_H

// Standard C++ library includes

// 3rd party library includes

// FIFE includes
// These includes are split up in two parts, separated by one empty line
// First block: files included from the FIFE root src directory
// Second block: files included from the same folder

enum logmodule_t {
	LM_CORE = -1,
	LM_AUDIO,
	LM_CONTROLLER,
	LM_EVTCHANNEL,
	LM_GUI,
	LM_CONSOLE,
	LM_LOADERS,
	LM_MODEL,
	LM_STRUCTURES,
	LM_INSTANCE,
	LM_LOCATION,
	LM_METAMODEL,
	LM_PATHFINDER,
	LM_UTIL,
	LM_VFS,
	LM_VIDEO,
	LM_VIEW,
	LM_CAMERA,
	LM_VIEWVIEW,
	LM_XML,
	LM_MODULE_MAX // sentinel
};

#define MODULE_INFO_RELATIONSHIPS \
	ModuleInfo moduleInfos[] = { \
		{LM_AUDIO, LM_CORE, "Audio"}, \
		{LM_CONTROLLER, LM_CORE, "Controller"}, \
		{LM_EVTCHANNEL, LM_CORE, "Event Channel"}, \
		{LM_GUI, LM_CORE, "GUI"}, \
		  {LM_CONSOLE, LM_GUI, "Console"}, \
		{LM_LOADERS, LM_CORE, "Loaders"}, \
		{LM_MODEL, LM_CORE, "Model"}, \
		  {LM_STRUCTURES, LM_MODEL, "Structures"}, \
		    {LM_INSTANCE, LM_STRUCTURES, "Instance"}, \
		    {LM_LOCATION, LM_STRUCTURES, "Location"}, \
		  {LM_METAMODEL, LM_MODEL, "Metamodel"}, \
		{LM_PATHFINDER, LM_CORE, "Pathfinder"}, \
		{LM_UTIL, LM_CORE, "Util"}, \
		{LM_VFS, LM_CORE, "VFS"}, \
		{LM_VIDEO, LM_CORE, "Video" }, \
		{LM_VIEW, LM_CORE, "View"}, \
		  {LM_CAMERA, LM_VIEW, "Camera"}, \
		  {LM_VIEWVIEW, LM_VIEW, "View::View"}, \
		{LM_XML, LM_CORE, "XML"} \
	};

#endif
