from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Tremor"

def tremorSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Tremor ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Tremor ({} rounds)".format(args.get_arg(1)))
    return 0

def tremorSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("TREMOR"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("TREMOR"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def tremorSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def tremorSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def tremorSpellSpellEnd(attachee, args, evt_obj):
    print "Tremor SpellEnd"
    return 0

tremorSpell = PythonModifier("sp-Tremor", 2) # spell_id, duration
tremorSpell.AddHook(ET_OnGetTooltip, EK_NONE, tremorSpellTooltip, ())
tremorSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, tremorSpellEffectTooltip, ())
tremorSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, tremorSpellSpellEnd, ())
tremorSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, tremorSpellHasSpellActive, ())
tremorSpell.AddHook(ET_OnD20Signal, EK_S_Killed, tremorSpellKilled, ())
tremorSpell.AddSpellDispelCheckStandard()
tremorSpell.AddSpellTeleportPrepareStandard()
tremorSpell.AddSpellTeleportReconnectStandard()
tremorSpell.AddSpellCountdownStandardHook()
