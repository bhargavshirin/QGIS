"""
***************************************************************************
    test_qgsembeddedsymbolrenderer.py
    ---------------------
    Date                 : March 2021
    Copyright            : (C) 2021 by Nyall Dawson
    Email                : nyall dot dawson at gmail dot com
***************************************************************************
*                                                                         *
*   This program is free software; you can redistribute it and/or modify  *
*   it under the terms of the GNU General Public License as published by  *
*   the Free Software Foundation; either version 2 of the License, or     *
*   (at your option) any later version.                                   *
*                                                                         *
***************************************************************************

From build dir, run: ctest -R PyQgsEmbeddedSymbolRenderer -V

"""

__author__ = "Matthias Kuhn"
__date__ = "December 2015"
__copyright__ = "(C) 2015, Matthias Kuhn"

import unittest

import qgis  # NOQA
from qgis.PyQt.QtCore import QSize
from qgis.core import (
    QgsEmbeddedSymbolRenderer,
    QgsFeature,
    QgsFillSymbol,
    QgsGeometry,
    QgsLineSymbol,
    QgsMapSettings,
    QgsMarkerSymbol,
    QgsRectangle,
    QgsVectorLayer,
)
from qgis.testing import start_app, QgisTestCase

from utilities import unitTestDataPath

TEST_DATA_DIR = unitTestDataPath()

start_app()


class TestQgsEmbeddedSymbolRenderer(QgisTestCase):
    @classmethod
    def control_path_prefix(cls):
        return "embedded"

    def testPoints(self):
        points_layer = QgsVectorLayer("Point", "Polys", "memory")
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromWkt("Point(-100 30)"))
        f.setEmbeddedSymbol(
            QgsMarkerSymbol.createSimple(
                {
                    "name": "triangle",
                    "size": 10,
                    "color": "#ff0000",
                    "outline_style": "no",
                }
            )
        )
        self.assertTrue(points_layer.dataProvider().addFeature(f))
        f.setGeometry(QgsGeometry.fromWkt("Point(-110 40)"))
        f.setEmbeddedSymbol(
            QgsMarkerSymbol.createSimple(
                {"name": "square", "size": 7, "color": "#00ff00", "outline_style": "no"}
            )
        )
        self.assertTrue(points_layer.dataProvider().addFeature(f))
        f.setGeometry(QgsGeometry.fromWkt("Point(-90 50)"))
        f.setEmbeddedSymbol(
            QgsMarkerSymbol.createSimple(
                {"name": "circle", "size": 9, "color": "#0000ff", "outline_style": "no"}
            )
        )
        self.assertTrue(points_layer.dataProvider().addFeature(f))

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsMarkerSymbol.createSimple(
                {"name": "star", "size": 10, "color": "#ff0000", "outline_style": "no"}
            )
        )
        points_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(400, 400))
        mapsettings.setOutputDpi(96)
        mapsettings.setExtent(QgsRectangle(-163, 22, -70, 52))
        mapsettings.setLayers([points_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_points", "embedded_points", mapsettings
            )
        )

    def testLines(self):
        line_layer = QgsVectorLayer("LineString", "Polys", "memory")
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromWkt("LineString(-100 30, -120 30)"))
        f.setEmbeddedSymbol(
            QgsLineSymbol.createSimple({"line_width": 3, "line_color": "#ff0000"})
        )
        self.assertTrue(line_layer.dataProvider().addFeature(f))
        f.setGeometry(QgsGeometry.fromWkt("LineString(-110 40, -130 40)"))
        f.setEmbeddedSymbol(
            QgsLineSymbol.createSimple({"line_width": 1.5, "line_color": "#00ff00"})
        )
        self.assertTrue(line_layer.dataProvider().addFeature(f))
        f.setGeometry(QgsGeometry.fromWkt("LineString(-90 50, -140 50)"))
        f.setEmbeddedSymbol(
            QgsLineSymbol.createSimple(
                {"line_width": 2, "line_color": "#0000ff", "line_style": "dash"}
            )
        )
        self.assertTrue(line_layer.dataProvider().addFeature(f))

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsLineSymbol.createSimple(
                {"line_width": 10, "line_color": "#ff0000"}
            )
        )
        line_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(400, 400))
        mapsettings.setOutputDpi(96)
        mapsettings.setExtent(QgsRectangle(-163, 22, -70, 52))
        mapsettings.setLayers([line_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_lines", "embedded_lines", mapsettings
            )
        )

    def testFills(self):
        line_layer = QgsVectorLayer("Polygon", "Polys", "memory")
        f = QgsFeature()
        f.setGeometry(
            QgsGeometry.fromWkt("Polygon((-100 30, -120 30, -110 20, -100 30))")
        )
        f.setEmbeddedSymbol(
            QgsFillSymbol.createSimple({"color": "#ff0000", "outline_style": "no"})
        )
        self.assertTrue(line_layer.dataProvider().addFeature(f))
        f.setGeometry(
            QgsGeometry.fromWkt("Polygon((-110 40, -130 40, -120 50, -110 40))")
        )
        f.setEmbeddedSymbol(
            QgsFillSymbol.createSimple({"color": "#00ff00", "outline_style": "no"})
        )
        self.assertTrue(line_layer.dataProvider().addFeature(f))
        f.setGeometry(
            QgsGeometry.fromWkt("Polygon((-90 50, -140 50, -110 60, -90 50))")
        )
        f.setEmbeddedSymbol(
            QgsFillSymbol.createSimple({"color": "#0000ff", "outline_style": "no"})
        )
        self.assertTrue(line_layer.dataProvider().addFeature(f))

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsFillSymbol.createSimple(
                {"color": "#ffff00", "outline_style": "no"}
            )
        )
        line_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(400, 400))
        mapsettings.setOutputDpi(96)
        mapsettings.setExtent(QgsRectangle(-163, 22, -70, 52))
        mapsettings.setLayers([line_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_polys", "embedded_polys", mapsettings
            )
        )

    def testDefaultSymbol(self):
        points_layer = QgsVectorLayer("Point", "Polys", "memory")
        f = QgsFeature()
        f.setGeometry(QgsGeometry.fromWkt("Point(-100 30)"))
        f.setEmbeddedSymbol(
            QgsMarkerSymbol.createSimple(
                {
                    "name": "triangle",
                    "size": 10,
                    "color": "#ff0000",
                    "outline_style": "no",
                }
            )
        )
        self.assertTrue(points_layer.dataProvider().addFeature(f))
        f.setGeometry(QgsGeometry.fromWkt("Point(-110 40)"))
        f.setEmbeddedSymbol(
            QgsMarkerSymbol.createSimple(
                {"name": "square", "size": 7, "color": "#00ff00", "outline_style": "no"}
            )
        )
        self.assertTrue(points_layer.dataProvider().addFeature(f))
        f.setGeometry(QgsGeometry.fromWkt("Point(-90 50)"))
        f.setEmbeddedSymbol(None)
        self.assertTrue(points_layer.dataProvider().addFeature(f))

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsMarkerSymbol.createSimple(
                {"name": "star", "size": 10, "color": "#ff00ff", "outline_style": "no"}
            )
        )
        points_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(400, 400))
        mapsettings.setOutputDpi(96)
        mapsettings.setExtent(QgsRectangle(-163, 22, -70, 52))
        mapsettings.setLayers([points_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_defaultsymbol", "embedded_defaultsymbol", mapsettings
            )
        )

    def testMapInfoLineSymbolConversion(self):
        line_layer = QgsVectorLayer(
            TEST_DATA_DIR + "/mapinfo/line_styles.TAB", "Lines", "ogr"
        )

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsLineSymbol.createSimple({})
        )
        line_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(2000, 4000))
        mapsettings.setOutputDpi(96)
        mapsettings.setMagnificationFactor(2)
        mapsettings.setExtent(line_layer.extent().buffered(0.1))

        mapsettings.setLayers([line_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_mapinfo_lines", "embedded_mapinfo_lines", mapsettings
            )
        )

    def testMapInfoFillSymbolConversion(self):
        line_layer = QgsVectorLayer(
            TEST_DATA_DIR + "/mapinfo/fill_styles.TAB", "Fills", "ogr"
        )

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsFillSymbol.createSimple({})
        )
        line_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(2000, 4000))
        mapsettings.setOutputDpi(96)
        mapsettings.setMagnificationFactor(2)
        mapsettings.setExtent(line_layer.extent().buffered(0.1))

        mapsettings.setLayers([line_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_mapinfo_fills", "embedded_mapinfo_fills", mapsettings
            )
        )

    def testMapInfoMarkerSymbolConversion(self):
        line_layer = QgsVectorLayer(
            TEST_DATA_DIR + "/mapinfo/marker_styles.TAB", "Marker", "ogr"
        )

        renderer = QgsEmbeddedSymbolRenderer(
            defaultSymbol=QgsMarkerSymbol.createSimple({})
        )
        line_layer.setRenderer(renderer)

        mapsettings = QgsMapSettings()
        mapsettings.setOutputSize(QSize(2000, 4000))
        mapsettings.setOutputDpi(96)
        mapsettings.setMagnificationFactor(2)
        mapsettings.setExtent(line_layer.extent().buffered(0.1))

        mapsettings.setLayers([line_layer])

        self.assertTrue(
            self.render_map_settings_check(
                "embedded_mapinfo_markers", "embedded_mapinfo_markers", mapsettings
            )
        )


if __name__ == "__main__":
    unittest.main()
