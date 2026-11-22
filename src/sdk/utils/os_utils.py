import json
import sys 
import os 
# from typing import Any 
from typing import Any, Dict



class OsHandler: 

    # TODO: change to a level schema 
    def read_json_file(self, json_file:str) -> Dict[str, Any] :
        """
        Read a JSON file and return its content as a dictionary.

        Args:
            json_file (str): Path to the JSON file to read.

        Returns:
            dict: The parsed JSON content.
        """
        with open(json_file, "r") as f:
            data = json.load(f)

        return data

    def check_script_is_on_pythonpath(self, script_path:str) -> None: 

        script_dir:str = os.path.dirname(script_path)

        if script_dir and script_dir not in sys.path:
            sys.path.append(script_dir)

        return None

