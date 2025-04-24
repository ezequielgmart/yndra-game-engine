# from app.model.main_model import AppModel

from app.controller.main_controller import AppState, Application
import os


project_json = 'app//project.json'

STATE = AppState(project_json)

APPLICATION = Application()

LEVELS = [os.path.join(STATE.content['project_path'] + "\\assets\\levels\\initial_level.json")]
