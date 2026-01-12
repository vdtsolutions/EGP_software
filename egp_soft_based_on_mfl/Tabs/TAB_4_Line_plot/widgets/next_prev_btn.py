from .Linechart_countervSensor_btn import Line_chart1


def Line_chart1_next(self):
    current_index = self.combo.currentIndex()
    if current_index < self.combo.count() - 1:
        self.combo.setCurrentIndex(current_index + 1)
        Line_chart1(self)


def Line_chart1_previous(self):
    current_index = self.combo.currentIndex()
    if current_index > 0:
        self.combo.setCurrentIndex(current_index - 1)
        Line_chart1(self)