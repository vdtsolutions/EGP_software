def full_screen(self):
    """Switch from Screen1 to Screen2 safely in the new UI."""
    try:
        if hasattr(self, "stack"):
            self.stack.setCurrentIndex(1)   # show tabs screen
            if hasattr(self, "menubar"):
                self.menubar.setVisible(True)
        else:
            print("⚠️ full_screen() called but no stack layout exists.")
    except Exception as e:
        print("⚠️ full_screen() failed:", e)