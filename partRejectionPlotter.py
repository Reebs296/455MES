from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QColor, QFont, QPen

class RejectionPlotter:
    def __init__(self, view):
        self.view = view
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

    def plot_rejected_parts(self, intervals, rejected_parts):
        # Clear any existing items in the scene
        self.scene.clear()

        # Get the size of the QGraphicsView
        view_width = self.view.width()
        view_height = self.view.height()

        # Debugging
        print(f"View Size: {view_width}x{view_height}")
        print(f"Intervals: {intervals}")
        print(f"Rejected Parts: {rejected_parts}")

        # Flatten rejected_parts and find the max rejection value
        all_rejections = [rejection for sublist in rejected_parts for rejection in sublist]
        max_rejections = max(all_rejections)  # Find max rejection across all intervals

        y_scale = view_height / max_rejections  # Scale bars based on max rejection value

        # Bar chart configuration
        bar_width = view_width // len(intervals)  # Adjust width to fit each interval

        # Plot bars for each interval
        for i, (interval, rejection) in enumerate(zip(intervals, rejected_parts)):
            # Since each interval has one rejection value, take the first value in the list for that interval
            rejection_value = rejection[0]  # Only plot the first rejection value for each interval

            # Calculate bar dimensions
            bar_height = rejection_value * y_scale
            x_pos = i * bar_width  # Space each bar equally along the X-axis
            y_pos = view_height - bar_height  # Position bar from bottom of the view

            # Create a bar item
            bar = QGraphicsRectItem(x_pos, y_pos, bar_width, bar_height)
            bar.setBrush(QColor(100, 150, 200))  # Light blue for bars
            self.scene.addItem(bar)

            # Add value label on top of the bar
            value_label = QGraphicsTextItem(str(rejection_value))
            value_label.setFont(QFont("Arial", 10))
            value_label.setPos(x_pos + bar_width / 4, y_pos - 20)  # Adjust label position
            self.scene.addItem(value_label)

        # Add Y-axis labels
        self.add_y_axis_labels(view_height, max_rejections)

        # Adjust scene size
        self.scene.setSceneRect(0, 0, view_width, view_height + 50)

    def add_y_axis_labels(self, view_height, max_rejections):
        """Add Y-axis labels along the left side."""
        step = max_rejections // 5  # Divide the range into 5 steps
        for i in range(0, max_rejections + 1, step):
            label = QGraphicsTextItem(str(i))
            label.setFont(QFont("Arial", 10))
            y_pos = view_height - i * (view_height / max_rejections)  # Position based on scaling
            label.setPos(10, y_pos - 10)  # Offset for alignment
            self.scene.addItem(label)
