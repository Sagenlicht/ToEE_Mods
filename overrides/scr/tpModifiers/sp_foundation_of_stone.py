from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Foundation of Stone"

def foundationOfStoneSpellOnBeginRoud(attachee, args, evt_obj):
    args.set_arg(2, attachee.location)
    print "{} location: {}".format(attachee, attachee.location)
    return 0

def foundationOfStoneSpellBonusToAc(attachee, args, evt_obj):
    if attachee.location == args.get_arg(2):
        evt_obj.bonus_list.add(2, 0, "~Foundation of Stone~[TAG_SPELLS_FOUNDATION_OF_STONE] Bonus")
    print "Hourglas state: {}".format(evt_obj.tb_status.hourglass_state)
    return 0

def foundationOfStoneSpellAbilityCheckBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(4, 0, "~Foundation of Stone~[TAG_SPELLS_FOUNDATION_OF_STONE] Bonus")
    return 0

def foundationOfStoneSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Foundation of Stone ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Foundation of Stone ({} rounds)".format(args.get_arg(1)))
    return 0

def foundationOfStoneSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("FOUNDATION_OF_STONE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("FOUNDATION_OF_STONE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def foundationOfStoneSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def foundationOfStoneSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def foundationOfStoneSpellSpellEnd(attachee, args, evt_obj):
    print "Foundation of Stone SpellEnd"
    return 0

foundationOfStoneSpell = PythonModifier("sp-Foundation of Stone", 3) # spell_id, duration, location
foundationOfStoneSpell.AddHook(ET_OnGetAbilityCheckModifier, EK_STAT_STRENGTH, foundationOfStoneSpellAbilityCheckBonus,())
foundationOfStoneSpell.AddHook(ET_OnBeginRound, EK_NONE, foundationOfStoneSpellOnBeginRoud, ())
foundationOfStoneSpell.AddHook(ET_OnGetACBonus2 , EK_NONE, foundationOfStoneSpellBonusToAc, ())
foundationOfStoneSpell.AddHook(ET_OnGetTooltip, EK_NONE, foundationOfStoneSpellTooltip, ())
foundationOfStoneSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, foundationOfStoneSpellEffectTooltip, ())
foundationOfStoneSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, foundationOfStoneSpellSpellEnd, ())
foundationOfStoneSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, foundationOfStoneSpellHasSpellActive, ())
foundationOfStoneSpell.AddHook(ET_OnD20Signal, EK_S_Killed, foundationOfStoneSpellKilled, ())
foundationOfStoneSpell.AddSpellDispelCheckStandard()
foundationOfStoneSpell.AddSpellTeleportPrepareStandard()
foundationOfStoneSpell.AddSpellTeleportReconnectStandard()
foundationOfStoneSpell.AddSpellCountdownStandardHook()
