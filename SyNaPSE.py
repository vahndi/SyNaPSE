import enaml
from enaml.qt.qt_application import QtApplication


# TODO: import user_views.py and user_models.py to make it extensible, or a 
#       list of files given in a text file


if __name__ == '__main__' and __package__ is None:

    from os import sys, path
    sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))


if __name__ == '__main__':

    with enaml.imports():
        from models_views.Main import Main_View

    app = QtApplication()
    view = Main_View()
    view.show()
    app.start()
