from setuptools import setup

setup(
    name='prlog',
    version=0.1,
    description='Retrieves and analyses github pull request log',
    author='Aryeh Leib Taurog',
    author_email='python@aryehleib.com',
    license=['BSD'],
    packages=[
        "prlog",
    ],
    zip_safe=False,
    install_requires=['requests', 'pandas', 'matplotlib'],
    entry_points={
        'console_scripts': [
            'csv_dump=prlog.csv_dump:run',
            'plot_counts=prlog.plot_counts:run',
            'csv_dump=prlog.csv_dump:run',
        ],
    },
)
