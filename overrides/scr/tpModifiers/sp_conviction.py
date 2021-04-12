from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Conviction"

def convictionSpellBonusToSaves(attachee, args, evt_obj):
    evt_obj.bonus_list.add(args.get_arg(2), 13, "~Conviction~[TAG_SPELLS_CONVICTION] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #Bonus is passed by spell
    return 0

def convictionSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Conviction ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Conviction ({} rounds)".format(args.get_arg(1)))
    return 0

def convictionSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CONVICTION"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CONVICTION"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def convictionSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def convictionSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def convictionSpellSpellEnd(attachee, args, evt_obj):
    print "Conviction SpellEnd"
    return 0

convictionSpell = PythonModifier("sp-Conviction", 3) # spell_id, duration, spellBonus
convictionSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, convictionSpellBonusToSaves, ())
convictionSpell.AddHook(ET_OnGetTooltip, EK_NONE, convictionSpellTooltip, ())
convictionSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, convictionSpellEffectTooltip, ())
convictionSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, convictionSpellSpellEnd, ())
convictionSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, convictionSpellHasSpellActive, ())
convictionSpell.AddHook(ET_OnD20Signal, EK_S_Killed, convictionSpellKilled, ())
convictionSpell.AddSpellDispelCheckStandard()
convictionSpell.AddSpellTeleportPrepareStandard()
convictionSpell.AddSpellTeleportReconnectStandard()
convictionSpell.AddSpellCountdownStandardHook()
