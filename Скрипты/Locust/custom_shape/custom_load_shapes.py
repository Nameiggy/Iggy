from locust import LoadTestShape
from config.config import cfg, logger


class MyCustomLoadShape(LoadTestShape):

    stages = [] # объявлем переменную со стейджами

    if cfg.loadshape.stages_count == 1: # если ступень в env одна - формируем просто одну stage (постоянная нагрузка)
        logger.info(f"CustomLoadShape with {cfg.loadshape.stages_count} stages")

        stages = [
            {"duration": cfg.loadshape.duration, "users": cfg.loadshape.users, "spawn_rate": cfg.loadshape.spawn_rate}
        ]

        print(stages)

    else: # в противном случае, выполняем данный блок
        logger.info(f"CustomLoadShape with {cfg.loadshape.stages_count} stages")

        stages_count = cfg.loadshape.stages_count
        step_duration = cfg.loadshape.duration
        step_users = cfg.loadshape.users
        spawn_rate = cfg.loadshape.spawn_rate

        duration_counter = cfg.loadshape.duration
        users_counter = cfg.loadshape.users

        stages.append({"duration": step_duration, "users": step_users, "spawn_rate": spawn_rate}) # формируем первую ступень из параметров заданных в env

        for i in range(stages_count-1): # для оставшихся stages_count - 1 (так как первую уже сформировали) формируем stage и складываем в лист stages
            duration_counter += step_duration
            users_counter += step_users
            
            stages.append({"duration": duration_counter, "users": users_counter, "spawn_rate": spawn_rate})

        print(stages)

    def tick(self): # стандартная функция локаста, взятая из документации, для работы с кастомными "Лоад-Шейпами"
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None