from .LineChart_draw import Line_chart_orientation

def Line_chart_orientation_next(self):
    current_index = self.combo_orientation.currentIndex()
    if current_index < self.combo_orientation.count() - 1:
        self.combo_orientation.setCurrentIndex(current_index + 1)
        Line_chart_orientation(self)


def Line_chart_orientation_previous(self):
    current_index = self.combo_orientation.currentIndex()
    if current_index > 0:
        self.combo_orientation.setCurrentIndex(current_index - 1)
        Line_chart_orientation(self)