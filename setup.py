from setuptools import setup, find_packages

setup(
    name='pull-log',
    version=0.1,
    description='Retrieves and analyses github pull request log',
    author='Aryeh Leib Taurog',
    author_email='python@aryehleib.com',
    license=['BSD'],
    packages=[
        "prlog",
        "prlog.query",
    ],
    zip_safe=False,
    install_requires=['requests'],
    entry_points={
        'console_scripts': [
            # 'commandname=module.path:function'
        ],
    },
)
