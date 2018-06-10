# Movi't - 2017 Website

The new website for the [Movi't](https://movit.resel.fr) club, made in 2017

## Quick startup:

Install [Vagrant](https://www.vagrantup.com/) then open a terminal:

```bash
git clone http://git.ignamarte.net/Ignamarte/movit-2017.git
cd movit-2017
vagrant up
vagrant ssh
cd /movit/
python3 manage.py runserver 0.0.0.0:8000
```

Open your browser and visit **10.0.3.69:8000**, enjoy !

The vagrant development environment should provide everything you need for the project to work locally. For a production environment I strongly recommend using [a python virtual environment](https://virtualenv.pypa.io/en/stable/).

## Quick note:
Due to copyrights, the banner video is not included in the repo, be aware you have to add one manually.
