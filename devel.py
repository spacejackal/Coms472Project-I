import numpy as np
import scipy

from main import Task

# example of testing a specific task
id = 13
T = Task(id)                # initialize task
T.plan_path()               # path planning
T.visualize_path()          # path visualization
print (T.check_path())      # the validity check of the generated path

# for id in range(0,99):
#     T = Task(id)                # initialize task
#     T.plan_path()               # path planning
#     T.visualize_path()          # path visualization
#     print (T.check_path())      # the validity check of the generated path