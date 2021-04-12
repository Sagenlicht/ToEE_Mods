from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Resistance Superior"

def resistanceGreaterSpellBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(6, 15, "~Resistance, Superior~[TAG_SPELLS_RESISTANCE_SUPERIOR] ~Resistance~[TAG_MODIFIER_RESISTANCE] Bonus") #Resistance, Superior is a flat +6 resistance bouns to saves
    return 0

def resistanceGreaterSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Resistance, Superior ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Resistance, Superior ({} rounds)".format(args.get_arg(1)))
    return 0

def resistanceGreaterSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("RESISTANCE_SUPERIOR"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("RESISTANCE_SUPERIOR"), -2, " ({} rounds)".format(args.get_arg(1)))
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
    print "Resistance Superior SpellEnd"
    return 0

resistanceGreaterSpell = PythonModifier("sp-Resistance Superior", 2) # spell_id, duration
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
