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

    def remove_shape(self, index: int):
        if 0 <= index < len(self.shapes):
            del self.shapes[index]
            self._notify()

    def save_csv(self, path: str):
        with open(path, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.writer(f, delimiter=";")

            for shape in self.shapes:
                writer.writerow([shape.name, *shape.coords()])

    def load_csv(self, path: str):
        loaded = []

        with open(path, "r", newline="", encoding="utf-8-sig") as f:
            reader = csv.reader(f, delimiter=";")
            for row in reader:
                if len(row) != 5:
                    continue

                name = row[0]
                shape_class = Shape.registry.get(name)
                if shape_class is None:
                    continue

                try: 
                    x1, y1, x2, y2 = (int(v) for v in row[1:])
                except ValueError:
                    continue
                if shape_class.click_only:
                    loaded.append(shape_class(x1, y1))
                else: 
                    loaded.append(shape_class(x1, y1, x2, y2))
                if len(loaded) >= self.MAX_SHAPES:
                    break

            self.shapes = loaded
            self._notify()

    