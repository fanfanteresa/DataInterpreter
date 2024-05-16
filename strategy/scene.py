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
    name: str = ""
    desc: str = ""
    guidance: str = ""


'''
总计，总共完成了多少，平均完成率，平均完成量，完成最好的三家，完成最差的3个，
然后比他人，比自己
'''


class Scene(YamlModel):
    name: str = ""
    desc: str = ""
    tasks: List[TaskTypeDef] = []

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


class SceneRegistry(BaseModel):
    scene: Scene = Field(default_factory=Scene)

    def register_scene(
            self,
            scene_path,
            verbose=False,
    ):
        scene = Scene.from_yaml_file(scene_path)
        scene_name = scene.name
        self.scene = scene

        if verbose:
            logger.info(f"Prompt file {scene_name} registered")

    def get_scene(self) -> Scene:
        return self.scene

    def get_task_guidance(self, task_type_name: str):
        for tt in self.scene.tasks:
            if tt.name == task_type_name:
                return tt.guidance
        return ""


# Registry instance
SCENE_REGISTRY = SceneRegistry()
