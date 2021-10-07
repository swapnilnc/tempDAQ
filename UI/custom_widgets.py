from typing import List

import pyqtgraph as py_graph
from PyQt5.QtWidgets import QWidget, QGridLayout

from . import ui_graph_widget, ui_custom_progressbar_widget

# some hex colors to represent up-to 25 different plots
fav_colors = (
    '#196ab4', '#f1c232', '#f44336', '#8fce00', '#6A6A77',
    '#ff8888', '#004444', '#f44f36', '#6d1046', '#561a12',
    '#f44f36', '#33ff88', '#627582', '#758262', '#134f5c',
    '#7e707d', '#ffd700', '#ffff00', '#008000', '#4ca3dd',
    '#101010', '#0a75ad', '#81d8d0', '#ff00ff', '#0ff1ce'
)


class CustomProgressbarWidget(QWidget, ui_custom_progressbar_widget.Ui_Form):
    def __init__(self, progressbar_label: str, max_limit=100, value=0):
        super(CustomProgressbarWidget, self).__init__()
        self.setupUi(self)

        self.progressBar.setMaximum(int(max_limit))
        self.progressBar.setValue(value)
        self.label_progressbar.setText(progressbar_label)

    def update_label(self, text: str):
        self.label_progressbar.setText(text)

    def update_progressbar(self, value: float):
        self.progressBar.setValue(int(value))
        self.value_label.setText(str(value))


class CustomGraphWidget(QWidget, ui_graph_widget.Ui_Form):
    def __init__(self, title_text, x_title_text, plot_names: List):
        super(CustomGraphWidget, self).__init__()
        self.plot_names = plot_names
        self.setupUi(self)

        self.graph_widget: 'py_graph.PlotWidget' = py_graph.PlotWidget()
        self.graph_widget.showGrid(x=True, y=True, alpha=1.0)
        self.graph_widget.setTitle(title_text)
        self.graph_widget.setLabel('bottom', x_title_text)
        self.graph_widget.setBackground("#FDE3CF")  # set graph background color
        self.gridLayout_3 = QGridLayout(self.widget)
        self.widget.setLayout(self.gridLayout_3)
        self.gridLayout_3.addWidget(self.graph_widget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)

        self.plot_items = []
        self.plot_coordinates = []
        self.reset_graphs()

    def reset_graphs(self):
        """
        clear and reset all items from graph canvas
        :return:
        """
        for plot_item in self.plot_items:
            plot_item.clear()
        self.graph_widget.clear()
        self.plot_items.clear()
        self.plot_coordinates.clear()

    def add_data(self, x, y, plot_num: int = 0):
        """
        Implicitly update plot with newly received values/ add new plot values to store
        :param x: time data
        :param y: y values [List]
        :param plot_num: unique plot index
        :return: None
        """
        self.graph_widget.addLegend()
        if plot_num < len(self.plot_items):
            self.plot_coordinates[plot_num]['x'] += [x]
            self.plot_coordinates[plot_num]['y'] += [y]
            self.plot_items[plot_num].setData(self.plot_coordinates[plot_num]['x'],
                                              self.plot_coordinates[plot_num]['y'],
                                              name='N/A' if plot_num >= len(self.plot_names)
                                              else
                                              self.plot_names[plot_num])
        else:
            self.plot_coordinates.append({'x': [x], 'y': [y]})
            plot = self.graph_widget.plot([x],
                                          [y],
                                          symbol='o',
                                          symbolBrush=fav_colors[plot_num],
                                          name='N/A' if plot_num >= len(self.plot_names) else self.plot_names[plot_num])
            self.plot_items.append(plot)

    def plot(self, x, *y_values):
        """
        :param x: integer value of time intervals of n secs
        :param args: y_values for n plots
        :return: None
        """
        for index, y in enumerate(y_values[:len(self.plot_names)]):
            self.add_data(x, y, index)
