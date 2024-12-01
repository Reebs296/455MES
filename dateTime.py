from datetime import datetime
import pytz

class DateTimeUpdater:

    def __init__(self, ui_page):
        # Accept the UI page object as a parameter
        self.ui_page = ui_page

    def update(self):
        # Get current time in UTC and convert to PST
        utc_now = datetime.now(pytz.utc)
        pst_time = utc_now.astimezone(pytz.timezone('US/Pacific'))

        # Format current date (DD/MM/YY)
        current_date = pst_time.strftime("%d/%m/%y")

        # Format current time (HH:MM:SS)
        current_time = pst_time.strftime("%H:%M:%S") + " PST"

        # Update labels if they exist
        if hasattr(self.ui_page, 'label_13') and self.ui_page.label_13:
            self.ui_page.label_13.setText(current_date)

        if hasattr(self.ui_page, 'label_14') and self.ui_page.label_14:
            self.ui_page.label_14.setText(current_time)
