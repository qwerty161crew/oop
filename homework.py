M_IN_KM = 1000
CALORIES_MEAN_SPEED_MULTIPLIER = 18
CALORIES_MEAN_SPEED_SHIFT = 1.79


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км / ч; '
                f'Потрачено ккал: {self.calories:.3f}.')


class Training:
    """Базовый класс тренировки."""

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        LEN_STEP = 0.65
        return self.action * LEN_STEP / M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.distance / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((CALORIES_MEAN_SPEED_MULTIPLIER
                * self.speed + CALORIES_MEAN_SPEED_SHIFT)
                * self.duration / M_IN_KM)

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return (CALORIES_MEAN_SPEED_MULTIPLIER * self.speed
                + CALORIES_MEAN_SPEED_SHIFT) * \
            self.weight / M_IN_KM * (self.duration * 60)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        self.height = height
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((0.035 * self.height + ((self.speed / 3.6)**2
                / (self.weight / 100)) * 0.029 * self.height)
                * (self.duration * 60))


class Swimming(Training):
    """Тренировка: плавание."""

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool, count_pool):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_distance(self):
        return self.length_pool * self.count_pool / M_IN_KM / self.duration

    def get_mean_speed(self):
        return self.distance * self.count_pool / M_IN_KM / self.duration

    def get_spent_calories(self):
        return (self.speed + 1.1) * 2 * self.weight * self.duration


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    work = {'RUN': Running,
            'WLK': SportsWalking,
            'SWM': Swimming}
    if workout_type in work.keys():
        return work[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
