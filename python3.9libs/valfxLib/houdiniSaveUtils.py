#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
:module: houdiniSaveUtils
:platform: Windows
:description: Houdini increment and save module
:author: Valentin David <vdavid.pro@gmail.com>
:license: MIT License
"""
# --------------------------------------------------------------------------------------------------
# Python built-in modules import
# --------------------------------------------------------------------------------------------------
import os
import re
import logging as log

# --------------------------------------------------------------------------------------------------
# Third-party modules import
# --------------------------------------------------------------------------------------------------
import hou

# --------------------------------------------------------------------------------------------------
# Globals
# --------------------------------------------------------------------------------------------------
log.basicConfig(level='INFO')

"""With this global variable you can decide the versioning pattern you prefer
The default setting will match all of these :

propHouse_model_v104_t32.ma
propHouse_model_v4104_t5442.mb
fxSnow_fx_v4398_t01.hip
shot010_comp_v853_t94.nk

Then the best way to use it is to create a shelf tool in Houdini, 
then Ctrl+Alt+Shift+LMB on the newly created tool to assign a keyboard shortcut to it

"""
PATTERN = re.compile(r'(?P<entity>\w{3,99})(?P<task>_\w{2,99})(?P<version>_v\d{3,4})(?P<take>_t\d{2,4})(?P<extension>.\w+)')


# --------------------------------------------------------------------------------------------------
# DCC-specific definitions
# --------------------------------------------------------------------------------------------------
def getSceneName():
    """Get the current scene name and return it

    :return: Current scene name
    :rtype: str
    """
    return hou.hipFile.basename()


def getScenePath():
    """Get the current scene path and return it

    :return: Current scene path
    :rtype: str
    """
    return hou.hipFile.path()


def confirmSave(newScenePath, newSceneName):
    """Check if the file already exists and ask user to confirm if he wants to overwrite

    :param newScenePath: Path the scene would be saved to if these checks pass
    :type newScenePath: str
    :param newSceneName: Name of the new scene
    :type newSceneName: str
    :return: Whether the scene should be saved
    :rtype: bool
    """
    if os.path.isfile(newScenePath):
        confirm = hou.ui.displayConfirmation(
            text='{} already exists. Do you want to replace it?'.format(newSceneName),
            title='Overwrite hip file ?',
            suppress=hou.confirmType.OverwriteFile
        )
        if confirm == 'Yes':
            return True
        elif confirm == 'No':
            return False

    else:
        return True


def saveScene(scenePath):
    """Save a new scene with desired path

    :param scenePath: Path of the scene to save
    :type scenePath: str
    """
    hou.hipFile.save(file_name=scenePath)
    log.debug('Saved scene as : {}'.format(scenePath))


# --------------------------------------------------------------------------------------------------
# Agnostic definitions
# --------------------------------------------------------------------------------------------------
def incrementScene(scenePath, context, toIncrement='version'):
    """Increment the version or take of the scene based on current scene context

    :param scenePath: Current scene path
    :type scenePath: str
    :param context: Complete context of the scene
    :type context: re.Match
    :param toIncrement: Can be either 'version' or 'take'
    :type toIncrement: str
    """
    sceneDir = os.path.dirname(scenePath)

    if toIncrement == 'version':
        currentVersionStr = re.sub(r'_v', '', context.group('version'))
    else:
        # If it aint the version, it's the take
        currentVersionStr = re.sub(r'_t', '', context.group('take'))

    currentVersion = int(currentVersionStr)
    newVersion = currentVersion + 1
    padding = len(currentVersionStr)
    newVersion = str(newVersion).zfill(padding)

    if toIncrement == 'version':
        version = '_v{}'.format(newVersion)
        take = '_t01'
    else:
        version = context.group('version')
        take = '_t{}'.format(newVersion)

    log.debug('version : {}'.format(version))
    log.debug('take : {}'.format(take))

    # Create new name
    newSceneName = '{}{}{}{}{}'.format(
        context.group('entity'),
        context.group('task'),
        version,
        take,
        context.group('extension')
    )
    newScenePath = '{}/{}'.format(sceneDir, newSceneName)

    log.debug('newSceneName : {}'.format(newSceneName))
    log.debug('newScenePath : {}'.format(newScenePath))

    # check if the file exists
    if confirmSave(newScenePath, newSceneName):
        saveScene(newScenePath)


def getSceneContext(sceneName):
    """Given a scene name, this will return a dictionary with the context of the scene

    :param sceneName: Scene name matching the pattern
    :type sceneName: str
    :return: Context of the scene
    :rtype: re.Match
    """
    match = PATTERN.match(sceneName)

    if match is None:
        raise ValueError('Scene name does not match the desired pattern', sceneName, PATTERN)
    # TODO : instead of raising an error, we could start a function that opens a small UI to save using the pattern

    log.debug('entity : {}'.format(match.group('entity')))
    log.debug('task : {}'.format(match.group('task')))
    log.debug('version : {}'.format(match.group('version')))
    log.debug('take : {}'.format(match.group('take')))
    log.debug('extension : {}'.format(match.group('extension')))

    return match


def increment(versionOrTake):
    """This is the main function of this module and will increase the current scene version or take

    :param versionOrTake: Can be either 'version' or 'take'
    :type versionOrTake: str
    """
    sceneName = getSceneName()
    scenePath = getScenePath()
    sceneContext = getSceneContext(sceneName)
    incrementScene(scenePath, sceneContext, versionOrTake)
