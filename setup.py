from setuptools import setup

setup(
    name        ='material_ui',
    version     ='0.1.1',
    description ='Material UI for Kivy.',
    url         ='https://github.com/Cuuuurzel/kivy-material-ui',
    author      ='Federico Curzel',
    author_email='cuuuurzel@gmail.com',
    packages    =['material_ui.flatui', 'material_ui.navigation'],
    zip_safe    =False,
#    install_requires=['kivy'],
    include_package_data=True,
)
