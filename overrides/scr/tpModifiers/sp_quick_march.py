from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Quick March"

def quickMarchSpellCorrectDurationForCaster(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if attachee == spellPacket.caster:
        args.set_arg(1, (args.get_arg(1)-1)) #reduce duration by 1 for caster so it is actually only active in current round
    return 0

def quickMarchSpellMovementBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(30, 12 ,"~Quick March~[TAG_SPELLS_QUICK_MARCH] ~Enhancement~[TAG_ENHANCEMENT] Bonus") #Quick March adds 30ft. to movement speed
    return 0


def quickMarchSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Quick March ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Quick March ({} rounds)".format(args.get_arg(1)))
    return 0

def quickMarchSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("QUICK_MARCH"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("QUICK_MARCH"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def quickMarchSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def quickMarchSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def quickMarchSpellSpellEnd(attachee, args, evt_obj):
    print "Quick March SpellEnd"
    return 0

quickMarchSpell = PythonModifier("sp-Quick March", 2) # spell_id, duration
quickMarchSpell.AddHook(ET_OnConditionAdd, EK_NONE, quickMarchSpellCorrectDurationForCaster,())
quickMarchSpell.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, quickMarchSpellMovementBonus,())
quickMarchSpell.AddHook(ET_OnGetTooltip, EK_NONE, quickMarchSpellTooltip, ())
quickMarchSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, quickMarchSpellEffectTooltip, ())
quickMarchSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, quickMarchSpellSpellEnd, ())
quickMarchSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, quickMarchSpellHasSpellActive, ())
quickMarchSpell.AddHook(ET_OnD20Signal, EK_S_Killed, quickMarchSpellKilled, ())
quickMarchSpell.AddSpellDispelCheckStandard()
quickMarchSpell.AddSpellTeleportPrepareStandard()
quickMarchSpell.AddSpellTeleportReconnectStandard()
quickMarchSpell.AddSpellCountdownStandardHook()
