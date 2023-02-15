class BezierCollection:
    def __init__(self):
        self.bezier_curves = []

    def add(self, bezier_curve):
        self.bezier_curves.append(bezier_curve)

    def number_of_quartets(self):
        return len(self.bezier_curves)

    def get_quartet(self, quartet_index):
        return self.bezier_curves[quartet_index]

    def get_quartet_from_time(self, time: float):
        return self.bezier_curves[int(time)]

    def give_position_is_inside_control_point(self, x, y, image_width):
        for quartet_index in range(len(self.bezier_curves)):
            result = self.bezier_curves[quartet_index].is_in_control_point(
                x, y, image_width)
            if result[0]:
                return quartet_index, result[1], True

        return -1, -1, False

    def save_control_points(self):
        with open('control_points.txt', 'w') as file:
            for quartet in self.bezier_curves:
                file.write('\n    control_point_quartet_collection.add(ControlPointQuartet(')
                for index, point in enumerate(quartet.points):
                    if index == 3:
                        file.write(f'\n        {point.x}, {point.y}')
                    else:
                        file.write(f'\n        {point.x}, {point.y},')
                file.write('))')
