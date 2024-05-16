# -*- encoding: utf-8 -*-
import os
from collections import defaultdict
from typing import List
from pathlib import Path
from pydantic import BaseModel, Field, model_validator

from const import METAGPT_ROOT
from logs import logger
from utils.yaml_model import YamlModel


class TaskTypeDef(BaseModel):
    name: str
    desc: str = ""
    guidance: str = ""

'''
总计，总共完成了多少，平均完成率，平均完成量，完成最好的三家，完成最差的3个，
然后比他人，比自己
'''


class Scene(YamlModel):
    name: str = ""
    desc: str = ""
    tasks: List[TaskTypeDef] = Field(default_factory=TaskTypeDef)

    @model_validator(mode="after")
    def add_extra_tasks(self):
        other = TaskTypeDef(name="other", desc="Any tasks not in the defined categories")
        translation = TaskTypeDef(name="translation", desc="translate the result in Chinese")
        self.tasks.append(other)
        self.tasks.append(translation)
        return self

    def get_task_guidance(self, task_type_name: str) -> str:
        for tt in self.tasks:
            if tt.name == task_type_name:
                return tt.guidance
        return ""

    @classmethod
    def default(cls):
        return cls.from_yaml_file(Path(METAGPT_ROOT / "config/scenes/default.yaml"))

    @classmethod
    def from_file(cls, file_path):



class SceneRegistry(BaseModel):
    scenes: dict = {}

    @model_validator(mode="after")
    def register(self):
        scene_dir = METAGPT_ROOT / "config/scenes/"
        for file in os.listdir(scene_dir):
            filepath = os.path.join(scene_dir, file)
            self.register_scene(filepath)
        # self.scenes["default"] = Scene.default()

    def register_scene(
        self,
        scene_path,
        verbose=False,
    ):
        # scene = Scene.from_yaml_file(Path(METAGPT_ROOT / "config/scenes/bank_assessment.yaml"))
        scene = Scene.from_yaml_file(scene_path)
        scene_name = scene.name
        if self.has_scene(scene_name):
            return
        self.scenes[scene_name] = scene

        if verbose:
            logger.info(f"{scene_name} registered")

    def has_scene(self, key: str) -> bool:
        return key in self.scenes

    def get_scene(self, key) -> Scene:
        return self.scenes.get(key)

    def get_all_scenes(self) -> dict[str, Scene]:
        return self.scenes

    def get_default(self):
        return self.get_scene("default")

    def get_task_guidance(self, task_type_name: str):
        for scene_name in self.scenes:
            scene = self.scenes[scene_name]
            for tt in scene.tasks:
                if tt.name == task_type_name:
                    return tt.guidance
        return ""



# Registry instance
SCENE_REGISTRY = SceneRegistry()

