from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Clear Mind"

def clearMindSpellBonusToMindAffecting(attachee, args, evt_obj):
    if evt_obj.flags & 0x8000000: #according to d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_MIND_AFFECTING = 28,  // 0x8000000;
        attachee.float_text_line("Clear Mind")
        evt_obj.bonus_list.add(4, 153,"~Clear Mind~[TAG_SPELLS_CLEAR_MIND] ~Sacred~[TAG_MODIFIER_SACRED] Bonus") #151 = Alchemical; Clear Mind adds a +5 Alchemical Bonus to Fortitude Saves vs. poison
    return 0

def clearMindSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Clear Mind ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Clear Mind ({} rounds)".format(args.get_arg(1)))
    return 0

def clearMindSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CLEAR_MIND"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CLEAR_MIND"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def clearMindSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def clearMindSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def clearMindSpellSpellEnd(attachee, args, evt_obj):
    print "Clear Mind SpellEnd"
    return 0

clearMindSpell = PythonModifier("sp-Clear Mind", 2) # spell_id, duration
clearMindSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, clearMindSpellBonusToMindAffecting,())
clearMindSpell.AddHook(ET_OnGetTooltip, EK_NONE, clearMindSpellTooltip, ())
clearMindSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, clearMindSpellEffectTooltip, ())
clearMindSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, clearMindSpellSpellEnd, ())
clearMindSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, clearMindSpellHasSpellActive, ())
clearMindSpell.AddHook(ET_OnD20Signal, EK_S_Killed, clearMindSpellKilled, ())
clearMindSpell.AddSpellDispelCheckStandard()
clearMindSpell.AddSpellTeleportPrepareStandard()
clearMindSpell.AddSpellTeleportReconnectStandard()
clearMindSpell.AddSpellCountdownStandardHook()
