import config


# Examples: https://doc.qt.io/qt-5/stylesheet-examples.html

def defineStyle():

    if config.menuLayout == "material" and config.qtMaterial:
        config.theme = "dark" if config.qtMaterialTheme.startswith("dark_") else "default"
        config.qtMaterial = False

    config.materialStyle = """

QLabel {0} color: {3}; {1}

QPushButton {0}background-color: {2}; color: {3};{1} QPushButton:hover {0}background-color: {4}; color: {5};{1} QPushButton:pressed {0}background-color: {6}; color: {7}{1}

QComboBox {0}background-color: {2}; color: {3}; {1} 
QComboBox:hover {0}background-color: {4}; color: {5}; {1}
QComboBox QAbstractItemView {0}background-color: {2}; color: {3}; {1} 

QRadioButton {0}background-color: {2}; color: {3}; {1}
QRadioButton:hover {0}background-color: {4}; color: {5}; {1}
QRadioButton:checked {0}background-color: {6}; color: {7}; {1}

QCheckBox {0} background-color: {2}; color: {3}; {1}
QCheckBox:hover {0} background-color: {4}; color: {5}; {1}
QCheckBox:checked {0} background-color: {6}; color: {7}; {1}

QTableView {0}
    selection-background-color: {4};
    selection-color: {5};
{1}

QHeaderView::section {0}
    background-color: {2};
    color: {3};
{1}

QLineEdit {0}
    border: 2px solid {4};
    border-radius: 10px;
    padding: 0 8px;
    background: {2};
    color: {3};
    selection-background-color: {6};
    selection-color: {7};
{1}

/* Style the tab using the tab sub-control. Note that
    it reads QTabBar _not_ QTabWidget */
QTabWidget::tab-bar {0}
    left: 2px; /* move to the right by 2px */
{1}

QTabBar::tab {0}
    background-color: {2};
    color: {3};
    border: 2px solid {2};
    border-bottom-color: {3};
    border-top-left-radius: 4px;
    border-top-right-radius: 4px;
    min-width: 8ex;
    padding: 2px;
{1}

QTabBar::tab:hover {0}
    background-color: {4};
    color: {5};
    border: 2px solid {4};
    border-bottom-color: {5};
{1}

QTabBar::tab:selected {0}
    background-color: {6};
    color: {7};
    border-color: {7};
    border-bottom-color: {6};
{1}

QTabBar::tab:!selected {0}
    margin-top: 2px; /* make non-selected tabs look smaller */
{1}

QMenu {0}
    background-color: {2}; /* sets background of the menu */
    color: {3};
    border: 1px solid {4};
{1}

QMenu::item {0}
    /* sets background of menu item. set this to something non-transparent
        if you want menu color and menu item color to be different */
    background-color: transparent;
{1}

QMenu::item:selected {0} /* when user selects item using mouse or keyboard */
    background-color: {4};
    color: {5};
{1}

QMenuBar {0}
    background-color: {2};
    color: {3};
    spacing: 3px; /* spacing between menu bar items */
{1}

QMenuBar::item {0}
    padding: 1px 4px;
    background: transparent;
    border-radius: 4px;
{1}

QMenuBar::item:selected {0} /* when selected using mouse or keyboard */
    background: {4};
    color: {5};
{1}

QMenuBar::item:pressed {0}
    background: {6};
    color: {7};
{1}

QProgressBar {0}
    border: 2px solid {4};
    border-radius: 5px;
    text-align: center;
{1}

QProgressBar::chunk {0}
    background-color: {7};
    color: {6};
    width: 20px;
{1}

QSplitter::handle {0}
    background-color: {2};
{1}

QSplitter::handle:hover {0}
    background-color: {4};
{1}

QSplitter::handle:pressed {0}
    background-color: {6};
{1}

QGroupBox::title {0}
    color: {3};
{1}

    """.format(
        "{",
        "}",
        config.widgetBackgroundColor,
        config.widgetForegroundColor,
        config.widgetBackgroundColorHover,
        config.widgetForegroundColorHover,
        config.widgetBackgroundColorPressed,
        config.widgetForegroundColorPressed
        )

config.defineStyle = defineStyle