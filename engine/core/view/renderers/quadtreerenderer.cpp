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

// 3rd party library includes

// FIFE includes
// These includes are split up in two parts, separated by one empty line
// First block: files included from the FIFE root src directory
// Second block: files included from the same folder
#include "video/renderbackend.h"
#include "util/logger.h"

#include "util/fife_math.h"
#include "util/logger.h"
#include "model/metamodel/grids/cellgrid.h"
#include "model/structures/elevation.h"
#include "model/structures/instance.h"
#include "model/structures/layer.h"
#include "model/structures/location.h"

#include "view/camera.h"
#include "quadtreerenderer.h"
#include "model/structures/instancetree.h"
#include "util/quadtree.h"

///credit to phoku for his NodeDisplay example which the visitor code is adapted from ( he coded the quadtree after all )
namespace FIFE {
	static Logger _log(LM_VIEWVIEW);

	QuadTreeRenderer::QuadTreeRenderer(RenderBackend* renderbackend, int position):
			m_renderbackend(renderbackend) {
		setPipelinePosition(position);
		setEnabled(false);
	}

	QuadTreeRenderer::~QuadTreeRenderer() {	}
	static int minpt;
	static int maxpt;
	RenderVisitor::RenderVisitor(RenderBackend * rb, Layer * layer, Camera *camera) {

		m_renderbackend = rb;
		m_layer = layer;
		m_camera = camera;
	}

	RenderVisitor::~RenderVisitor() {}

	template<typename T> bool RenderVisitor::visit(QuadNode<T,2>* node, int d) {

		if (d==0)
			visited = 0;

		int x = node->x();
		int y = node->y();
		int size = node->size();

		++visited;
		CellGrid *cg = m_layer->getCellGrid(); ///we have checked for null pointer in  quadtreerenderer::render().. no need to check again


		ExactModelCoordinate emc= cg->toElevationCoordinates(ExactModelCoordinate( x-0.5,y-0.5) );//0.5 for each cell's half-width
		ScreenPoint scrpt1 =m_camera->toScreenCoordinates( emc );
		emc= cg->toElevationCoordinates(ExactModelCoordinate( x-0.5,y+size-1-0.5) );// this size usage is wrong.. me thinks
		ScreenPoint scrpt2 =m_camera->toScreenCoordinates( emc );
		emc= cg->toElevationCoordinates(ExactModelCoordinate( x+size-1-0.5,y-0.5) );
		ScreenPoint scrpt3 =m_camera->toScreenCoordinates( emc );
		emc= cg->toElevationCoordinates(ExactModelCoordinate( x+size-1-0.5,y+size-1-0.5) );
		ScreenPoint scrpt4 =m_camera->toScreenCoordinates( emc );
		minpt =std::min(minpt,scrpt1.x);
		maxpt =std::max(maxpt,scrpt1.x);

		m_renderbackend->drawLine( Point(scrpt1.x,scrpt1.y) , Point(scrpt2.x,scrpt2.y), 255, 0, 0);
		m_renderbackend->drawLine(Point(scrpt1.x,scrpt1.y), Point(scrpt3.x,scrpt3.y), 255, 0, 0);
		m_renderbackend->drawLine(Point(scrpt3.x,scrpt3.y), Point(scrpt4.x,scrpt4.y), 255, 0, 0);
		m_renderbackend->drawLine(Point(scrpt2.x,scrpt2.y), Point(scrpt4.x,scrpt4.y), 255, 0, 0);

		return true;
	}


	void QuadTreeRenderer::render(Camera* cam, Layer* layer, std::vector<Instance*>& instances) {
		minpt =0;
		maxpt =0;
		CellGrid* cg = layer->getCellGrid();
		if (!cg) {
			FL_WARN(_log, "No cellgrid assigned to layer, cannot draw grid");
			return;
		}
		InstanceTree * itree = layer->getInstanceTree();

		static RenderVisitor VIPguess(m_renderbackend, layer,cam);

		itree->m_tree.apply_visitor( VIPguess );
		std::cout << "max: " << maxpt << "\n";
	}

}

