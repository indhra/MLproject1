from setuptools import find_packages, setup
from typing import List
# when there is huge project having 100s dependencies
def get_requirements(file_path:str)->List[str]:
    """ this function will retun the list of requirements """
    requirements = []
    with open(file_path) as file_obj:
        requirements = ''
    
setup(
    name='mlproject',
    version='0.0.1',
    author='IndhraKiranu',
    author_email='indhrakiranu39@gmail.com',
    packages=find_packages(),
    install_requires= get_requirements('requirements.txt') #['pandas','numpy','seaborn']
)