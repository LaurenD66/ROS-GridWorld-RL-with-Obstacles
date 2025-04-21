#!/usr/bin/env python3
import rospy
import numpy as np
import os
import sys

# Correctly add Python module path dynamically
script_dir = os.path.dirname(os.path.realpath(__file__))
module_dir = os.path.join(script_dir, '..', 'src')
sys.path.insert(0, module_dir)

# Now correctly import modules
from grid_world_env import GridWorldEnv
from obstacle_clustering import ObstacleClusteringMixin
from moving_obstacles import MovingObstaclesMixin
from reward_shaping import RewardShapingMixin
from training_utils import QLearningAgent, load_q_table_from_yaml, save_q_table_to_yaml

def get_env(variant):
    if variant == "clustered":
        class ClusteredEnv(ObstacleClusteringMixin, GridWorldEnv): pass
        return ClusteredEnv()
    elif variant == "moving":
        class MovingEnv(MovingObstaclesMixin, GridWorldEnv): pass
        return MovingEnv()
    elif variant == "shaped":
        class ShapedEnv(RewardShapingMixin, GridWorldEnv): pass
        return ShapedEnv()
    return GridWorldEnv(render_mode="human")

if __name__ == "__main__":
    rospy.init_node("q_learning_gridworld_node")
    train_mode = rospy.get_param("~train_mode", True)
    variant = rospy.get_param("~env_variant", "original")

    render_mode = "human" if not train_mode else None
    env = get_env(variant)
    env.render_mode = render_mode

    agent = QLearningAgent(env)

    if train_mode:
        agent.train()
        save_q_table_to_yaml(agent.q_table)
        rospy.loginfo("✅ Training complete and Q-table saved.")
    else:
        agent.load("q_table.yaml")
        result = agent.evaluate()
        rospy.loginfo(f"✅ Evaluation path: {result[0]}")

