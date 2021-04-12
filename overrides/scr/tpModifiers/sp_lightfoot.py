from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Lightfoot"

def lightfootSpellCancelAoO(attachee, args, evt_obj):
    attachee.float_text_line("Lightfooted")
    evt_obj.return_val = 0
    return 0

def lightfootSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Lightfoot ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Lightfoot ({} rounds)".format(args.get_arg(1)))
    return 0

def lightfootSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("LIGHTFOOT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("LIGHTFOOT"), -2, " (({} rounds)".format(args.get_arg(1)))
    return 0

def lightfootSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def lightfootSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def lightfootSpellSpellEnd(attachee, args, evt_obj):
    print "Lightfoot SpellEnd"
    return 0

lightfootSpell = PythonModifier("sp-Lightfoot", 2) # spell_id, duration
lightfootSpell.AddHook(ET_OnD20Query, EK_Q_AOOIncurs, lightfootSpellCancelAoO,())
lightfootSpell.AddHook(ET_OnGetTooltip, EK_NONE, lightfootSpellTooltip, ())
lightfootSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, lightfootSpellEffectTooltip, ())
lightfootSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, lightfootSpellSpellEnd, ())
lightfootSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, lightfootSpellHasSpellActive, ())
lightfootSpell.AddHook(ET_OnD20Signal, EK_S_Killed, lightfootSpellKilled, ())
lightfootSpell.AddSpellDispelCheckStandard()
lightfootSpell.AddSpellTeleportPrepareStandard()
lightfootSpell.AddSpellTeleportReconnectStandard()
lightfootSpell.AddSpellCountdownStandardHook()
