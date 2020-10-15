from setuptools import setup, find_packages

setup(
    name='sample_project',
    version='0.0.1',

    description="sample_project",
    license='GPLv2',

    author='Jeffrey Ness',
    author_email='jeffrey.ness@atlassian.com',

    packages=find_packages(
        exclude=['tests']
    ),

    test_suite='tests',

    install_requires=[
        'boto3'
    ],

    tests_require=[
        'moto'
    ],

    entry_points={
        'console_scripts': [
            's3 = sample_project.s3:main',
            'route53 = sample_project.route53:main'
        ]
    },
)
