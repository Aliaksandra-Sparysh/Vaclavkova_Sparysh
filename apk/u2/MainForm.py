
from PyQt6 import QtCore, QtGui, QtWidgets
from algorithms import *
from draw import Draw
import struct
import numpy as np
from math import *
 
class Ui_MainForm(object):
    def setupUi(self, MainForm):
        MainForm.setObjectName("MainForm")
        MainForm.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(parent=MainForm)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Canvas = Draw(parent=self.centralwidget)
        self.Canvas.setObjectName("Canvas")
        self.horizontalLayout.addWidget(self.Canvas)
        MainForm.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(parent=MainForm)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 33))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(parent=self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuSimplify = QtWidgets.QMenu(parent=self.menubar)
        self.menuSimplify.setObjectName("menuSimplify")
        self.menuView = QtWidgets.QMenu(parent=self.menubar)
        self.menuView.setObjectName("menuView")
        MainForm.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(parent=MainForm)
        self.statusbar.setObjectName("statusbar")
        MainForm.setStatusBar(self.statusbar)
        self.toolBar = QtWidgets.QToolBar(parent=MainForm)
        self.toolBar.setObjectName("toolBar")
        MainForm.addToolBar(QtCore.Qt.ToolBarArea.TopToolBarArea, self.toolBar)
        
        self.actionExit = QtGui.QAction(parent=MainForm)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("icons/exit.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionExit.setIcon(icon)
        self.actionExit.setObjectName("actionExit")
        
        self.actionMin_Bounding_Rectangle = QtGui.QAction(parent=MainForm)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("icons/maer.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionMin_Bounding_Rectangle.setIcon(icon1)
        self.actionMin_Bounding_Rectangle.setObjectName("actionMin_Bounding_Rectangle")
        
        self.actionPCAS = QtGui.QAction(parent=MainForm)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("icons/pca.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionPCAS.setIcon(icon2)
        self.actionPCAS.setObjectName("actionPCAS")
        
        self.actionClear_results = QtGui.QAction(parent=MainForm)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap("icons/clear_ch.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_results.setIcon(icon3)
        self.actionClear_results.setObjectName("actionClear_results")
        
        self.actionClear_all = QtGui.QAction(parent=MainForm)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap("icons/clear_er.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionClear_all.setIcon(icon4)
        self.actionClear_all.setObjectName("actionClear_all")
        
        self.actionLongest_Edge = QtGui.QAction(parent=MainForm)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap("icons/longestedge.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionLongest_Edge.setIcon(icon5)
        self.actionLongest_Edge.setObjectName("actionLongest_Edge")
        
        self.actionWall_Average = QtGui.QAction(parent=MainForm)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap("icons/wa.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWall_Average.setIcon(icon6)
        self.actionWall_Average.setObjectName("actionWall_Average")
        
        self.actionWeighted_bisector = QtGui.QAction(parent=MainForm)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap("icons/weightedbisector.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionWeighted_bisector.setIcon(icon7)
        self.actionWeighted_bisector.setObjectName("actionWeighted_bisector")
        
        self.actionOpen = QtGui.QAction(parent=MainForm)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap("icons/open_file.png"), QtGui.QIcon.Mode.Normal, QtGui.QIcon.State.Off)
        self.actionOpen.setIcon(icon8)
        self.actionOpen.setObjectName("actionOpen")
        
        self.actionEvaluate = QtGui.QAction(parent=MainForm)
        icon_eval = QtGui.QIcon()
        self.actionEvaluate.setObjectName("actionEvaluate")
        self.menuView.addAction(self.actionEvaluate)
        self.toolBar.addAction(self.actionEvaluate)
        
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuSimplify.addAction(self.actionMin_Bounding_Rectangle)
        self.menuSimplify.addAction(self.actionPCAS)
        self.menuSimplify.addAction(self.actionLongest_Edge)
        self.menuSimplify.addAction(self.actionWall_Average)
        self.menuSimplify.addAction(self.actionWeighted_bisector)
        self.menuView.addAction(self.actionClear_results)
        self.menuView.addAction(self.actionClear_all)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuSimplify.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionMin_Bounding_Rectangle)
        self.toolBar.addAction(self.actionPCAS)
        self.toolBar.addAction(self.actionLongest_Edge)
        self.toolBar.addAction(self.actionWall_Average)
        self.toolBar.addAction(self.actionWeighted_bisector)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionClear_results)
        self.toolBar.addAction(self.actionClear_all)
        self.toolBar.addSeparator()
         
        self.actionMin_Bounding_Rectangle.triggered.connect(self.simplifyBuildingMBRClick)
        self.actionClear_results.triggered.connect(self.clearResultsClick)
        self.actionPCAS.triggered.connect(self.simplifyBuildingPCAClick)
        self.actionWall_Average.triggered.connect(self.simplifyBuildingWallAverageClick)
        self.actionLongest_Edge.triggered.connect(self.simplifyBuildingLongestEdgeClick)
        self.actionOpen.triggered.connect(self.openFileClick)
        self.actionWeighted_bisector.triggered.connect(self.simplifyBuildingWeightedBisectorClick)
        self.actionClear_all.triggered.connect(self.clearAllClick)

        self.actionEvaluate.triggered.connect(self.evaluateEfficiencyClick)
        
        self.retranslateUi(MainForm)
        QtCore.QMetaObject.connectSlotsByName(MainForm)
         
    def simplifyBuildingMBRClick(self):
        buildings = self.Canvas.getBuildings()
        a = Algorithms()
        
        results = []
        
        for b in buildings:
            if len(b) > 2:
                mbr_res = a.simplifyBuildingMBR(b)
                #Add result into a list
                results.append(mbr_res)
                
        #Sent list to Canvas
        self.Canvas.setMBRs(results)
        
        #Repaint
        self.Canvas.repaint()

    def simplifyBuildingPCAClick(self):
        buildings = self.Canvas.getBuildings()
        a = Algorithms()
        
        results = []
        
        for b in buildings:
            if len(b) > 2:
                pca_res = a.simplifyBuildingPCA(b)
                results.append(pca_res)
                
        self.Canvas.setMBRs(results)
        self.Canvas.repaint()

    def simplifyBuildingLongestEdgeClick(self):
        buildings = self.Canvas.getBuildings()
        a = Algorithms()
        results = []
        
        for b in buildings:
            if len(b) > 2:
                res = a.simplifyBuildingLongestEdge(b)
                results.append(res)
                
        self.Canvas.setMBRs(results)
        self.Canvas.repaint()
        
    def simplifyBuildingWallAverageClick(self):
        #Handle Wall Average button click
        # Get building from canvas
        buildings = self.Canvas.getBuildings()
        a = Algorithms()
        results = []
        
        # Process each building in the set [cite: 2]
        for b in buildings:
            if len(b) > 2:
                # Run Wall Average algorithm
                res = a.simplifyBuildingWallAverage(b)
                results.append(res)
                
        # Send results back to canvas
        self.Canvas.setMBRs(results)
        self.Canvas.repaint()
        
    def simplifyBuildingWeightedBisectorClick(self):
        """Handle Weighted Bisector button click."""
        # Get all buildings from canvas
        buildings = self.Canvas.getBuildings()
        a = Algorithms()
        results = []
        
        # Process each building
        for b in buildings:
            if len(b) > 2:
                # Run Weighted Bisector algorithm
                res = a.simplifyBuildingWeightedBisector(b)
                results.append(res)
                
        # Update canvas with results
        self.Canvas.setMBRs(results)
        self.Canvas.repaint()
                     
    def clearResultsClick(self):
        self.Canvas.clearResult()
        
    def clearAllClick(self):
        # Removes all buildings and results from the canvas
        self.Canvas.clearAll()
        
    def evaluateEfficiencyClick(self):
        
        #Computes average angular deviation for all methods and shows a popup.
        
        buildings = self.Canvas.getBuildings()
        # Validation: Check if there are any buildings to process
        if not buildings or (len(buildings) == 1 and len(buildings[0]) == 0):
            self.show_error_popup("Evaluation Error", "No buildings found.")
            return

        a = Algorithms()
        # Dictionary mapping display names to algorithm methods
        methods = {
            "MBR": a.simplifyBuildingMBR,
            "PCA": a.simplifyBuildingPCA,
            "Wall Average": a.simplifyBuildingWallAverage,
            "Weighted Bisector": a.simplifyBuildingWeightedBisector,
            "Longest Edge": a.simplifyBuildingLongestEdge
        }

        report = "Average Angular Deviation (RMSE):\n\n"
        
        for name, method_func in methods.items():
            total_rms = 0
            count = 0
            
            for b in buildings:
                if len(b) > 2:
                    simplified = method_func(b)
                    # Use the error calculation from algorithms.py
                    rms = a.calculateRMSError(b, simplified)
                    total_rms += rms
                    count += 1
            
            if count > 0:
                avg_rms_deg = degrees(total_rms / count)
                report += f"{name:20}: {avg_rms_deg:>6.2f}°\n"

        # Create and display the info box
        msg = QtWidgets.QMessageBox(self.centralwidget)
        msg.setWindowTitle("Methods Efficiency Comparison")
        msg.setText(report)
        # Monospace font ensures the alignment of numbers is consistent
        msg.setStyleSheet("font-family: monospace;")
        msg.exec()
            
    def openFileClick(self):
        # Open file dialog to select a Shapefile
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(self.centralwidget, "Select a file to open","","Shapefiles (*.shp);;All Files (*)")
        if file_path:
            print(f"Successfully selected: {file_path}")
            polygons = self.getPolygonsFromSHP(file_path)
            if polygons:
                self.Canvas.loadBuildings(polygons)

    def getPolygonsFromSHP(self, file_path):
        polygons = []
        try:
            with open(file_path, "rb") as f:
                # Read the main file header
                header = f.read(100)
                # Shape type is stored at byte 32
                shape_type, = struct.unpack("<i", header[32:36])
                 
                if shape_type not in [5, 15, 25]:
                    self.show_error_popup("Data Error", "This Shapefile does not contain polygons.")
                    return None
                # Iterate through individual records in the SHP file
                while True:
                    # Each record has an 8-byte header
                    record_header = f.read(8)
                    if not record_header or len(record_header) < 8:
                        break 
                     
                    _, content_length = struct.unpack(">ii", record_header)
                    content_bytes = content_length * 2
                    record_content = f.read(content_bytes)
                    
                    # Read the shape type of the specific record 
                    rec_shape_type, = struct.unpack("<i", record_content[0:4])
                    if rec_shape_type not in [5, 15, 25]:
                        continue

                    # Extract number of parts and total number of points in the polygon
                    num_parts, num_points = struct.unpack("<ii", record_content[36:44])

                    if num_parts <= 0 or num_points <= 0:
                        continue

                    # Read indices where each part (ring) starts
                    parts_indices = list(struct.unpack(f"<{num_parts}i", record_content[44:44 + num_parts * 4]))
                    parts_indices.append(num_points)
                    points_start_index = 44 + (num_parts * 4)
                     
                    record_polygons = []
                    # Process each part of the polygon
                    for p in range(num_parts):
                        part_points = []
                        start_pt = parts_indices[p]
                        end_pt = parts_indices[p+1]
                     
                        # Extract X and Y coordinates for each point
                        for i in range(start_pt, end_pt):
                            start = points_start_index + (i * 16)
                            x, y = struct.unpack("<dd", record_content[start:start+16])
                            part_points.append([x, y])
                         
                        if len(part_points) > 0:
                            record_polygons.append(np.array(part_points))
                            
                    # Add the complete polygon to the list 
                    if record_polygons:
                        polygons.append(record_polygons)
                     
            print(f"Successfully loaded {len(polygons)} polygons")
            if len(polygons) == 0:
                self.show_error_popup("Data Error", "No valid shapes found.")
                return None
            
            # Rescale and shift data to fit the current canvas size 
            normalized_polygons = self.normalizeData(polygons, self.Canvas.width(), self.Canvas.height())
            return normalized_polygons

        except Exception as e:
            self.show_error_popup("Data Loading Error", f"Failed to load Shapefile.\nError: {str(e)}")
            return None

    def normalizeData(self, polygons_list, canvas_width, canvas_height, margin=50):
        # If no polygons were loaded, return an empty list
        if not polygons_list: return []
        all_rings = [ring for poly in polygons_list for ring in poly]
        all_points = np.vstack(all_rings)
        # Find the bounding box of the entire dataset (min/max X and Y)
        min_vals = np.min(all_points, axis=0)
        max_vals = np.max(all_points, axis=0)
        
        # Calculate the real-world width and height of the data
        data_width = max_vals[0] - min_vals[0]
        data_height = max_vals[1] - min_vals[1]
        # Prevent division by zero if all points are the same
        if data_width == 0: data_width = 1
        if data_height == 0: data_height = 1
        
        # Calculate available drawing area on the canvas
        usable_width = canvas_width - (margin * 2)
        usable_height = canvas_height - (margin * 2)
        scale = min(usable_width / data_width, usable_height / data_height) * 0.9
         
        # Calculate the size of the data after scaling
        scaled_width = data_width * scale
        scaled_height = data_height * scale
        # Calculate offsets to center the data within the canvas
        offset_x = (canvas_width - scaled_width + margin) / 2
        offset_y = (canvas_height - scaled_height + margin) / 2

        normalized_polygons = []
        for poly in polygons_list:
            normalized_poly = []
            for coords in poly:
                norm_coords = np.zeros_like(coords, dtype=float)
                # Normalize X: shift to zero, scale, and add offset
                norm_coords[:, 0] = (coords[:, 0] - min_vals[0]) * scale + offset_x
                # Normalize Y. flip the axis
                norm_coords[:, 1] = canvas_height - offset_y - ((coords[:, 1] - min_vals[1]) * scale)
                normalized_poly.append(norm_coords)
            normalized_polygons.append(normalized_poly)
             
        return normalized_polygons

    def show_error_popup(self, title, message):
        mb = QtWidgets.QMessageBox(self.centralwidget)
        mb.setWindowTitle(title)
        mb.setText(message)            
        mb.exec()

    def retranslateUi(self, MainForm):
        _translate = QtCore.QCoreApplication.translate
        MainForm.setWindowTitle(_translate("MainForm", "Simplify buildings"))
        self.menuFile.setTitle(_translate("MainForm", "File"))
        self.menuSimplify.setTitle(_translate("MainForm", "Simplify"))
        self.menuView.setTitle(_translate("MainForm", "View"))
        self.toolBar.setWindowTitle(_translate("MainForm", "toolBar"))
        self.actionExit.setText(_translate("MainForm", "Exit"))
        self.actionExit.setToolTip(_translate("MainForm", "Close application"))
        self.actionMin_Bounding_Rectangle.setText(_translate("MainForm", "Min. Bounding Rectangle"))
        self.actionMin_Bounding_Rectangle.setToolTip(_translate("MainForm", "Simplify building using minimum bounding rectangle"))
        self.actionPCAS.setText(_translate("MainForm", "PCA"))
        self.actionPCAS.setToolTip(_translate("MainForm", "Simplify building using PCA"))
        self.actionClear_results.setText(_translate("MainForm", "Clear results"))
        self.actionClear_all.setText(_translate("MainForm", "Clear all"))
        self.actionClear_all.setToolTip(_translate("MainForm", "Clear all data"))
        self.actionLongest_Edge.setText(_translate("MainForm", "Longest Edge"))
        self.actionLongest_Edge.setToolTip(_translate("MainForm", "Simplify building using PCA longest edge"))
        self.actionWall_Average.setText(_translate("MainForm", "Wall Average"))
        self.actionWall_Average.setToolTip(_translate("MainForm", "Simplify building using wall average"))
        self.actionWeighted_bisector.setText(_translate("MainForm", "Weighted Bisector"))
        self.actionWeighted_bisector.setToolTip(_translate("MainForm", "Simplify building using weighted bisector"))
        self.actionOpen.setText(_translate("MainForm", "Open"))
        self.actionOpen.setToolTip(_translate("MainForm", "Open file"))
        self.actionEvaluate.setText(_translate("MainForm", "Evaluate Efficiency"))
        self.actionEvaluate.setToolTip(_translate("MainForm", "Compare all methods using RMSE"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainForm = QtWidgets.QMainWindow()
    ui = Ui_MainForm()
    ui.setupUi(MainForm)
    MainForm.show()
    sys.exit(app.exec())