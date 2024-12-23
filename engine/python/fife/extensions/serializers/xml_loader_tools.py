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

""" utilities for xml maploading process """
from past.utils import old_div
import os
import math

def loadImportFile(loader, path, engine, debug=False):
	""" uses XMLObjectLoader to load import files from path
	
	@type	path:	string
	@param	path:	path to import file
	@type	debug:	bool
	@param	debug:	flag to activate / deactivate print statements
	"""
	loader.loadResource(path)
	if debug: print('imported object file ' + path)

def loadImportDir(loader, path, engine, debug=False):
	""" helper function to call loadImportFile on a directory
	
	@type	path:	string
	@param	path:	path to import directory
	@type	debug:	bool
	@param	debug:	flag to activate / deactivate print statements
	"""
	for _file in [f for f in engine.getVFS().listFiles(path) if f.split('.')[-1] == 'xml']:
		loadImportFile(loader, '/'.join([path, _file]), engine, debug)

def loadImportDirRec(loader, path, engine, debug=False):
	""" helper function to call loadImportFile recursive on a directory

	@type	path:	string
	@param	path:	path to import directory
	@type	debug:	bool
	@param	debug:	flag to activate / deactivate print statements	
	"""
	loadImportDir(loader, path, engine, debug)

	for _dir in [d for d in engine.getVFS().listDirectories(path) if not d.startswith('.')]:
		loadImportDirRec(loader, '/'.join([path, _dir]), engine, debug)
		
def root_subfile(masterfile, subfile):
	"""
	Returns new path for given subfile (path), which is rooted against masterfile
	E.g. if masterfile is ./../foo/bar.xml and subfile is ./../foo2/subfoo.xml,
	returned path is ../foo2/subfoo.xml
	NOTE: masterfile is expected to be *file*, not directory. subfile can be either
	"""
	s = '/'

	masterfile = norm_path(os.path.abspath(masterfile))
	subfile = norm_path(os.path.abspath(subfile))

	master_fragments = masterfile.split(s)
	sub_fragments = subfile.split(s)

	master_leftovers = []
	sub_leftovers = []

	for i in range(len(master_fragments)):
		try:
			if master_fragments[i] == sub_fragments[i]:
				master_leftovers = master_fragments[i+1:]
				sub_leftovers = sub_fragments[i+1:]
		except IndexError:
			break

	pathstr = ''
	for f in master_leftovers[:-1]:
		pathstr += '..' + s
	pathstr += s.join(sub_leftovers)
	return pathstr

def reverse_root_subfile(masterfile, subfile):
	"""
	does inverse operation to root_subfile. E.g. 
	E.g. if masterfile is ./../foo/bar.xml and subfile is ../foo2/subfoo.xml,
	returned path ./../foo2/subfoo.xml
	Usually this function is used to convert saved paths into engine relative paths
	NOTE: masterfile is expected to be *file*, not directory. subfile can be either
	"""
	s = '/'

	masterfile = norm_path(os.path.abspath(masterfile)).split(s)[:-1]
	subfile = norm_path(os.path.abspath( s.join(masterfile) + s + subfile ))
	masterfile = norm_path(os.getcwd()) + s + 'foo.bar' # cheat a little to satisfy root_subfile
	return root_subfile(masterfile, subfile)

def norm_path(path):
	"""
	Makes the path use '/' delimited separators. FIFE always uses these delimiters, but some os-related
	routines will default to os.path.sep.
	"""
	if os.path.sep == '/':
		return path

	return '/'.join(path.split(os.path.sep))


def frange(limit1, limit2 = None, increment = 1.):
	"""Range function that accepts floats (and integers).
	If only one limit is specified, assumes 0 as lower limit.

	Usage:
	frange(-2, 2, 0.1)
	frange(10)
	frange(10, increment = 0.5)

	The returned value is an iterator.  Use list(frange) for a list.

	source: U{http://code.activestate.com/recipes/
	66472-frange-a-range-function-with-float-increments/}
 
	@type	limit1:	float
	@param	limit1:	lower range limit
	@type	limit2:	float
	@param	limit2:	upper range limit
	@type	increment:	float
	@param	increment:	length of each step
	@rtype	generator
	@return	iterable over (limit2 - limit1) / increment steps
	"""

	if limit2 is None:
		limit2, limit1 = float(limit1), 0.
	else:
		limit1 = float(limit1)

	count = int(math.ceil(old_div((limit2 - limit1),increment)))
	return (limit1 + n*increment for n in range(count))
	
