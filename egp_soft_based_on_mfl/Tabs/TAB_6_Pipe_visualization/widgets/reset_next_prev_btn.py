from .Analysis_btn import pre_graph_analysis


def reset_btn_fun_pipe(self):
    if self.figure.gca().patches:
        for patch in self.figure.gca().patches:
            patch.remove()
        for text in self.figure.gca().texts:
            text.remove()
        self.canvas.draw()
        self.rect_start_pipe = None  # Store the starting point of the rectangle
        self.rect_end_pipe = None


def graph_analysis_next(self):
    current_index = self.combo_box.currentIndex()
    if current_index < self.combo_box.count() - 1:
        self.combo_box.setCurrentIndex(current_index + 1)
        pre_graph_analysis(self)

def graph_analysis_previous(self):
    current_index = self.combo_box.currentIndex()
    if current_index > 0:
        self.combo_box.setCurrentIndex(current_index - 1)
        pre_graph_analysis(self)