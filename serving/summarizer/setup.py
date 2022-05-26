from setuptools import find_packages, setup

setup(
    name='summarizer',
    version='0.1.0',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'flask==1.1.2',
        'tensorflow==2.7.2',
        'spacy==2.3.2',
        'pandas==1.0.5',
        'rouge-score==0.0.4',
        'boto3==1.16.48'
    ],
)