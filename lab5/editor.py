import csv
from shapes import Shape

class MyEditor:
    MAX_SHAPES = 127
    _instance = None

    def __init__(self):
        if MyEditor._instance is not None:
            raise RuntimeError("Використовуйте MyEditor.get_instance()")
        self.shapes: list[Shape] = []
        self._listeners = []

    @staticmethod
    def get_instance():
        if MyEditor._instance is None:
            MyEditor._instance = MyEditor()

        return MyEditor._instance
    
    @staticmethod
    def release():
        MyEditor._instance = None

    def subscribe(self, callback):
        self._listeners.append(callback)

    def unsubscribe(self, callback):
       if callback in self._listeners:
            self._listeners.remove(callback) 

    def _notify(self):
        for callback in list(self._listeners):
            callback()

    def add_shape(self, shape: Shape) -> bool:
        if len(self.shapes) >= self.MAX_SHAPES:
            return False
        
        self.shapes.append(shape)
        self._notify()
        return True
    
    def clear(self):
        self.shapes.clear()
        self._notify()

    def save_csv(self, path: str):
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")

            for shape in self.shapes:
                writer.writerow([shape.name, *shape.coords()])