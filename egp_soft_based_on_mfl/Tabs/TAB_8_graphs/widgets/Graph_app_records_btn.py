from .graph_app_gui import GraphApp

def Graph_app(self):
    print("Loading GraphApp...")

    try:
        # Remove any existing widgets from hbox_6_graph
        while self.hbox_6_graph.count():
            child = self.hbox_6_graph.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Load GraphApp
        self.graph_app_widget = GraphApp(self)
        self.hbox_6_graph.addWidget(self.graph_app_widget)
        print("GraphApp loaded successfully.")

    except Exception as e:
        print("Error loading GraphApp:", e)