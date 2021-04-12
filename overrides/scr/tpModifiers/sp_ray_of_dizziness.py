from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Ray of Dizziness"

def rayOfDizzinessSpellTurnBasedStatusInit(attachee, args, evt_obj):
    if evt_obj.tb_status.hourglass_state > 2:
        attachee.float_text_line("Dizzy", tf_red)
        evt_obj.tb_status.hourglass_state = 2 # Limited to a Standard or Move Action only
    return 0

def rayOfDizzinessSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Ray of Dizziness ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Ray of Dizziness ({} rounds)".format(args.get_arg(1)))
    return 0

def rayOfDizzinessSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("RAY_OF_DIZZINESS"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("RAY_OF_DIZZINESS"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def rayOfDizzinessSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0
    
def rayOfDizzinessSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def rayOfDizzinessSpellSpellEnd(attachee, args, evt_obj):
    print "Ray of DizzinessSpellEnd"
    return 0

rayOfDizzinessSpell = PythonModifier("sp-Ray of Dizziness", 2) # spell_id, duration
rayOfDizzinessSpell.AddHook(ET_OnTurnBasedStatusInit, EK_NONE, rayOfDizzinessSpellTurnBasedStatusInit, ())
rayOfDizzinessSpell.AddHook(ET_OnGetTooltip, EK_NONE, rayOfDizzinessSpellTooltip, ())
rayOfDizzinessSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, rayOfDizzinessSpellEffectTooltip, ())
rayOfDizzinessSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, rayOfDizzinessSpellSpellEnd, ())
rayOfDizzinessSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, rayOfDizzinessSpellHasSpellActive, ())
rayOfDizzinessSpell.AddHook(ET_OnD20Signal, EK_S_Killed, rayOfDizzinessSpellKilled, ())
rayOfDizzinessSpell.AddSpellDispelCheckStandard()
rayOfDizzinessSpell.AddSpellTeleportPrepareStandard()
rayOfDizzinessSpell.AddSpellTeleportReconnectStandard()
rayOfDizzinessSpell.AddSpellCountdownStandardHook()
