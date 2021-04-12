from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Ironguts"

def irongutsSpellBonusToPoisonSaves(attachee, args, evt_obj):
    if evt_obj.flags & 0x8: #according to d20_defs.h D20STD_F_POISON = 4, // 0x8; so I do use 8 and not D20STD_F_POISON as it returns 4 and is not working
        evt_obj.bonus_list.add(5, 151,"~Ironguts~[TAG_SPELLS_IRONGUTS] ~Alchemical~[TAG_MODIFIER_ALCHEMICAL] Bonus") #151 = Alchemical; Ironguts adds a +5 Alchemical Bonus to Fortitude Saves vs. poison
    return 0

def irongutsSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Ironguts ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Ironguts ({} rounds)".format(args.get_arg(1)))
    return 0

def irongutsSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("IRONGUTS"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("IRONGUTS"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def irongutsSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def irongutsSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def irongutsSpellSpellEnd(attachee, args, evt_obj):
    print "Ironguts SpellEnd"
    attachee.condition_add('Nauseated Condition', 1) #When spell expires target is nauseated for 1 round
    return 0

irongutsSpell = PythonModifier("sp-Ironguts", 2) # spell_id, duration
irongutsSpell.AddHook(ET_OnSaveThrowLevel, EK_SAVE_FORTITUDE, irongutsSpellBonusToPoisonSaves,())
irongutsSpell.AddHook(ET_OnGetTooltip, EK_NONE, irongutsSpellTooltip, ())
irongutsSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, irongutsSpellEffectTooltip, ())
irongutsSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, irongutsSpellSpellEnd, ())
irongutsSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, irongutsSpellHasSpellActive, ())
irongutsSpell.AddHook(ET_OnD20Signal, EK_S_Killed, irongutsSpellKilled, ())
irongutsSpell.AddSpellDispelCheckStandard()
irongutsSpell.AddSpellTeleportPrepareStandard()
irongutsSpell.AddSpellTeleportReconnectStandard()
irongutsSpell.AddSpellCountdownStandardHook()
