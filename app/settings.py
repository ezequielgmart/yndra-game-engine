# from app.model.main_model import AppModel

from app.controller.main_controller import AppState, Application


project_json = 'app//project.json'

STATE = AppState(project_json)

APPLICATION = Application()