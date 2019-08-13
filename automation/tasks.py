############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
from invoke import task, context
from automation.tasks_ext import clean
from automation.tasks_ext import venv
from automation.tasks_ext import test
from automation.tasks_ext import support
from automation.tasks_ext import build_dist
from automation.tasks_ext import build_app
from automation.tasks_ext import build_dmg
from automation.tasks_ext import deploy_dist
from automation.tasks_ext import run_app
from automation.tasks_ext import run_dist


#
# defining all necessary virtual client login for building over all platforms
#

# defining environment for ubuntu
clientUbuntu = 'astro-ubuntu.fritz.box'
userUbuntu = 'mw@' + clientUbuntu
workUbuntu = userUbuntu + ':/home/mw/mountwizzard4'

# defining work environment for mate working
clientWork = 'astro-comp.fritz.box'
userWork = 'mw@' + clientWork
workWork = userWork + ':/home/mw/mountwizzard4'

# defining work environment for mate test
clientMate = 'astro-comp.fritz.box'
userMate = 'mw@' + clientMate
workMate = userMate + ':/home/mw/test'

# same for windows10 with cmd.exe as shell
clientWindows = 'astro-windows.fritz.box'
userWindows = 'mw@' + clientWindows
workWindows = userWindows + ':/Users/mw/mountwizzard4'
buildWindows = userWindows + ':/Users/mw/MountWizzard'

# same for mac
clientMAC = 'astro-mac.fritz.box'
userMAC = 'mw@' + clientMAC
workMAC = userMAC + ':/Users/mw/mountwizzard4'
buildMAC = userMAC + ':/Users/mw/MountWizzard'

# cleaning up and refactoring


def runMW(c, param):
    c.run(param, echo=True, hide='out')
    # c.run(param)


def printMW(param):
    print('\n\n\033[95m\033[1m' + param + '\033[0m\n')


@task(pre=[])
def clean_all(c):
    printMW('clean all')
    clean_mountcontrol(c)
    clean_indibase(c)
    clean_mountwizzard(c)


@task(pre=[])
def venv_all(c):
    printMW('venv all')
    venv_mac(c)
    venv_ubuntu(c)
    venv_windows(c)
    venv_work(c)


@task(pre=[])
def test_all(c):
    printMW('test all')
    test_mountcontrol(c)
    test_mountwizzard(c)


@task(pre=[])
def build_all(c):
    printMW('build all')
    build_mountcontrol(c)
    build_indibase(c)
    build_mountwizzard(c)
    build_windows_app(c)
    build_mac_app(c)


@task(pre=[])
def deploy_all(c):
    printMW('deploy all')
    deploy_ubuntu_dist(c)
    deploy_mate_dist(c)
    deploy_windows_dist(c)
    deploy_mac_dist(c)


@task(pre=[])
def run_all(c):
    printMW('run all')
    run_ubuntu_dist(c)
    run_mate_dist(c)
    run_windows_dist(c)
    run_windows_app(c)
    run_mac_dist(c)
    run_mac_app(c)
