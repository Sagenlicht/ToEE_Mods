from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Sirines Grace"

### Swim Speed and breath underwater is not applicable in ToEE nor the underwater combat changes ###

def sirinesGraceSpellAbilityBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(4, 12, "~Sirines Grace~[TAG_SPELLS_SIRINES_GRACE] ~Enhancement~[TAG_ENHANCEMENT] Bonus") #Sirines Grace adds a +4 Enhancement Bonus to Charisma and Dexterity
    return 0

def sirinesGraceSpellPerformBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(8, 0, "~Sirines Grace~[TAG_SPELLS_SIRINES_GRACE] Bonus") #Sirines Grace adds a +8 untyped Bonus to Perform
    return 0

def sirinesGraceSpellAcBonus(attachee, args, evt_obj):
    spellTargetCharisma = attachee.stat_level_get(stat_charisma)
    charismaModifier = (spellTargetCharisma-10)/2
    evt_obj.bonus_list.add(charismaModifier, 11, "~Sirines Grace~[TAG_SPELLS_SIRINES_GRACE] ~Deflection~[TAG_DEFLECTION_BONUS] Bonus") #Sirines Grace adds a +4 Enhancement Bonus to Charisma and Dexterity
    return 0

def sirinesGraceSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Sirines Grace ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Sirines Grace ({} rounds)".format(args.get_arg(1)))
    return 0

def sirinesGraceSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("SIRINES_GRACE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("SIRINES_GRACE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def sirinesGraceSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def sirinesGraceSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def sirinesGraceSpellSpellEnd(attachee, args, evt_obj):
    print "Sirines Grace SpellEnd"
    return 0

sirinesGraceSpell = PythonModifier("sp-Sirines Grace", 2) # spell_id, duration
sirinesGraceSpell.AddHook(ET_OnGetAC, EK_NONE, sirinesGraceSpellAcBonus,())
sirinesGraceSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_PERFORM, sirinesGraceSpellPerformBonus,())
sirinesGraceSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_CHARISMA, sirinesGraceSpellAbilityBonus,())
sirinesGraceSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, sirinesGraceSpellAbilityBonus,())
sirinesGraceSpell.AddHook(ET_OnGetTooltip, EK_NONE, sirinesGraceSpellTooltip, ())
sirinesGraceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, sirinesGraceSpellEffectTooltip, ())
sirinesGraceSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, sirinesGraceSpellSpellEnd, ())
sirinesGraceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, sirinesGraceSpellHasSpellActive, ())
sirinesGraceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, sirinesGraceSpellKilled, ())
sirinesGraceSpell.AddSpellDispelCheckStandard()
sirinesGraceSpell.AddSpellTeleportPrepareStandard()
sirinesGraceSpell.AddSpellTeleportReconnectStandard()
sirinesGraceSpell.AddSpellCountdownStandardHook()
