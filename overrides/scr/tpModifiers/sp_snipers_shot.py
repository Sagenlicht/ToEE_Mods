from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Snipers Shot"

def snipersShotSpellEnableSneakAttack(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def snipersShotSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Snipers Shot ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Snipers Shot ({} rounds)".format(args.get_arg(1)))
    return 0

def snipersShotSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SNIPERS_SHOT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("SNIPERS_SHOT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def snipersShotSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def snipersShotSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def snipersShotSpellSpellEnd(attachee, args, evt_obj):
    print "Snipers Shot SpellEnd"
    return 0

snipersShotSpell = PythonModifier("sp-Snipers Shot", 3) # spell_id, duration, notFirstAttack
snipersShotSpell.AddHook(ET_OnD20PythonQuery, "Disable Sneak Attack Range Requirement", snipersShotSpellEnableSneakAttack,())
snipersShotSpell.AddHook(ET_OnGetTooltip, EK_NONE, snipersShotSpellTooltip, ())
snipersShotSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, snipersShotSpellEffectTooltip, ())
snipersShotSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, snipersShotSpellSpellEnd, ())
snipersShotSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, snipersShotSpellHasSpellActive, ())
snipersShotSpell.AddHook(ET_OnD20Signal, EK_S_Killed, snipersShotSpellKilled, ())
snipersShotSpell.AddSpellDispelCheckStandard()
snipersShotSpell.AddSpellTeleportPrepareStandard()
snipersShotSpell.AddSpellTeleportReconnectStandard()
snipersShotSpell.AddSpellCountdownStandardHook()
