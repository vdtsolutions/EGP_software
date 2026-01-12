from .heatmap_generator.tab9_heatmap import tab9_heatmap

def tab9_heatmap_next(self):
    current_index = self.combo_tab9.currentIndex()
    if current_index < self.combo_tab9.count() - 1:
        self.combo_tab9.setCurrentIndex(current_index + 1)
        tab9_heatmap(self)

def tab9_heatmap_previous(self):
    current_index = self.combo_tab9.currentIndex()
    if current_index > 0:
        self.combo_tab9.setCurrentIndex(current_index - 1)
        tab9_heatmap(self)