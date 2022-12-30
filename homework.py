from dataclasses import dataclass, asdict
from typing import Sequence, Dict, Tuple, List, Type


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type, duration, distance, speed, calories):
        self.training_type: str  # Тип тренировки
        self.duration: float     # Продолжительность
        self.distance: float     # Расстояние
        self.speed: float        # Скорость
        self.calories: float     # Килокалории
        self.MESSAGE: str = (f'Тип тренировки: {training_type}; '
                             f'Длительность: {duration:.3f} ч.; '
                             f'Дистанция: {distance:.3f} км; '
                             f'Ср. скорость: {speed:.3f} км/ч; '
                             f'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    M_IN_KM: int = 1000     # Километры
    MIN_IN_H: int = 60   # Часы
    LEN_STEP: float = 0.65  # Длина шага
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self,
                 action: int,      # Действие
                 duration: float,  # Продолжительность
                 weight: float,    # Вес
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return ((self.action * self.LEN_STEP) / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.speed
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration
                * self.MIN_IN_H))

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(
            training_type=self.__class__.__name__,
            duration=self.duration,
            distance=self.get_distance(),
            speed=self.get_mean_speed(),
            calories=self.get_spent_calories()
        )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_SHIFT: float = 1.79

    def __init__(self, action: int, duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.speed
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM * (self.duration
                * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    SPENT_CALORIES_COEF_3 = 2
    KMH_IN_MSEC = 0.278
    CM_IN_M = 100

    def __init__(self, action: int, duration: float,
                 weight: float, height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        self.distance = self.get_distance()
        self.speed = self.get_mean_speed()
        self.calories = self.get_spent_calories()

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMH_IN_MSEC)
                    ** 2 / (self.height / self.CM_IN_M)) *
                 self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                 * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    KONST = 1.1
    KONST_2 = 2
    LEN_STEP = 1.38

    def __init__(self, action: int, duration: float,
                 weight: float, length_pool, count_pool):
        self.action = action
        self.duration = duration
        self.weight = weight
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_distance(self):
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self):
        distance_mtr = self.length_pool * self.count_pool
        distance__km = distance_mtr / self.M_IN_KM

        return distance__km / self.duration

    def get_spent_calories(self):
        return ((self.get_mean_speed() + self.KONST)
                * self.KONST_2 * self.weight * self.duration)


def read_package(workout_type: str, data: Sequence[int]) -> Training:
    """Прочитать данные полученные от датчиков."""

    title_of_the_workout = Dict[str, Type[Training]]

    training_name: title_of_the_workout = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type in training_name:
        return training_name[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages: Sequence[Tuple[str, List[int]]] = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
