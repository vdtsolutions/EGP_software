from egp_soft_based_on_mfl.Tabs.TAB_8_graphs.Graph1 import GraphTab


def load_pipetally(self):
    from PyQt5.QtWidgets import QFileDialog

    file_path, _ = QFileDialog.getOpenFileName(
        self,
        "Select Pipetally File",
        "",
        "Excel Files (*.xlsx *.xls *.csv);;All Files (*)"
    )

    if not file_path:
        return

    self.pipetally = file_path
    print("Pipetally loaded:", self.pipetally)

    # Mark pipetally as loaded
    self.pipetally_loaded = True

    # -------------------------------------------------------
    # CREATE GRAPH TAB (ONLY ONCE)
    # -------------------------------------------------------
    if self.Graph1 is None:
        self.Graph1 = GraphTab(self)

        # Remove placeholder
        self.right_tabWidget.removeTab(self.graph_tab_index)

        # Insert actual GraphTab
        self.graph_tab_index = self.right_tabWidget.insertTab(
            self.graph_tab_index,
            self.Graph1,
            "Graph"
        )

        # Keep Graph tab locked initially
        self.right_tabWidget.setTabEnabled(self.graph_tab_index, False)

        print("GraphTab created and locked.")

        # -------------------------------------------------------------
        # 🔥 LATE POPULATE GRAPH TAB IF TABLES WERE ALREADY LOADED
        # -------------------------------------------------------------
        # Populate weld IDs if weld table was loaded before GraphTab creation
        if self.weld_loaded:
            try:
                weld_ids = [
                    self.tab_showData.myTableWidget.item(r, 0).text()
                    for r in range(self.tab_showData.myTableWidget.rowCount())
                ]
                self.Graph1.combo_graph.clear()
                self.Graph1.combo_graph.addItems(weld_ids)
                print("GraphTab welds populated (late-load).")
            except Exception as e:
                print("Populate graph weld failed: ", e)

        # Populate pipe IDs if pipe table was loaded before GraphTab creation
        if self.pipe_loaded and hasattr(self.Graph1, "combo_pipe"):
            try:
                pipe_ids = [
                    self.tab_showData.myTableWidget1.item(r, 0).text()
                    for r in range(self.tab_showData.myTableWidget1.rowCount())
                ]
                self.Graph1.combo_pipe.clear()
                self.Graph1.combo_pipe.addItems(pipe_ids)
                print("GraphTab pipes populated (late-load).")
            except Exception as e:
                print("Populate graph pipe failed:", e)

    # -------------------------------------------------------
    # NOW APPLY UNLOCK RULES
    # -------------------------------------------------------
    try_enable_graph_tab(self)

def try_enable_graph_tab(self):
    if self.weld_loaded and self.pipe_loaded and self.pipetally_loaded:
        self.right_tabWidget.setTabEnabled(self.graph_tab_index, True)
        print(f" heatmap_index : {self.heatmap_tab_index}")
        self.right_tabWidget.setTabEnabled(self.heatmap_tab_index, True)
        print("Graph Tab ENABLED")
    else:
        print("Graph waiting… weld:", self.weld_loaded,
              "pipe:", self.pipe_loaded,
              "pipetally:", self.pipetally_loaded)