from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Distort Speech"

def distortSpeechSpellCheckIfVerbal(attachee, args, evt_obj):
    spellToCheck = evt_obj.get_spell_packet()
    usedComponents = spellToCheck.get_spell_component_flags()
    print "usedComponents: {}".format(usedComponents)
    if usedComponents & SCF_VERBAL:
        args.set_arg(2,1)
    else:
        args.set_arg(2, 0)
    return 0

def distortSpeechSpellDistortCheck(attachee, args, evt_obj):
    if not args.get_arg(2): #Only spells with verbal components get distortet;
        attachee.float_text_line("Not a verbal spell")
        return 0
    distortBonusList = tpdp.BonusList()
    failDc = 51 #Distort Speech is a 50% Chance to fail spells and activate items
    failDice = dice_new('1d100')
    distortDiceResult = failDice.roll()
    distortHistory = tpdp.create_history_dc_roll(attachee, failDc, failDice, distortDiceResult, "Distort Spell Failure Check", distortBonusList)
    game.create_history_from_id(distortHistory)
    if distortDiceResult < failDc:
        evt_obj.return_val = 100
        attachee.float_text_line("Distort Speech Failure", tf_red)
        game.particles('Fizzle', attachee)
    return 0

distortSpeechSpell = PythonModifier("sp-Distort Speech", 3) # spell_id, duration, verbalComponent
distortSpeechSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, distortSpeechSpellCheckIfVerbal,())
distortSpeechSpell.AddHook(ET_OnD20Query, EK_Q_SpellInterrupted, distortSpeechSpellDistortCheck,())
distortSpeechSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
distortSpeechSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
distortSpeechSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
distortSpeechSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
distortSpeechSpell.AddSpellDispelCheckStandard()
distortSpeechSpell.AddSpellTeleportPrepareStandard()
distortSpeechSpell.AddSpellTeleportReconnectStandard()
distortSpeechSpell.AddSpellCountdownStandardHook()
