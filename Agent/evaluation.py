import sys
import imageio
import os 

def evaluate_policy(agent, env):
    rewards = 0  # Variable to track the cumulative rewards during evaluation
    obs = env.reset()  # Reset the environment and get the initial observation
    done = False  # Flag to track if the episode is done
    score = 0  # Variable to track the total score achieved
    filename = "results/score_.gif"  # Filename for saving the evaluation frames as a GIF
    with imageio.get_writer(filename, mode='I', duration=50, quantizer='nq', subrectangles=True) as writer:  # Open the GIF writer with lower fps (e.g., 10)
        while not done:
            action = agent.act(obs, None, exploration=False)  # Select an action using the agent's policy
            obs, reward, done, _ = env.step(action)  # Take a step in the environment using the selected action
            rewards += reward  # Accumulate the reward
            writer.append_data(env.get_image_array_from_game())  # Save the current frame to the GIF
    print("----------------------------------------------")
    print("Total score achieved: %f" % env.score)  # Print the total score achieved in the evaluation
    print("----------------------------------------------")
    new_filename = "results/score_{}.gif".format(env.score)  # Update the filename with the final score
    os.rename(filename, new_filename)  # Rename the file with the updated filename
    return rewards  # Return the accumulated rewards for the evaluation
