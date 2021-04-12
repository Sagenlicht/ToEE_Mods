from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Undersong"

def undersongSpellReplaceConWithPerform(attachee, args, evt_obj):
    bonusToConcentration = attachee.skill_level_get(skill_perform) - attachee.skill_level_get(skill_concentration)
    if bonusToConcentration > 0: #Undersong is a may condition
        evt_obj.bonus_list.add(bonusToConcentration,0,"~Undersong~[TAG_SPELLS_UNDERSONG] Bonus") #Undersong replaces Concentration Checks with Perform Checks, to simplify it, add the diff as a generic stacking bonus
    return 0

def undersongSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Undersong (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Undersong (" + str(args.get_arg(1)) + " rounds)")
    return 0

def undersongSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("UNDERSONG"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("UNDERSONG"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def undersongSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def undersongSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def undersongSpellSpellEnd(attachee, args, evt_obj):
    print "Undersong SpellEnd"
    return 0

undersongSpell = PythonModifier("sp-Undersong", 2) # spell_id, duration
undersongSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_CONCENTRATION, undersongSpellReplaceConWithPerform,())
undersongSpell.AddHook(ET_OnGetTooltip, EK_NONE, undersongSpellTooltip, ())
undersongSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, undersongSpellEffectTooltip, ())
undersongSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, undersongSpellSpellEnd, ())
undersongSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, undersongSpellHasSpellActive, ())
undersongSpell.AddHook(ET_OnD20Signal, EK_S_Killed, undersongSpellKilled, ())
undersongSpell.AddSpellDispelCheckStandard()
undersongSpell.AddSpellTeleportPrepareStandard()
undersongSpell.AddSpellTeleportReconnectStandard()
undersongSpell.AddSpellCountdownStandardHook()
