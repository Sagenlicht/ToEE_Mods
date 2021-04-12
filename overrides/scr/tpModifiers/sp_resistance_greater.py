from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Resistance Greater"

def resistanceGreaterSpellBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(3, 15, "~Resistance, Greater~[TAG_SPELLS_RESISTANCE_GREATER] ~Resistance~[TAG_MODIFIER_RESISTANCE] Bonus") #Resistance, Greater is a flat +3 resistance bouns to saves
    return 0

def resistanceGreaterSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Resistance Greater ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Resistance Greater ({} rounds)".format(args.get_arg(1)))
    return 0

def resistanceGreaterSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("RESISTANCE_GREATER"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("RESISTANCE_GREATER"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def resistanceGreaterSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def resistanceGreaterSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def resistanceGreaterSpellSpellEnd(attachee, args, evt_obj):
    print "Resistance Greater SpellEnd"
    return 0

resistanceGreaterSpell = PythonModifier("sp-Resistance Greater", 2) # spell_id, duration
resistanceGreaterSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, resistanceGreaterSpellBonus,())
resistanceGreaterSpell.AddHook(ET_OnGetTooltip, EK_NONE, resistanceGreaterSpellTooltip, ())
resistanceGreaterSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, resistanceGreaterSpellEffectTooltip, ())
resistanceGreaterSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, resistanceGreaterSpellSpellEnd, ())
resistanceGreaterSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, resistanceGreaterSpellHasSpellActive, ())
resistanceGreaterSpell.AddHook(ET_OnD20Signal, EK_S_Killed, resistanceGreaterSpellKilled, ())
resistanceGreaterSpell.AddSpellDispelCheckStandard()
resistanceGreaterSpell.AddSpellTeleportPrepareStandard()
resistanceGreaterSpell.AddSpellTeleportReconnectStandard()
resistanceGreaterSpell.AddSpellCountdownStandardHook()
