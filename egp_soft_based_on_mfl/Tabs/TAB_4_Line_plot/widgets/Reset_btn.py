def reset_btn_fun(self):
    """Reset just the LinePlotTab UI/state."""
    # Remove any drawn rectangle(s)
    ax = self.figure_x5.gca()
    for p in list(ax.patches):
        p.remove()
    self.canvas_x5.draw()

    # Clear child-owned inputs
    if hasattr(self, "latitude"):
        self.latitude.clear()
    if hasattr(self, "logitude"):
        self.logitude.clear()

    # Reset child selection state
    self.rect_start_1 = None
    self.rect_end_1 = None