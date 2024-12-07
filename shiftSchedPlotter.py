import random
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem, QGraphicsTextItem
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtGui import QColor, QFont, QPen
from datetime import datetime, timedelta

class ShiftSchedPlotter:
    def __init__(self, ui_shiftSched, firstName, lastName, employeeNumber, maxHours, minHours, start_date, end_date):
        self.ui_shiftSched = ui_shiftSched  # This is now ui_shiftSched, which is the QGraphicsView
        self.firstName = firstName
        self.lastName = lastName
        self.employeeNumber = employeeNumber
        self.maxHours = maxHours
        self.minHours = minHours
        self.start_date = start_date
        self.end_date = end_date
        self.scene = QGraphicsScene()
        self.view = ui_shiftSched  # Assuming the view object is passed correctly
        self.view.setScene(self.scene)

    def plot_shift_schedule(self):
        # Clear any existing items in the scene
        self.scene.clear()

        # Get the size of the QGraphicsView to scale the plot accordingly
        view_width = self.view.width()
        view_height = self.view.height()

        # Generate shift data based on the provided date range
        schedule_data = self.generate_shift_data(self.start_date, self.end_date, self.minHours, self.maxHours)

        # Scaling function for dates
        def date_to_x(date):
            days_difference = (date - self.start_date).days
            x_scale = view_width / (len(schedule_data) - 1)
            x_pos = 50 + days_difference * x_scale  # Padding from left edge
            return x_pos

        # Plot bars for each shift and date
        bar_width = view_width / len(schedule_data)
        max_hours_for_y_axis = 12  # Max 12 hours shift in a day

        # Scaling factor for Y-axis
        y_scale = view_height / max_hours_for_y_axis  # Scaling based on max hours

        for i, schedule in enumerate(schedule_data):
            date = schedule["date"]
            shift_info = schedule["shifts"]

            for j, (shift_name, hours) in enumerate(shift_info.items()):
                shift_y_pos = (max_hours_for_y_axis - hours) * y_scale  # Y position based on hours worked
                bar_height = hours * y_scale  # Bar height based on hours worked

                if shift_name == "Morning":
                    bar_color = QColor(255, 223, 0)  # Yellow for Morning
                elif shift_name == "Afternoon":
                    bar_color = QColor(255, 165, 0)  # Orange for Afternoon
                elif shift_name == "Night":
                    bar_color = QColor(0, 0, 255)  # Blue for Night

                # Draw the bar for the shift
                bar_rect = QGraphicsRectItem(date_to_x(date), shift_y_pos, bar_width, bar_height)
                bar_rect.setBrush(bar_color)
                self.scene.addItem(bar_rect)

        # Add X and Y axis labels
        self.add_x_axis_labels(schedule_data, view_width)
        self.add_y_axis_labels(view_height)

        # Add legend
        self.add_legend(view_width, view_height)

        # Adjust scene size
        self.scene.setSceneRect(0, 0, view_width + 100, view_height + 100)

        # Add a border around the scene for debugging
        border_rect = QGraphicsRectItem(0, 0, view_width + 100, view_height + 100)
        border_rect.setPen(QPen(QColor(0, 0, 0)))
        self.scene.addItem(border_rect)

    def add_x_axis_labels(self, schedule_data, view_width):
        """Add X-axis labels (dates) below the graph."""
        # Start from the position below the graph (adjust Y position)
        label_y_pos = 320  # You can adjust this based on your view height or desired spacing

        for i, schedule in enumerate(schedule_data):
            # Get the date text formatted as "Month Day"
            date_text = QGraphicsTextItem(schedule["date"].strftime("%b %d"))
            
            # Calculate the X position for each label based on the number of days and view width
            x_pos = 50 + i * (view_width // (len(schedule_data) - 1))
            
            # Set the position of the text (X position from `x_pos`, and the Y position from `label_y_pos`)
            date_text.setPos(x_pos, label_y_pos)
            
            # Add the date text item to the scene
            self.scene.addItem(date_text)

    def add_y_axis_labels(self, view_height):
        """Add Y-axis labels for hours along the left side."""
        max_hours_for_y_axis = 12  # Max 12 hours shift in a day
        y_scale = view_height / max_hours_for_y_axis  # Scaling based on max hours
        
        for i in range(max_hours_for_y_axis + 1):  # 0 to 12 hours
            label = QGraphicsTextItem(f"{i}")
            y_pos = view_height - (i * y_scale)  # Adjust position based on scaling
            label.setPos(10, y_pos)
            label.setFont(QFont("Arial", 10))
            self.scene.addItem(label)

    def add_legend(self, view_width, view_height):
        """Add a legend to the top right corner to explain the color codes."""
        # Shift types and their corresponding colors
        shift_types = [("Morning", QColor(255, 223, 0)), 
                       ("Afternoon", QColor(255, 165, 0)), 
                       ("Night", QColor(0, 0, 255))]

        # Position for the legend (top-right corner)
        legend_x = view_width - 120
        legend_y = 20  # Starting Y position for the legend

        # Add the legend items
        for shift_name, color in shift_types:
            # Draw colored rectangle for each shift type
            color_rect = QGraphicsRectItem(legend_x, legend_y, 15, 15)
            color_rect.setBrush(color)
            self.scene.addItem(color_rect)

            # Add the label for each shift type
            shift_label = QGraphicsTextItem(f"{shift_name}")
            shift_label.setPos(legend_x + 20, legend_y)
            shift_label.setFont(QFont("Arial", 10))
            self.scene.addItem(shift_label)

            # Adjust Y position for the next item
            legend_y += 20  # 20 pixels for spacing between legend items

    def generate_shift_data(self, start_date, end_date, min_hours, max_hours):
        """Generate simulated shift data for the given date range."""
        schedule_data = []
        total_days = (end_date - start_date).days + 1
        total_hours_needed = random.randint(min_hours, max_hours)
        current_date = start_date

        hours_left = total_hours_needed

        while current_date <= end_date:
            # Determine max hours for this day based on remaining hours
            max_hours_today = min(12, hours_left)  # Can't exceed 12 hours in a day

            # Randomly determine the number of hours for the shift
            hours_today = random.randint(1, max_hours_today)
            hours_left -= hours_today

            # Randomly choose a shift type
            shift_types = ["Morning", "Afternoon", "Night"]
            shift_type = random.choice(shift_types)

            # Assign the hours to the shift type
            shift_info = {"Morning": 0, "Afternoon": 0, "Night": 0}  # Initialize all shifts to 0
            shift_info[shift_type] = hours_today  # Assign the generated hours to the selected shift

            # Print the shift data for this day
            print(f"Date: {current_date.strftime('%Y-%m-%d')}")
            print(f"  Shift Type: {shift_type} | Hours: {hours_today}")
            print(f"  Remaining Hours: {hours_left}")
            print(f"  Total Hours for the Day: {shift_info}")

            schedule_data.append({"date": current_date, "shifts": shift_info})

            # Move to the next day
            current_date += timedelta(days=1)

        return schedule_data
