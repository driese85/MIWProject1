# import libraries
import click
from art import text2art
from colorama import Fore
from colorama import init as colorama_init
import numpy as np
import pandas as pd
import pickle
import logging

""" CLI app using click and art libraries """
# init colorama
colorama_init(autoreset=True)

# Logging config
FORMAT = '%(asctime)s | %(message)s'
logging.basicConfig(format=FORMAT, level=logging.INFO)

# load the pipeline from disk
logging.info("Loading model from file...")
filename = 'run/cli/data/finalized_model.pkl'
model = pickle.load(open(filename, 'rb'))

def prompt_param(message, acceptable_range, input_type, default):
    """Function to prompt for parameters

    Args:
        message (str): message to show in prompt
        acceptable_range (tuple(int, int)): acceptable range for input
        input_type (type): type to accept as input
        default (int): default value to accept as prompt

    Returns:
        float: entered value by user
    """

    while True:
        param = click.prompt(f'Patient\'s {message} | default:', type=input_type, default=default)
        # check if input is in predefined range
        if acceptable_range[0] <= param <= acceptable_range[1]:
            break
        # else ask user to provide input in between range
        else:
            click.echo(f"Please provide a number between {str(acceptable_range[0])} and {str(acceptable_range[1])}.")
    return float(param)

# init and run click
@click.command()
def makeCLI():
    """Creating the CLI app"""
     # Compose and format output text
    artl1 = text2art("Make IT Work", font='small',)
    artl2 = text2art("health app", font='c_ascii')
    print(f"{Fore.BLUE}{artl1}")
    print(f"{Fore.BLUE}{artl2}")

    # Ask for user to continue
    click.pause()

    # Clear terminal
    click.clear()

    # Ask to enter parameters
    enter_params = "Enter the following parameters to predict the lifespan:"
    print(f"{Fore.LIGHTRED_EX}{enter_params}")

    # Define allowed ranges for user input
    parameters_prompts = dict()
    entered_parameters = dict()
    parameters_prompts['genetic'] = ["genetic age", (60, 110), int, 85]
    parameters_prompts['length'] = ["length in cm", (150, 215), int, 185]
    parameters_prompts['mass'] = ["weight in kg", (50, 165), float, 80]
    parameters_prompts['exercise'] = ["exercise in hr/day", (0, 8), float, 2]
    parameters_prompts['alcohol'] = ["alcohol in glasses/day", (0, 10), int, 0]
    parameters_prompts['smoking'] = ["smoking in cig./day", (0, 25), int, 0]
    parameters_prompts['sugar'] = ["sugar in cubes/day", (0, 15), float, 4]
    
    # loop over all parameters to prompt to user
    for k, v in parameters_prompts.items():
        entered_parameters[k] = prompt_param(v[0], v[1], v[2], v[3])
    
    # Calculate bmi and power transforms
    entered_parameters['bmi'] = entered_parameters['mass'] / (entered_parameters['length']/100)**2
    entered_parameters['mass_square'] = entered_parameters['mass']**2
    entered_parameters['bmi_square'] = entered_parameters['bmi']**2
    entered_parameters['exercise_sqrt'] = np.power(entered_parameters['exercise'], 1/2)

    # remove mass from dict
    entered_parameters.pop('mass')

    # Convert dict to dataframe
    params_df = pd.DataFrame(entered_parameters, index=[0])

    # Reorder columns to match trained model
    params_df = params_df.reindex(columns=['genetic', 'length', 'bmi', 'exercise', 'smoking', 'alcohol', 'sugar', 'mass_square', 'bmi_square', 'exercise_sqrt'])
    
    # make a prediction based on the parameters given by the user
    
    prediction = model.predict(params_df)
    logging.info("Making a prediction...")
    # send the prediction back to the user
    click.echo(f"\nBased on the given parameters, the predicted lifespan is: \033[1m{Fore.GREEN}{round(prediction[0], 1)}\033[1m")

if __name__ == '__main__':
    makeCLI()