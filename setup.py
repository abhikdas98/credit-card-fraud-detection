'''
This is the setup file for the credit card fraud detection project.
It is used to install the required packages and dependencies for the project.
It also finds the packages in the project and includes them in the installation process.
'''

from setuptools import setup, find_packages
from typing import List

def get_requirements()->List[str]:
    '''This function will return the list of requirements'''
    requirement_lst: List[str] = []
    try:
        with open('requirements.txt', 'r') as file:
            #Read lines from the file
            lines = file.readlines()
            #Process the lines
            for line in lines:
                requirement = line.strip()
                if requirement and requirement != '-e .':
                    requirement_lst.append(requirement)
        
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return requirement_lst

print(get_requirements())

setup(
    name='credit_card_fraud_detection',
    version='0.0.1',
    author='Abhik',
    author_email='abhikdss98123@gmail.com',
    description='A credit card fraud detection project',
    packages=find_packages(),
    install_requires=get_requirements()
)