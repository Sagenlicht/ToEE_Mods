from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Distort Speech"

def distortSpeechSpellCheckIfVerbal(attachee, args, evt_obj):
    #Atm it is not possibly to read components
    #spellToCheck = evt_obj.get_spell_packet()
    #sTC_spell_enum = spellToCheck.spell_enum
    #if (sTC_spell_enum == 0):
    #    return 0
    #sTC_spell_entry = tpdp.SpellEntry(sTC_spell_enum)
    #checkComponents = sTC_spell_entry.components      -- not possible atm!
    #if checkComponents == :
    args.set_arg(2,1) #Set ComponentsUseV
    #else:
        #args.set_arg(2,0)
    return 0

def distortSpeechSpellDistortCheck(attachee, args, evt_obj):
    if not args.get_arg(2) == 1: #Only spells with verbal components get distortet;
        attachee.float_text_line("Not a verbal spell")
        return 0

    failDice = dice_new('1d100')
    distortDiceResult = failDice.roll()
    if distortDiceResult < 51: #Distort Speech is a 50% Chance to fail spells and activate items
        evt_obj.return_val = 100
        attachee.float_text_line("Distort Speech Failure", tf_red)
        game.create_history_freeform("~Distort Speech~[TAG_SPELLS_DISTORT_SPEECH] check: {} rolls a {}. Failure!\n\n".format(attachee.description, distortDiceResult))
        game.particles('Fizzle', attachee)
    else:
        attachee.float_text_line("Distort Speech Success")
        game.create_history_freeform("~Distort Speech~[TAG_SPELLS_DISTORT_SPEECH] check: {} rolls a {}. Success!\n\n".format(attachee.description, distortDiceResult))
    return 0

def distortSpeechSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Distort Speech ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Distort Speech ({} rounds)".format(args.get_arg(1)))
    return 0

def distortSpeechSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DISTORT_SPEECH"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DISTORT_SPEECH"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def distortSpeechSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def distortSpeechSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def distortSpeechSpellSpellEnd(attachee, args, evt_obj):
    print "Distort SpeechSpellEnd"
    return 0

distortSpeechSpell = PythonModifier("sp-Distort Speech", 3) # spell_id, duration, ComponentsUseV
distortSpeechSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, distortSpeechSpellCheckIfVerbal,())
distortSpeechSpell.AddHook(ET_OnD20Query, EK_Q_SpellInterrupted, distortSpeechSpellDistortCheck,())
distortSpeechSpell.AddHook(ET_OnGetTooltip, EK_NONE, distortSpeechSpellTooltip, ())
distortSpeechSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, distortSpeechSpellEffectTooltip, ())
distortSpeechSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, distortSpeechSpellSpellEnd, ())
distortSpeechSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, distortSpeechSpellHasSpellActive, ())
distortSpeechSpell.AddHook(ET_OnD20Signal, EK_S_Killed, distortSpeechSpellKilled, ())
distortSpeechSpell.AddSpellDispelCheckStandard()
distortSpeechSpell.AddSpellTeleportPrepareStandard()
distortSpeechSpell.AddSpellTeleportReconnectStandard()
distortSpeechSpell.AddSpellCountdownStandardHook()
