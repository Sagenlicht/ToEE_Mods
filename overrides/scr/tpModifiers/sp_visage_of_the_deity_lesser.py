from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Visage of the Deity lesser"

def visageOfTheDeityLesserSpellAbilityBonus(attachee, args, evt_obj):
    evt_obj.bonus_list.add(4, 12, "~Visage of the Deity, lesser~[TAG_SPELLS_VISAGE_OF_THE_DEITY_LESSER] ~Enhancement~[TAG_ENHANCEMENT] Bonus") #Visage of the Deity, lesser adds a +4 Enhancement Bonus to Charisma
    return 0

def visageOfTheDeityLesserSpellElementalResistance(attachee, args, evt_obj):
    casterAlignment = attachee.critter_get_alignment()
    if casterAlignment & ALIGNMENT_GOOD:
        evt_obj.damage_packet.add_damage_resistance(10, D20DT_ACID, 124) #ID 124 in damage.mes is Resistance to Energy
        evt_obj.damage_packet.add_damage_resistance(10, D20DT_COLD, 124) #ID 124 in damage.mes is Resistance to Energy
        evt_obj.damage_packet.add_damage_resistance(10, D20DT_ELECTRICITY, 124) #ID 124 in damage.mes is Resistance to Energy
    if casterAlignment & ALIGNMENT_EVIL:
        evt_obj.damage_packet.add_damage_resistance(10, D20DT_COLD, 124) #ID 124 in damage.mes is Resistance to Energy
        evt_obj.damage_packet.add_damage_resistance(10, D20DT_FIRE, 124) #ID 124 in damage.mes is Resistance to Energy
    return 0

def visageOfTheDeityLesserSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Visage of the Deity lesser ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Visage of the Deity lesser ({} rounds)".format(args.get_arg(1)))
    return 0

def visageOfTheDeityLesserSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("VISAGE_OF_THE_DEITY_LESSER"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("VISAGE_OF_THE_DEITY_LESSER"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def visageOfTheDeityLesserSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def visageOfTheDeityLesserSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def visageOfTheDeityLesserSpellSpellEnd(attachee, args, evt_obj):
    print "Visage of the Deity lesser SpellEnd"
    return 0

visageOfTheDeityLesserSpell = PythonModifier("sp-Visage of the Deity lesser", 2) # spell_id, duration
visageOfTheDeityLesserSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_CHARISMA, visageOfTheDeityLesserSpellAbilityBonus, ())
visageOfTheDeityLesserSpell.AddHook(ET_OnTakingDamage , EK_NONE, visageOfTheDeityLesserSpellElementalResistance,())
visageOfTheDeityLesserSpell.AddHook(ET_OnGetTooltip, EK_NONE, visageOfTheDeityLesserSpellTooltip, ())
visageOfTheDeityLesserSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, visageOfTheDeityLesserSpellEffectTooltip, ())
visageOfTheDeityLesserSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, visageOfTheDeityLesserSpellSpellEnd, ())
visageOfTheDeityLesserSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, visageOfTheDeityLesserSpellHasSpellActive, ())
visageOfTheDeityLesserSpell.AddHook(ET_OnD20Signal, EK_S_Killed, visageOfTheDeityLesserSpellKilled, ())
visageOfTheDeityLesserSpell.AddSpellDispelCheckStandard()
visageOfTheDeityLesserSpell.AddSpellTeleportPrepareStandard()
visageOfTheDeityLesserSpell.AddSpellTeleportReconnectStandard()
visageOfTheDeityLesserSpell.AddSpellCountdownStandardHook()
