/***************************************************************************
 *   Copyright (C) 2005-2008 by the FIFE team                              *
 *   http://www.fifengine.de                                               *
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
 *   51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA              *
 ***************************************************************************/

// Standard C++ library includes

// 3rd party library includes

// FIFE includes
// These includes are split up in two parts, separated by one empty line
// First block: files included from the FIFE root src directory
// Second block: files included from the same folder
#include "util/structures/purge.h"
#include "model/metamodel/abstractpather.h"
#include "model/metamodel/object.h"
#include "structures/map.h"
#include "util/base/exception.h"

#include "model.h"

namespace FIFE {

	Model::Model(): 
		FifeClass(),
		m_timeprovider(NULL) {
	}

	Model::~Model() {
		purge(m_maps);
		for(std::list<namespace_t>::iterator nspace = m_namespaces.begin(); nspace != m_namespaces.end(); ++nspace)
			purge(nspace->second);
		purge(m_pathers);
	}

	Map* Model::createMap(const std::string& identifier) {
		std::list<Map*>::const_iterator it = m_maps.begin();
		for(; it != m_maps.end(); ++it) {
			if(identifier == (*it)->getId())
				throw NameClash(identifier);
		}

		Map* map = new Map(identifier, &m_timeprovider);
		m_maps.push_back(map);
		return map;
	}

	void Model::adoptPather(AbstractPather* pather) {
		m_pathers.push_back(pather);
	}
	
	AbstractPather* Model::getPather(const std::string& pathername) {
		std::vector<AbstractPather*>::const_iterator it = m_pathers.begin();
		for(; it != m_pathers.end(); ++it) {
			if ((*it)->getName() == pathername) {
				return *it;
			}
		}
		return NULL;
	}
	
	Map* Model::getMap(const std::string& identifier) const {
		std::list<Map*>::const_iterator it = m_maps.begin();
		for(; it != m_maps.end(); ++it) {
			if((*it)->getId() == identifier)
				return *it;
		}

		throw NotFound(std::string("Tried to get non-existant map: ") + identifier + ".");
	}

	void Model::deleteMap(Map* map) {
		std::list<Map*>::iterator it = m_maps.begin();
		for(; it != m_maps.end(); ++it) {
			if(*it == map) {
				delete *it;
				m_maps.erase(it);
				return ;
			}
		}
	}

	size_t Model::getNumMaps() const {
		return m_maps.size();
	}

	void Model::deleteMaps() {
		purge(m_maps);
		m_maps.clear();
	}

	std::list<std::string> Model::getNamespaces() const {
		std::list<std::string> lst;
		std::list<namespace_t>::const_iterator nspace = m_namespaces.begin();
		for(; nspace != m_namespaces.end(); ++nspace) {
			lst.push_back(nspace->first);
		}

		return lst;
	}

	Object* Model::createObject(const std::string& identifier, const std::string& name_space, Object* parent) {

		std::list<namespace_t>::iterator nspace = m_namespaces.begin();
		for(; nspace != m_namespaces.end(); ++nspace) {
			if(nspace->first == name_space) break;
		}

		if(nspace == m_namespaces.end()) {
			m_namespaces.push_back(namespace_t(name_space,std::list<Object*>()));
			nspace = m_namespaces.end();
			--nspace;
		}

		std::list<Object*>::const_iterator it = nspace->second.begin();
		for(; it != nspace->second.end(); ++it) {
			if(identifier == (*it)->getId())
				throw NameClash(identifier);
		}

		Object* object = new Object(identifier, name_space, parent);
		nspace->second.push_back(object);
		return object;
	}

	Object* Model::getObject(const std::string& id, const std::string& name_space) {
		std::list<namespace_t>::iterator nspace = m_namespaces.begin();
		for(; nspace != m_namespaces.end(); ++nspace) {
			if(nspace->first == name_space) {
				std::list<Object*>::iterator obj = nspace->second.begin();
				for(; obj != nspace->second.end(); ++obj)
					if((*obj)->getId() == id) return *obj;
			}
		}
		for(; nspace != m_namespaces.end(); ++nspace) {
			std::list<Object*>::iterator obj = nspace->second.begin();
			for(; obj != nspace->second.end(); ++obj)
				if((*obj)->getId() == id) return *obj;
		}
 
		return 0;
	}

	const std::list<Object*>& Model::getObjects(const std::string& name_space) const {
		std::list<namespace_t>::const_iterator nspace = m_namespaces.begin();
		for(; nspace != m_namespaces.end(); ++nspace) {
			if(nspace->first == name_space) return nspace->second;
		}

		throw NotFound(name_space);
	}

	void Model::update() {
		std::list<Map*>::iterator it = m_maps.begin();
		for(; it != m_maps.end(); ++it) {
			(*it)->update();
		}
		std::vector<AbstractPather*>::iterator jt = m_pathers.begin();
		for(; jt != m_pathers.end(); ++jt) {
			(*jt)->update();
		}
	}

} //FIFE

