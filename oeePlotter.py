from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QFont, QPen

class OEEPlotter:
    def __init__(self, view):
        self.view = view
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

    def plot_oee_data(self, dates, oee_values, availability_values, performance_values, quality_values):
        # Clear any existing items in the scene
        self.scene.clear()

        # Get the size of the QGraphicsView to scale the plot accordingly
        view_width = self.view.width()
        view_height = self.view.height()

        # Debugging: Check the size of the view and the input data
        print(f"View Size: {view_width}x{view_height}")
        print(f"Dates: {dates}")
        print(f"OEE Values: {oee_values}")
        print(f"Availability Values: {availability_values}")
        print(f"Performance Values: {performance_values}")
        print(f"Quality Values: {quality_values}")

        # Scaling function for dates
        def date_to_x(date):
            # Assuming the start date is the first date in the list
            start_date = dates[0]
            days_difference = start_date.daysTo(date)
            x_scale = view_width / (len(dates) - 1)  # Scale based on the number of dates minus 1
            x_pos = 50 + days_difference * x_scale  # Adding 50 for padding from the left edge
            print(f"Date: {date.toString('MMM dd')}, X: {x_pos}")  # Debugging X position
            return x_pos

        # Y-axis scaling factor (height of the view divided by 100 for percentage scaling)
        y_scale = view_height / 100  # Assuming percentage scaling (0-100%)

        # Create paths for the 4 lines (OEE, Availability, Performance, Quality)
        
        def create_path(values, color):
            # Create a path for the metric with a specified color
            path = QPainterPath()
            # Start the path with the first point
            path.moveTo(date_to_x(dates[0]), view_height - values[0] * y_scale)
            for i in range(1, len(dates)):
                # Add each subsequent point as (x, y) for the path
                path.lineTo(date_to_x(dates[i]), view_height - values[i] * y_scale)
            return path

        # Create paths for each metric
        oee_path = create_path(oee_values, QColor(0, 0, 0))  # Black for OEE
        availability_path = create_path(availability_values, QColor(0, 255, 0))  # Green for Availability
        performance_path = create_path(performance_values, QColor(0, 0, 255))  # Blue for Performance
        quality_path = create_path(quality_values, QColor(255, 0, 0))  # Red for Quality

        # Increase pen width for visibility
        pen_width = 2

        # Add the paths to the scene with the appropriate colors
        self.scene.addPath(oee_path, QPen(QColor(0, 0, 0), pen_width))  # Black for OEE
        self.scene.addPath(availability_path, QPen(QColor(0, 255, 0), pen_width))  # Green for Availability
        self.scene.addPath(performance_path, QPen(QColor(0, 0, 255), pen_width))  # Blue for Performance
        self.scene.addPath(quality_path, QPen(QColor(255, 0, 0), pen_width))  # Red for Quality

        # Add X and Y axis labels
        self.add_x_axis_labels(dates, view_width)
        self.add_y_axis_labels(view_height)

        # Add legend to the scene
        self.add_legend()

        # Adjust scene size
        self.scene.setSceneRect(0, 0, view_width + 100, view_height + 100)

        # Add a border around the scene to help with debugging visibility
        border_rect = QGraphicsRectItem(0, 0, view_width + 100, view_height + 100)
        border_rect.setPen(QPen(QColor(0, 0, 0)))  # Black border
        self.scene.addItem(border_rect)

        # Re-center the view to fit the entire scene (this step is usually not mandatory)
        self.view.setRenderHint(QPainter.Antialiasing)

    def add_x_axis_labels(self, dates, view_width):
        """Add X-axis labels (dates) below the graph."""
        for i, date in enumerate(dates):
            date_text = QGraphicsTextItem(date.toString("MMM dd"))
            x_pos = 50 + i * (view_width // (len(dates) - 1))  # X position of the date label
            date_text.setPos(x_pos, 320)  # Adjust Y position for bottom of the graph
            self.scene.addItem(date_text)

    def add_y_axis_labels(self, view_height):
        """Add Y-axis labels (percentage values) along the left side."""
        for i in range(0, 101, 10):  # Y-axis from 0 to 100 (representing percentages)
            label = QGraphicsTextItem(f"{i}%")
            label.setPos(10, view_height - i * (view_height / 100))  # Adjust Y position based on scaling
            label.setFont(QFont("Arial", 10))  # Adjust font size for readability
            self.scene.addItem(label)

    def add_legend(self):
        """Add a legend to explain the colors."""
        legend_start_x = 350
        legend_start_y = 50

        # OEE Legend (Black)
        oee_legend = QGraphicsTextItem("OEE")
        oee_legend.setPos(legend_start_x + 20, legend_start_y)
        oee_legend.setFont(QFont("Arial", 10))
        self.scene.addItem(oee_legend)
        self.scene.addRect(legend_start_x, legend_start_y, 10, 10, QPen(QColor(0, 0, 0)), QColor(0, 0, 0))

        # Availability Legend (Green)
        availability_legend = QGraphicsTextItem("Availability")
        availability_legend.setPos(legend_start_x + 20, legend_start_y + 20)
        availability_legend.setFont(QFont("Arial", 10))
        self.scene.addItem(availability_legend)
        self.scene.addRect(legend_start_x, legend_start_y + 20, 10, 10, QPen(QColor(0, 255, 0)), QColor(0, 255, 0))

        # Performance Legend (Blue)
        performance_legend = QGraphicsTextItem("Performance")
        performance_legend.setPos(legend_start_x + 20, legend_start_y + 40)
        performance_legend.setFont(QFont("Arial", 10))
        self.scene.addItem(performance_legend)
        self.scene.addRect(legend_start_x, legend_start_y + 40, 10, 10, QPen(QColor(0, 0, 255)), QColor(0, 0, 255))

        # Quality Legend (Red)
        quality_legend = QGraphicsTextItem("Quality")
        quality_legend.setPos(legend_start_x + 20, legend_start_y + 60)
        quality_legend.setFont(QFont("Arial", 10))
        self.scene.addItem(quality_legend)
        self.scene.addRect(legend_start_x, legend_start_y + 60, 10, 10, QPen(QColor(255, 0, 0)), QColor(255, 0, 0))