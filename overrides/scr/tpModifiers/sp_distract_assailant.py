from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Distract Assailant"

def distractAssailantSpellSetFlankedCondition(attachee, args, evt_obj):
    attachee.condition_add('flatfooted')
    return 0

def distractAssailantSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Distract Assailant (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Distract Assailant (" + str(args.get_arg(1)) + " rounds)")
    return 0

def distractAssailantSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DISTRACT_ASSAILANT"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("DISTRACT_ASSAILANT"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def distractAssailantSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def distractAssailantSpellKilled(attachee, args, evt_obj):
    if attachee.d20query(Q_Flatfooted) == 1:
        attachee.condition_remove('flatfooted') #unsure if this command actually works
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def distractAssailantSpellSpellEnd(attachee, args, evt_obj):
    print "Distract AssailantSpellEnd"
    return 0

distractAssailantSpell = PythonModifier("sp-Distract Assailant", 2) # spell_id, duration
distractAssailantSpell.AddHook(ET_OnConditionAdd, EK_NONE, distractAssailantSpellSetFlankedCondition,())
distractAssailantSpell.AddHook(ET_OnGetTooltip, EK_NONE, distractAssailantSpellTooltip, ())
distractAssailantSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, distractAssailantSpellEffectTooltip, ())
distractAssailantSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, distractAssailantSpellSpellEnd, ())
distractAssailantSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, distractAssailantSpellHasSpellActive, ())
distractAssailantSpell.AddHook(ET_OnD20Signal, EK_S_Killed, distractAssailantSpellKilled, ())
distractAssailantSpell.AddSpellDispelCheckStandard()
distractAssailantSpell.AddSpellTeleportPrepareStandard()
distractAssailantSpell.AddSpellTeleportReconnectStandard()
distractAssailantSpell.AddSpellCountdownStandardHook()
