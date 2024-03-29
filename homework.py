from dataclasses import dataclass, asdict
from typing import Type, Dict


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    MESSAGE = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.'
    )

    def get_message(self) -> str:
        return self.MESSAGE.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    MIN_IN_H = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories()
                           )


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79

    def get_spent_calories(self):
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER
                * self.get_mean_speed()
                + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight
                / self.M_IN_KM
                * (self.duration * self.MIN_IN_H))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER = 0.035
    CALORIES_SPEED_HEIGHT_MULTIPLIER = 0.029
    CM_IN_M = 100
    KMH_IN_MSEC = round(Training.M_IN_KM
                        / (Training.MIN_IN_H * Training.MIN_IN_H), 3)

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_WEIGHT_MULTIPLIER * self.weight
                + ((self.get_mean_speed() * round(self.KMH_IN_MSEC, 3))**2
                   / (self.height / self.CM_IN_M))
                * self.CALORIES_SPEED_HEIGHT_MULTIPLIER
                * self.weight) * self.duration * self.MIN_IN_H)


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    СALORIES_SPEED_MULTIPLIER = 1.1
    COEFF_COUNT_СALORIES = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.СALORIES_SPEED_MULTIPLIER)
                * self.COEFF_COUNT_СALORIES * self.weight * self.duration)


TRAININGS: Dict[str, Type[Training]] = {
    'SWM': (Swimming, 5),
    'RUN': (Running, 3),
    'WLK': (SportsWalking, 4)
}


def read_package(workout_type: str, data) -> Training:
    """Прочитать данные полученные от датчиков."""

    if workout_type not in TRAININGS:
        raise ValueError(f"Неправильный тип тренировки\n"
                         f"Возможные названия тренировок: {workout_type}")

    if TRAININGS[workout_type][1] != len(data):
        raise ValueError(f'Неправильный тип данных: '
                         f'{TRAININGS[workout_type][1]}.'
                         'Такая тренировка не поддерживается'
                         f'У вас некорректные данные: {len(data)}.'
                         'Чиловые данные могут быть от 3 до 5')

    return TRAININGS[workout_type][0](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLR', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        main(read_package(workout_type, data))
