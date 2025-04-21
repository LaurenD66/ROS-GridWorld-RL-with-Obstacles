# ROS GridWorld Reinforcement Learning Project: 
## Pick and Place with Various Obstacle Behaviors

Construction environments can be chaotic, making robotic automation difficult. This project is intended to introduce reinforcement learning training and testing using to robotic movement using ROS (Robot Operating System), Gymnasium environments, and Docker to optimize robotic movement around various obstacle conditions.

## Step-by-Step Workflow

### Step 1: Setup the Workspace

Ensure your workspace structure is as follows:
```
dev_ws/
└── src/
    └── gridworld_agent/
        ├── scripts/ 
        │   └── node_01.py
        ├── src/
        │   ├── __init__.py
        │   ├── grid_world_env.py
        │   ├── obstacle_clustering.py
        │   ├── moving_obstacles.py
        │   ├── reward_shaping.py
        │   └── training_utils.py
        ├── package.xml
        └── CMakeLists.txt
```
Fork / clone grid_world_env.py from https://github.com/michelecobelli/Reinforcement-Learning-for-Robotic-Pick-and-Place.

### Step 2: Create Docker Environment 

Fork / Clone from https://github.com/MRAC-IAAC/ros-introduction to set up a virtual Docker environment.

Prior to building the docker in the terminal,

    (1) rename image file from "ros-introduction" to the name of the training file, "node.01":  latest in the build_image.sh and run_user.sh files.

    (2) add all relevant libraries (rospy, gymnasium, pygame, etc.) to the Dockerfile.

```bash
ros_obstacles/gridworld_agent/scripts/chmod +x node_01.py

...or... 

    Build your Docker image with necessary dependencies:
    ```bash
    docker build -t ros_gridworld .
    ```

    Run and enter the Docker container environment:
    ```bash
    docker run -it --rm ros_gridworld bash
    ```

    Inside Docker, build and source your ROS workspace:
    ```bash
    source /opt/ros/noetic/setup.bash
    cd /dev_ws
    catkin build
    source devel/setup.bash
    ```

### Step 3: Train your RL Agent

Inside the container shell, initiate training:
```bash
rosrun gridworld_agent node_01.py _train_mode:=true _env_variant:=original
```

This will:
- Start the training mode
- Select the original environment variant
- Save the trained Q-table (`q_table.yaml`)

### Step 4: Evaluate/Test your RL Agent

After training, evaluate the trained agent:
```bash
rosrun gridworld_agent node_01.py _train_mode:=false _env_variant:=original
```

This will:
- Load the saved Q-table (`q_table.yaml`)
- Evaluate the agent's performance
- Output the path taken by the agent

### Step 5: Experiment with Environment Variants 

You can test different environment configurations:
- Clustered obstacles: `_env_variant:=clustered`
- Moving obstacles: `_env_variant:=moving`
- Reward shaping: `_env_variant:=shaped`

Example:
```bash
rosrun gridworld_agent node_01.py _train_mode:=false _env_variant:=moving
```

### Step 6: Results and Visualization 

Use provided utilities in `training_utils.py` to:
- Generate videos of agent performance
- Analyze evaluation paths and results

---

## Common Issues

Downloading gymnasium-1.1.1-py3-none.any.whl
    - **ERROR: Could not find a version that satisfied the requirement rospy (from versions: none).
    - **ERROR: No matching distribution found for rospy

    These errors represent an incompatability between ROS1 and gymnasium.  While these files were RUN in the Docker added to the Dockerfile, they were not recognized when the docker was built and the development workspace was run in the ROS terminator.

---

## Recommended Workflow

Always perform training and evaluation inside Docker for best results:

```bash
docker run -it --rm ros_gridworld bash

# Inside Docker:
source /opt/ros/noetic/setup.bash
source /dev_ws/devel/setup.bash

# Train agent
rosrun gridworld_agent node_01.py _train_mode:=true _env_variant:=original

# Evaluate agent
rosrun gridworld_agent node_01.py _train_mode:=false _env_variant:=original
```

---

## Conclusion

This structured guide is intended to train, evaluated, and experiment with reinforcement learning agents using ROS, Gymnasium, and Docker.  The 