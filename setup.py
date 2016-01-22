from setuptools import setup

setup(
    name='ansimp_le',
    version='0.0',
    description=(
        'A Ansible Module for simp_le',
        'The Simple Let\'s Encrypt Client.'
    )
    url='http://github.com/hashfyre/ansimp_le',
    author='Joy Bhattacherjee',
    author_email='joy.bhattacherjee@gmail.com',
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'License :: OSI Approved :: MIT License'
    ],
    packages=['ansimp_le'],
    keywords='ansible letsencrypt simp_le',
    install_requires=[],
    entry_points={
        'console_scripts': [
            'ansimp_le=ansimp_le:main',
        ],
    }
)
