# -*- coding: utf-8 -*-

import sys, os.path
path = os.path.expanduser('~/RandomMetroidSolver')
if os.path.exists(path) and path not in sys.path:
    sys.path.append(path)

import datetime, os, hashlib

from parameters import *
from helpers import *
from tournament_locations import *
from solver import *
from get_random_rom import *

difficulties = {
    0: 'mania',
    easy : 'easy',
    medium : 'medium',
    hard : 'hard',
    harder : 'harder',
    hardcore : 'hardcore',
    mania : 'mania'
}

difficulties2 = {
    'easy' : easy,
    'medium' : medium,
    'hard' : hard,
    'harder' : harder,
    'hardcore' : hardcore,
    'mania' : mania
}

desc = {'Mockball': {'display': 'Mockball',
                     'title': 'Early super and ice beam',
                     'href': 'http://deanyd.net/sm/index.php?title=Mockball'},
        'SimpleShortCharge': {'display': 'Simple Short Charge',
                              'title': 'Waterway ETank without gravity, and Wrecked Ship access',
                              'href': 'http://deanyd.net/sm/index.php?title=Quick_charge'},
        'InfiniteBombJump': {'display': 'Infinite Bomb Jump',
                             'title': 'To access certain locations without high jump or space jump',
                             'href': 'https://www.youtube.com/watch?v=Qfmcm7hkXP4'},
        'GreenGateGlitch': {'display': 'Green Gate Glitch',
                            'title': 'To access screw attack and crocomire',
                            'href': 'http://deanyd.net/sm/index.php?title=Gate_Glitch'},
        'ShortCharge': {'display': 'Short Charge',
                        'title': 'To kill draygon',
                        'href': 'http://deanyd.net/sm/index.php?title=Short_Charge'},
        'GravityJump': {'display': 'Gravity Jump',
                        'title': 'Super high jumps in water/lava',
                        'href': 'http://deanyd.net/sm/index.php?title=14%25#Gravity_Jump'},
        'SpringBallJump': {'display': 'Spring Ball Jump',
                           'title': 'Access to wrecked ship etank without anything else, suitless maridia navigation',
                           'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw' },
        'DraygonGrappleKill': {'display': 'Draygon Grapple Kill',
                               'title': 'n/a',
                               'href': 'https://www.youtube.com/watch?v=gcemRrXqCbE' },
        'MicrowaveDraygon': {'display': 'Microwave Draygon',
                             'title': 'Charge/Plasma/X-Ray glitch on Draygon',
                             'href': 'https://www.youtube.com/watch?v=tj0VybUH6ZY' },
        'MicrowavePhantoon': {'display': 'Microwave Phantoon',
                              'title': 'Same as Draygon, with a few missiles to start',
                              'href': None},
        'IceZebSkip': {'display': 'Ice Zeb Skip',
                       'title': 'Skip the Zebetites with Ice beam',
                       'href': 'https://www.youtube.com/watch?v=GBXi3MSpGZg' },
        'SpeedZebSkip': {'display': 'Speed Zeb Skip',
                         'title': 'Skip the Zebetites with a shinespark',
                         'href': 'https://www.youtube.com/watch?v=jEAgdWQ9kLQ' },
        'CeilingDBoost': {'display': 'Ceiling Damage Boost',
                          'title': 'Hit an enemy at the right time to get the item in Blue Brinstar Ceiling',
                          'href': 'https://www.metroid2002.com/3/early_items_blue_brinstar_energy_tank.php'},
        'AlcatrazEscape': {'display': 'Alcatraz Escape',
                           'title': 'Escape from Bomb area using its entrance tunnel',
                           'href': 'https://www.youtube.com/watch?v=XSBeLJJafjY'},
        'ReverseGateGlitch': {'display': 'Reverse Gate Glitch',
                              'title': 'Open wave gate in Pink Brinstar from bottom left corner with High Jump',
                              'href': None },
        'EarlyKraid': {'display': 'Early Kraid',
                       'title': 'Access Kraid area by wall jumping',
                       'href': None },
        'XrayDboost': {'display': 'X-Ray Damage Boost',
                       'title': 'Get to X-Ray location without Space Jump or Grapple',
                       'href': None },
        'RedTowerClimb': {'display': 'Red Tower Climb',
                          'title': 'Climb Red Tower without Ice or Screw Attack',
                          'href': None },
        'HiJumpGauntletAccess': {'display': 'Hi-Jump Gauntlet Access',
                                 'title': 'Access Gauntlet area using tricky wall jumps',
                                 'href': 'https://www.youtube.com/watch?v=2a6mf-kB60U' },
        'GauntletWithBombs': {'display': 'Gauntlet With Bombs',
                              'title': 'Traverse Gauntlet area with only bombs',
                              'href': None },
        'GauntletWithPowerBombs': {'display':
                                   'Gauntlet With Power-Bombs',
                                   'title': 'Traverse Gauntlet area with power bombs',
                                   'href': None},
        'GauntletEntrySpark': {'display': 'Gauntlet Entry Spark',
                               'title': 'n/a',
                               'href': 'https://www.youtube.com/watch?v=rFobt0S5sD4' },
        'NorfairReserveHiJump': {'display': 'Norfair Reserve Hi-Jump',
                                 'title': 'Access Norfair Reserve using just Hi Jump and wall jumping',
                                 'href': None },
        'WaveBeamWallJump': {'display': 'Wave-Beam Wall-Jump',
                             'title': 'Climb to Wave Beam with wall jumps',
                             'href': None },
        'ClimbToGrappleWithIce': {'display': 'Climb to Grapple With Ice',
                                  'title': 'Climb to Grapple Beam area using Ice Beam and bugs',
                                  'href': None },
        'LavaDive': {'display': 'Lava Dive',
                     'title': 'Enter Lower Norfair with Varia ans Hi Jump',
                     'href': 'https://www.youtube.com/watch?v=pdyBy_54dB0' },
        'WorstRoomIceCharge': {'display': 'Worst Room Ice and Charge',
                               'title': 'Go through Worst Room In The Game JUST by freezing pirates',
                               'href': 'https://www.youtube.com/watch?v=AYK7LREbLI8' },
        'WorstRoomHiJump': {'display': 'Worst Room Hi-Jump',
                            'title': 'Go through Worst Room In The Game with Hi Jump and wall jumps',
                            'href': 'https://www.youtube.com/watch?v=xyYIg7WSJ1w' },
        'ContinuousWallJump': {'display': 'Continuous Wall-Jump',
                               'title': 'Get over the moat using CWJ',
                               'href': 'https://www.youtube.com/watch?v=4HVhTwwax6g' },
        'DiagonalBombJump': {'display': 'Diagonal Bomb-Jump',
                             'title': 'Get over the moat using bomb jumps',
                             'href': 'https://www.youtube.com/watch?v=9Q8WGKCVb40' },
        'MockballWs': {'display': 'Mockball Wrecked Ship',
                       'title': 'Get over the moat using mockball and Spring Ball',
                       'href': 'https://www.youtube.com/watch?v=WYxtRF--834' },
        'SpongeBathBombJump': {'display': 'SpongeBath Bomb-Jump',
                               'title': 'Get through sponge bath room (before spiky room of death) with bomb jumps',
                               'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw' },
        'SpongeBathHiJump': {'display': 'SpongeBath Hi-Jump',
                             'title': 'Get through sponge bath room (before spiky room of death) with Hi Jump and walljumps',
                             'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw' },
        'SpongeBathSpeed': {'display': 'SpongeBath Speed',
                            'title': 'Get through sponge bath room (before spiky room of death) with Speed Boster and walljumps',
                            'href': 'https://www.youtube.com/watch?v=8ldQUIgBavw' },
        'SuitlessOuterMaridia': {'display': 'Suitless Outer Maridia',
                                 'title': 'Make your way through Maridia (up to Botwoon area) with Hi Jump, Grapple and Ice',
                                 'href': 'https://www.youtube.com/watch?v=c2xoPigezvM' },
        'SuitlessOuterMaridiaNoGuns': {'display': 'Suitless Outer Maridia with no Guns',
                                       'title': 'Same as above, but with no firepower besides Ice Beam',
                                       'href': 'https://www.youtube.com/watch?v=c2xoPigezvM' },
        'MochtroidClip': {'display': 'Mochtroid Clip',
                          'title': 'Get to Botwoon with Ice Beam',
                          'href': 'http://deanyd.net/sm/index.php?title=14%25#Mochtroid_Clip' },
        'PuyoClip': {'display': 'Puyo Clip',
                     'title': 'Get to Spring Ball with Gravity Suit and Ice Beam',
                     'href': 'https://www.youtube.com/watch?v=e5ZH_9paSLw' },
        'KillPlasmaPiratesWithSpark': {'display': 'Kill Plasma Pirates with Spark',
                                       'title': 'Use shinesparks to kill the pirates in Plasma Beam room',
                                       'href': None },
        'KillPlasmaPiratesWithCharge': {'display': 'Kill Plasma Pirates with Charge',
                                        'title': 'Use pseudo-screw to kill the pirates in Plasma Beam room',
                                        'href': None},
        'ExitPlasmaRoomHiJump': {'display': 'Exit Plasma room Hi-Jump',
                                 'title': 'Exit the Plasma room with Hi-Jump and walljumps',
                                 'href': None},
        'SuitlessSandpit': {'display': 'Suitless Sandpit',
                            'title': 'Access item in the left sandpit without Gravity',
                            'href': None}
}

usedAcrossTheGame = ['Mockball', 'SimpleShortCharge', 'InfiniteBombJump', 'GreenGateGlitch', 'ShortCharge', 'GravityJump', 'SpringBallJump']
bosses = ['DraygonGrappleKill', 'MicrowaveDraygon', 'MicrowavePhantoon']
endGame = ['IceZebSkip', 'SpeedZebSkip']
brinstar = ['CeilingDBoost', 'AlcatrazEscape', 'ReverseGateGlitch', 'EarlyKraid', 'XrayDboost', 'RedTowerClimb']
gauntlet = ['HiJumpGauntletAccess', 'GauntletWithBombs', 'GauntletWithPowerBombs', 'GauntletEntrySpark']
upperNorfair = ['NorfairReserveHiJump', 'WaveBeamWallJump', 'ClimbToGrappleWithIce']
lowerNorfair = ['LavaDive', 'WorstRoomIceCharge', 'WorstRoomHiJump']
wreckedShip = ['ContinuousWallJump', 'DiagonalBombJump', 'MockballWs']
wreckedShipEtank = ['SpongeBathBombJump', 'SpongeBathHiJump', 'SpongeBathSpeed']
maridiaSuitless = ['SuitlessOuterMaridia', 'SuitlessOuterMaridiaNoGuns']
maridiaClips = ['MochtroidClip', 'PuyoClip']
maridiaPlasmaRoom = ['KillPlasmaPiratesWithSpark', 'KillPlasmaPiratesWithCharge', 'ExitPlasmaRoomHiJump']
maridiaSandpit = ['SuitlessSandpit']

categories = [{'knows': usedAcrossTheGame, 'title': 'Used across the game'},
              {'knows': bosses, 'title': 'Bosses'},
              {'knows': endGame, 'title': 'End Game'},
              {'knows': brinstar, 'title': 'Brinstar'},
              {'knows': gauntlet, 'title': 'Gauntlet'},
              {'knows': upperNorfair, 'title': 'Upper Norfair'},
              {'knows': lowerNorfair, 'title': 'Lower Norfair'},
              {'knows': wreckedShip, 'title': 'Wrecked Ship'},
              {'knows': wreckedShipEtank, 'title': 'Wrecked Ship Etank'},
              {'knows': maridiaSuitless, 'title': 'Maridia Suitless'},
              {'knows': maridiaClips, 'title': 'Maridia Clips'},
              {'knows': maridiaPlasmaRoom, 'title': 'Maridia Plasma Room'},
              {'knows': maridiaSandpit, 'title': 'Maridia Sandpit'}]

def solver():
#    TR("difficulty_target:",
#       SELECT('easy', 'medium', 'hard', 'harder', 'hardcore', 'mania',
#              _name="difficulty_target",
#              requires=IS_IN_SET(['easy', 'medium', 'hard',
#                                  'harder', 'hardcore', 'mania']),
#              value=difficulties[Conf.difficultyTarget])))

    alreadyLoaded = False
    if session.paramsDict is not None:
        params = ParamsLoader.factory(session.paramsDict).params
        alreadyLoaded = True

    if (request.post_vars._formname is not None
        and request.post_vars._formname in ['loadform', 'saveform']
        and request.post_vars.paramsFile is not None):
        paramsFile = request.post_vars.paramsFile
        print("Use {} params from request".format(paramsFile))
    elif session.paramsFile is not None:
        paramsFile = session.paramsFile
        print("Use {} params from session".format(paramsFile))
    else:
        paramsFile = 'regular'
        print("Use {} params from default".format(paramsFile))

    if not alreadyLoaded:
        # load the presets
        params = ParamsLoader.factory('diff_presets/{}.json'.format(paramsFile)).params


    # main form
    mainTable = TABLE(TR("Tournament Rom seed: TX",
                         INPUT(_type="text",
                               _name="seed",
                               requires=IS_INT_IN_RANGE(0, 9999999, error_message = 'Seed is a number between 0 and 9999999'),
                               default=1234567)))
    mainTable.append(TR(INPUT(_type="submit",_value="Compute difficulty")))
    mainForm = FORM(mainTable, _id="mainform", _name="mainform")

    if mainForm.process(formname='mainform').accepted:
        print("mainForm is accepted")
        response.flash="main form accepted"
        session.result = compute_difficulty(mainForm.vars['seed'], request.post_vars)
        redirect(URL(r=request, f='solver'))

    # save form
    saveTable = TABLE(TR("Name of the preset:",
                         INPUT(_type="text",
                               _name="saveFile",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Preset name must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)])),
                      TR("Password:",
                         INPUT(_type="text",
                               _name="password",
                               requires=[IS_NOT_EMPTY(),
                                         IS_ALPHANUMERIC(error_message='Password must be alphanumeric and max 32 chars'), 
                                         IS_LENGTH(32)])))
    saveTable.append(TR(INPUT(_type="submit",_value="Save presets")))
    saveForm = FORM(saveTable, _id="saveform", _name="saveform")

    if saveForm.process(formname='saveform').accepted:
        print("saveForm is accepted")
        response.flash="save form accepted"

        # check if the presets file already exists
        saveFile = saveForm.vars['saveFile']
        password = saveForm.vars['password']
        passwordSHA256 = hashlib.sha256(password).hexdigest()
        fullPath = 'diff_presets/{}.json'.format(saveFile)
        if os.path.isfile(fullPath):
            # load it
            oldParams = ParamsLoader.factory(fullPath).params

            # check if password match
            if passwordSHA256 == oldParams['password']:
                # update the presets file
                paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
                paramsDict['password'] = passwordSHA256
                ParamsLoader.factory(paramsDict).dump(fullPath)
                session.paramsFile = saveFile
                redirect(URL(r=request, f='solver'))
            else:
                response.flash = "Password mismatch with existing presets file {}".format(saveFile)

        else:
            # write the presets file
            paramsDict = generate_json_from_parameters(request.post_vars, hidden=True)
            paramsDict['password'] = passwordSHA256
            ParamsLoader.factory(paramsDict).dump(fullPath)
            session.paramsFile = saveFile
            redirect(URL(r=request, f='solver'))

    # load form
    files = sorted(os.listdir('diff_presets'))
    presets = [os.path.splitext(file)[0] for file in files]

    loadTable = TABLE(TR("Choose an available preset:",
                         SELECT(*presets, **dict(_name="paramsFile", value=paramsFile))))
    loadTable.append(TR(INPUT(_type="submit",_value="Load presets")))
    loadForm = FORM(loadTable, _id="loadform", _name="loadform")

    if loadForm.process(formname='loadform').accepted:
        print("loadForm is accepted")
        response.flash="load form accepted"

        # check that the presets file exists
        paramsFile = loadForm.vars['paramsFile']
        fullPath = 'diff_presets/{}.json'.format(paramsFile)
        if os.path.isfile(fullPath):
            # load it
            params = ParamsLoader.factory(fullPath).params
            session.paramsFile = paramsFile
            # params changed, no longer display the old result to avoid confusion
            session.result = None
            session.paramsDict = None
            redirect(URL(r=request, f='solver'))
        else:
            response.flash = "Presets file not found"


    if session.result is not None:
        if session.result['difficulty'] == -1:
            resultText = "The rom \"{}\" is not finishable with the known technics".format(session.result['randomizedRom'])
        else:
            resultText = "The rom \"{}\" estimated difficulty is: {} ".format(session.result['randomizedRom'], session.result['baseDiff'])

        resultNormalized = session.result['normalized']

        # add generated path (spoiler !)
        pathTable = TABLE(TR(TH("Location Name"), TH("Area"), TH("Item"), TH("Difficulty")))
        for location, area, item, difficulty in session.result['generatedPath']:
            pathTable.append(TR(location, area, item, difficulty))
    else:
        resultText = None
        resultNormalized = None
        pathTable = None


    # send values to view
    return dict(mainForm=mainForm, loadForm=loadForm, saveForm=saveForm,
                desc=desc,
                difficulties=difficulties,
                categories=categories,
                knows=params['Knows'],
                resultText=resultText, pathTable=pathTable, resultNormalized=resultNormalized,
                easy=easy,medium=medium,hard=hard,harder=harder,hardcore=hardcore,mania=mania)

def generate_json_from_parameters(vars, hidden):
    if hidden is True:
        hidden = "_hidden"
    else:
        hidden = ""
    paramsDict = {'Conf': {}, 'Settings': {}, 'Knows': {}}
    for var in Knows.__dict__:
        # print("var={}".format(var))
        if var[0:len('__')] != '__':
            boolVar = vars[var+"_bool"+hidden]
            # print("{} = {}".format(var+"_bool"+hidden, boolVar))
            if boolVar is None:
                paramsDict['Knows'][var] = [False, 0]
            else:
                paramsDict['Knows'][var] = [True, difficulties2[vars[var+"_diff"+hidden]]]
            # print("{}: {}".format(var, paramsDict['Knows'][var]))

    return paramsDict

def compute_difficulty(seed, post_vars):
    originalRom = os.path.expanduser('~/RandomMetroidSolver/Super_Metroid_JU.smc')
    seed = '6869602'

    # generate json from rom to avoid downloading it again and again if the user is tweaking its params
    jsonFileName = 'TX' + str(seed) + '.json'

    if not os.path.isfile(jsonFileName):
        # randomized rom is downloaded in "~/web2py/" (the cwd when in web2py)
        # during development don't ask the same seed over and over again
        #randomizedRom = getRandomizedRom(originalRom, seed)
        randomizedRom = "Item Randomizer TX6869602.sfc"

        romLoader = RomLoader.factory(randomizedRom)
        romLoader.assignItems(locations)
        romLoader.dump(jsonFileName)
        os.remove(randomizedRom)
    else:
        randomizedRom = "Item Randomizer TX{}.sfc".format(seed)

    # generate json from parameters
    paramsDict = generate_json_from_parameters(post_vars, hidden=False)
    session.paramsDict = paramsDict

    # call solver
    solver = Solver(type='web', rom=jsonFileName, params=[paramsDict])
    difficulty = solver.solveRom()
    (baseDiff, normalized) = DifficultyDisplayer(difficulty).normalize()

    generatedPath = solver.getPath(solver.visitedLocations)

    return dict(randomizedRom=randomizedRom, difficulty=difficulty,
                baseDiff=baseDiff, normalized=normalized, generatedPath=generatedPath)