# 1. Introduction

This project is intended for CS 396 Artificial Life in Northwestern University. The project employs the structure from Ludobots and utilizes the Pyrosim package.

One approach to creating robots with optimal performance is through artificial evolution. In this experiment, we utilized this approach by allowing a computer to randomly generate robots and evolve them over hundreds of generations, with the ultimate goal of achieving good performance on a specific task. The task at hand was to move in an environment with high gravitational force (g=200), with the robot's performance determined by its absolute movement on the xy-plane. While a good performance is the desired outcome, the fitness score of task performance was used as a selection criterion during the evolution process. In this article, we will delve into the design of our experiment, including the methodology used and the results obtained. Additionally, we will discuss potential areas for improvement and future directions for this research. Finally, we will draw a conclusion based on our findings.

# 2. Project Design	
## 2.1 Body Design
For the design of our body structure, we employed a tree structure. In this structure, each node represents a cube, and each edge signifies a joint between two cubes.  To build the tree structure, we randomly determine the size of the tree by generating a random integer. Once the size is determined, the tree is built in a random fashion, following the constraint that each node can have a maximum of three children.

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225153973-9f754b01-94f6-46ab-ae8d-888be7fee83d.png">

In this section, we have discussed the original design of the robot, while the symmetry design will be presented and discussed in detail in the upcoming Experiment session.

### 2.1.1 Cubes
To create each cube in the structure, we generate random numbers between 0.1 and 2 for the length, width, and height dimensions. Additionally, there is a 50% chance that each cube will have a sensor neuron. If the cube has a sensor, it is colored green, and if not, it is colored blue.

### 2.1.2 Joints
In our design, we employed the Socket-and-Ball Implementation, which involves adding a small cube, referred to as a "ball," with a size of 0, between two adjacent cubes. This addition allows for more complex movement between the cubes. Specifically, we used two joints to connect the first cube to the "ball" and the "ball" to the second cube, respectively. These two joints have free rotation axes that are perpendicular to each other, enabling movement similar to that of human shoulders. This design has proven to perform much better than a simple joint, allowing for more realistic and intricate movements.

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225145591-fe828aeb-ef41-44dd-b0a6-c0118b4ea470.png">


## 2.2 Brain Design
To design the brain of our robot, we utilized a fully connected linear layer. The linear layer was initialized with values ranging from -1 to 1. During operation, each sensor sends its sensory value to the brain, where it is processed by the linear layer. The resulting value is then multiplied by a motor range, which we set to 0.6 for this experiment. Finally, this value is sent to each motor neuron, enabling the robot to make the corresponding movement.

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225146867-fdf5197f-444d-4057-b392-85490147efa4.png">

## 2.3 Evolution Plan Design
### 2.3.1 Mutation
Our experiment involved defining three types of mutations. The first type is the brain mutation, which involves updating a single entry in the robot's brain. The second type is the body mutation, which entails changing the shape of two cubes. Finally, we implemented the sensor swap mutation, where the sensor is moved from one cube with the sensor to another cube without it.

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225166695-3c902f16-35ef-4891-9f53-d395fda4f516.png">

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225166746-5c7f47f1-6aa0-4f7e-8ec3-ac971f765f5e.png">

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225166793-36db9c4b-8776-4ac2-a37b-af270f66da41.png">

### 2.3.2 Selection
Each individual in each generation starts as an exact copy of its parent. After undergoing mutation, it is compared to its parent. The individual with better performance is then selected to move forward to the next generation. There is no crossover involved in this process. This cycle of selection and mutation was repeated for hundreds of generations, allowing the robots to evolve and optimize their performance on the given task. Through this iterative process, we were able to observe the emergence of novel body and brain structures that enabled the robots to move in ways that were not previously possible.

# 3. Experiments
## 3.1 Brain evolution with random bodies vs. the co-evolution of bodies and brains

<img width="525" alt="image" src="https://user-images.githubusercontent.com/88709397/225153754-bdc5bfac-d1e8-41f0-a6bf-628b15cb5d31.png">

In our experiment, we had a control group where all three types of mutations were allowed to occur simultaneously. Conversely, in the test group, only one type of mutation was allowed to occur in each generation, and all three types of mutations were applied sequentially over the course of three generations.

Our hypothesis is that the test group, which underwent a more sequential mutation process, will exhibit better performance and a faster growth trend in the fitness curve. This is based on the idea that a more targeted and gradual mutation process may lead to a more efficient evolution of the robot's design.

### 3.1.1 Implemetation Details
To ensure robust results, we ran the experiment for a total of 500 generations in the control group and 1500 generations in the test group. This allowed us to observe the long-term effects of the different mutation strategies on the evolution of the robots. In the test group, we evaluate the result from each generation where the generation number is a multiple of three. This allows for a fair comparison between the control and test groups, both of which have 500 generation entries.

## 3.2 Body Design: The Original vs. The Symmetric

In the natural world, many animals exhibit some form of symmetry. This raises the question of whether symmetry is a crucial factor in the process of movement. To test this, we implemented a symmetry design where each time a cube j is added to cube i, we also add a cube -j to cube -i. Furthermore, we make sure that the new cubes grow in mirrored directions. Although this design is centered symmetric rather than axis symmetric, which is common in most animals, we still hypothesize that it will have a better performance in the end compared to the original design. However, we do not have a hypothesis for the growth rate of the fitness curve in this case.

### 3.2.1 Implemetation Details
In this experiment, we utilize the test group from 3.1 as the control group since we are implementing the coevolution concept. However, we have simplified the process by eliminating the sensor swapping mutation since it is challenging to implement in the symmetry design. As a result, the test group runs for 1000 generations, and we only evaluate every even-numbered generation.

# 4. Results
I average the fitness scores of each generation.
## 4.1 Brain evolution with random bodies vs. the co-evolution of bodies and brains

## 4.2 Body Design: The Original vs. The Symmetric

# 5. Discussion
## 5.1 Interesting Observations
The environment includes an obstacle block, which many robots in our experiment learned to push away rather than finding an alternate path. This unexpected behavior may be attributed to our greedy selection process, where the robot with the highest movement score is chosen for the next generation. Thus, if a robot learns to move towards the obstacle, its offspring are more likely to inherit this behavior and learn new pushing techniques based on it, instead of exploring easier paths.

## 5.2 Failed Trails
One of my failed design attempts involved training robots to climb a stair-like structure. However, due to the large number of cubes required to form the stairs, the training process proved to be incredibly time-consuming. As a result, I decided to abandon this approach and instead focused on creating an environment with high gravitational force.

## 5.3 Possible Improvement
### 5.3.1 More Mutations
As we have separated the body and brain evolution in our experiment, we have restricted the mutation that adds or removes body parts. This is because such changes in the body will also necessitate corresponding changes in the brain, making it difficult to use a fixed genotype to build our robot. However, introducing more flexibility in the mutation can lead to better-performing robots. If more time is allowed, this is definitely a good direction to improve our design.

### 5.3.2 Self-Intersecting
To address this issue of overlapping, we can implement a simple separation algorithm that ensures each body part is positioned at a certain distance from other body parts. This can be achieved by checking the distance between each pair of cubes and moving them away from each other if they are too close. However, this algorithm can be time-consuming as the number of cubes increases.

## 5.4 Future Work
### 5.4.1 An experiment on the brain
Recent deep learning research suggests that the model is capable of capturing the task-specific information within itself. In other words, the "brain" of our robots should encode the information about how to walk. If we extract this brain and use it as a hidden state for a new robot, and then change the environment, the new robot can quickly learn how to walk by learning a mapping to the hidden state. I find this idea intriguing and would like to explore it further in future work.

### 5.4.2 Make the improvements and Re-run this experiment
### 5.4.3 Redesign the failed trails
### 5.4.4 A further study on the interesting observations

# 6. Appendix

# 7. Reference
