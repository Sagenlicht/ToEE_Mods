from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Nixies Grace"

### Swim Speed and breath underwater is not applicable in ToEE ###

### Is low light vision of revelance? ####

def nixiesGraceSpellDexterityBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(6, 12, "~Nixies Grace~[TAG_SPELLS_NIXIES_GRACE] ~Enhancement~[TAG_ENHANCEMENT] Bonus") #Nixies Grace adds a +6 Enhancement Bonus to Dexterity
    return 0

def nixiesGraceSpellWisdomBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(2, 12, "~Nixies Grace~[TAG_SPELLS_NIXIES_GRACE] ~Enhancement~[TAG_ENHANCEMENT] Bonus") #Nixies Grace adds a +2 Enhancement Bonus to Wisdom
    return 0

def nixiesGraceSpellCharismaBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(8, 12, "~Nixies Grace~[TAG_SPELLS_NIXIES_GRACE] ~Enhancement~[TAG_ENHANCEMENT] Bonus") #Nixies Grace adds a +8 Enhancement Bonus to Charisma
    return 0

def nixiesGraceSpellColdIronDr(attachee, args, evt_obj): #Nixies Grace grants DR 5/cold iron
    evt_obj.damage_packet.add_physical_damage_res(5, D20DAP_COLD, 126) #ID126 in damage.mes is DR
    return 0

def nixiesGraceSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Nixies Grace ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Nixies Grace ({} rounds)".format(args.get_arg(1)))
    return 0

def nixiesGraceSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("NIXIES_GRACE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("NIXIES_GRACE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def nixiesGraceSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def nixiesGraceSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def nixiesGraceSpellSpellEnd(attachee, args, evt_obj):
    print "Nixies Grace SpellEnd"
    return 0

nixiesGraceSpell = PythonModifier("sp-Nixies Grace", 2) # spell_id, duration
nixiesGraceSpell.AddHook(ET_OnTakingDamage , EK_NONE, nixiesGraceSpellColdIronDr,())
nixiesGraceSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_CHARISMA, nixiesGraceSpellCharismaBonus,())
nixiesGraceSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, nixiesGraceSpellDexterityBonus,())
nixiesGraceSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_WISDOM, nixiesGraceSpellWisdomBonus,())
nixiesGraceSpell.AddHook(ET_OnGetTooltip, EK_NONE, nixiesGraceSpellTooltip, ())
nixiesGraceSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, nixiesGraceSpellEffectTooltip, ())
nixiesGraceSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, nixiesGraceSpellSpellEnd, ())
nixiesGraceSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, nixiesGraceSpellHasSpellActive, ())
nixiesGraceSpell.AddHook(ET_OnD20Signal, EK_S_Killed, nixiesGraceSpellKilled, ())
nixiesGraceSpell.AddSpellDispelCheckStandard()
nixiesGraceSpell.AddSpellTeleportPrepareStandard()
nixiesGraceSpell.AddSpellTeleportReconnectStandard()
nixiesGraceSpell.AddSpellCountdownStandardHook()
