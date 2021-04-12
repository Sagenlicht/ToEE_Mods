from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Divine Protection"

def divineProtectionSpellBonus(attachee, args, evt_obj):
    #Divine Protection grants a +1 morale bonus to AC and saving throws
    evt_obj.bonus_list.add(1, 13, "~Divine Protection~[TAG_SPELLS_DIVINE_PROTECTION] ~Morale~[TAG_MODIFIER_MORALE] Bonus")
    return 0

def divineProtectionSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Divine Protection ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Divine Protection ({} rounds)".format(args.get_arg(1)))
    return 0

def divineProtectionSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DIVINE_PROTECTION"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DIVINE_PROTECTION"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def divineProtectionSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def divineProtectionSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def divineProtectionSpellSpellEnd(attachee, args, evt_obj):
    print "Divine Protection SpellEnd"
    return 0

divineProtectionSpell = PythonModifier("sp-Divine Protection", 2) # spell_id, duration
divineProtectionSpell.AddHook(ET_OnGetAC, EK_NONE, divineProtectionSpellBonus,())
divineProtectionSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, divineProtectionSpellBonus,())
divineProtectionSpell.AddHook(ET_OnGetTooltip, EK_NONE, divineProtectionSpellTooltip, ())
divineProtectionSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, divineProtectionSpellEffectTooltip, ())
divineProtectionSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, divineProtectionSpellSpellEnd, ())
divineProtectionSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, divineProtectionSpellHasSpellActive, ())
divineProtectionSpell.AddHook(ET_OnD20Signal, EK_S_Killed, divineProtectionSpellKilled, ())
divineProtectionSpell.AddSpellDispelCheckStandard()
divineProtectionSpell.AddSpellTeleportPrepareStandard()
divineProtectionSpell.AddSpellTeleportReconnectStandard()
divineProtectionSpell.AddSpellCountdownStandardHook()
