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
 *   51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA              *
 ***************************************************************************/

// Standard C++ library includes
#include <assert.h>
#include <iostream>

// 3rd party library includes

// FIFE includes
// These includes are split up in two parts, separated by one empty line
// First block: files included from the FIFE root src directory
// Second block: files included from the same folder
#include "util/fife_math.h"
#include "util/logger.h"

#include "squaregrid.h"

namespace FIFE {
	static Logger _log(LM_SQUAREGRID);

	SquareGrid::SquareGrid(bool diagonals_accessible): 
		CellGrid(),
		m_diagonals_accessible(diagonals_accessible) {
	}

	SquareGrid::~SquareGrid() {
	}

	bool SquareGrid::isAccessible(const ModelCoordinate& curpos, const ModelCoordinate& target) {
		if (curpos == target)
			return true;
		if ((curpos.x == target.x) && (curpos.y - 1 == target.y))
			return true;
		if ((curpos.x == target.x) && (curpos.y + 1 == target.y))
			return true;
		if ((curpos.x + 1 == target.x) && (curpos.y == target.y))
			return true;
		if ((curpos.x - 1 == target.x) && (curpos.y == target.y))
			return true;

		if (m_diagonals_accessible) {
			return isAccessibleDiagonal(curpos, target);
		}

		return false;
	}

	bool SquareGrid::isAccessibleDiagonal(const ModelCoordinate& curpos, const ModelCoordinate& target) {
		if ((curpos.x - 1 == target.x) && (curpos.y - 1 == target.y))
			return true;
		if ((curpos.x - 1 == target.x) && (curpos.y + 1 == target.y))
			return true;
		if ((curpos.x + 1 == target.x) && (curpos.y - 1 == target.y))
			return true;
		if ((curpos.x + 1 == target.x) && (curpos.y + 1 == target.y))
			return true;
		return false;
	}

	float SquareGrid::getAdjacentCost(const ModelCoordinate& curpos, const ModelCoordinate& target) {
		assert(isAccessible(curpos, target));
		if (curpos == target) {
			return 0;
		}
		if (isAccessibleDiagonal(curpos, target)) {
			return M_SQRT2;
		}
		return 1;
	}

	const std::string& SquareGrid::getName() const {
		static std::string squareGrid("Square Grid");
		static std::string squareGridDiagonal("Square Grid with diagonal access");
		if (m_diagonals_accessible) {
			return squareGrid;
		}
		return squareGridDiagonal;
	}
	
	ExactModelCoordinate SquareGrid::toElevationCoordinates(const ExactModelCoordinate& layer_coords) {
		return m_inverse_matrix * layer_coords;
	}

	ExactModelCoordinate SquareGrid::toExactLayerCoordinates(const ExactModelCoordinate& elevation_coord) {
		return m_matrix * elevation_coord;
	}

	ModelCoordinate SquareGrid::toLayerCoordinates(const ExactModelCoordinate& elevation_coord) {
		ExactModelCoordinate dblpt = toExactLayerCoordinates(elevation_coord);
		ModelCoordinate result;
		result.x = static_cast<int>(floor(dblpt.x));
		result.y = static_cast<int>(floor(dblpt.y));
		
		if ((dblpt.x - static_cast<double>(result.x)) > 0.5) {
			result.x++;
		}
		if ((dblpt.y - static_cast<double>(result.y)) > 0.5) {
			result.y++;
		}
		
		return result;
	}
	
	void SquareGrid::getVertices(std::vector<ExactModelCoordinate>& vtx, const ModelCoordinate& cell) {
		vtx.clear();
		double x = static_cast<double>(cell.x);
		double y = static_cast<double>(cell.y);
		vtx.push_back(ExactModelCoordinate(x-0.5, y-0.5));
		vtx.push_back(ExactModelCoordinate(x+0.5, y-0.5));
		vtx.push_back(ExactModelCoordinate(x+0.5, y+0.5));
		vtx.push_back(ExactModelCoordinate(x-0.5, y+0.5));
	}
}