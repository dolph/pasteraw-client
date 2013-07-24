import setuptools


setuptools.setup(
    name='pasteraw',
    version='1.0.0',
    description='Pipe stdin to a raw pastebin',
    author='Dolph Mathews',
    author_email='dolph.mathews@gmail.com',
    url='http://github.com/dolph/pasteraw-client',
    scripts=['pasteraw.py'],
    install_requires=['requests'],
    py_modules=['pasteraw'],
    entry_points={'console_scripts': ['pasteraw = pasteraw:cli']},
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
    ],
)
