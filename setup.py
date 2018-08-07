import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name="PyMsu2Wav",
    version="0.0.1",
    author="fantallis",
    description="Converts MSU-1 .pmc files to RIFF .wav files",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/qadan/pymsu2wav',
    packages=setuptools.find_packages(),
    )
