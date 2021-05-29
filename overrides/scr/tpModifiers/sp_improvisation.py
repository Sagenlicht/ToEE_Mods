from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Improvisation"

#Args:
# 0 spell_id
# 1 duration
# 2 bonusToAdd
# 3 bonusPool
# 4 activateAbility
# 5 activateSkill
# 6 activateAttack

def improvisationSpellConditionAdd(attachee, args, evt_obj):
    attachee.float_text_line("Luck Pool: {}".format(args.get_arg(3)))
    return 0

def improvisationSpellRadial(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    improvisationBonusCap = min(args.get_arg(3), spellPacket.caster_level/2) #Bonus cannot be higher than points left in BonusPool

    #Add the top level menu
    radialParent = tpdp.RadialMenuEntryParent("Improvisation ({})".format(args.get_arg(3)))
    improvisationRadialId = radialParent.add_child_to_standard(attachee, tpdp.RadialMenuStandardNode.Class)

    #Add a slider to set the bonus
    sliderSetBonusAmount = tpdp.RadialMenuEntrySlider("Set Bonus Amount", "Set Bonus Amount for Improvisation", 0, improvisationBonusCap, "TAG_INTERFACE_HELP")
    sliderSetBonusAmount.link_to_args(args, 2)
    sliderSetBonusAmount.add_as_child(attachee, improvisationRadialId)

    #Add checkboxes to activate or deactivate the bonus for different options
    checkboxAbilityBonus = tpdp.RadialMenuEntryToggle("+{} to next Ability Check".format(args.get_arg(2)), "TAG_SPELLS_IMPROVISATION")
    checkboxAbilityBonus.link_to_args(args, 4)
    checkboxAbilityBonus.add_as_child(attachee, improvisationRadialId)

    checkboxSkillBonus = tpdp.RadialMenuEntryToggle("+{} to next Skill Check".format(args.get_arg(2)), "TAG_SPELLS_IMPROVISATION")
    checkboxSkillBonus.link_to_args(args, 5)
    checkboxSkillBonus.add_as_child(attachee, improvisationRadialId)

    checkboxAttackBonus = tpdp.RadialMenuEntryToggle("+{} to next Attack".format(args.get_arg(2)), "TAG_SPELLS_IMPROVISATION")
    checkboxAttackBonus.link_to_args(args, 6)
    checkboxAttackBonus.add_as_child(attachee, improvisationRadialId)
    return 0

def improvisationSpellAbilityCheckBonus(attachee, args, evt_obj):
    if args.get_arg(4): #check if enabled
        evt_obj.bonus_list.add(args.get_arg(2), 14, "~Improvisation~[TAG_SPELLS_IMPROVISATION] ~Luck~[TAG_MODIFIER_LUCK] Bonus") # Luck Bonus = 14
        args.set_arg(3, args.get_arg(3)-args.get_arg(2))
        if args.get_arg(3) > 0:
            attachee.float_text_line("Luck Pool Left: {}".format(args.get_arg(3)))
            if args.get_arg(3) < args.get_arg(2):
                args.set_arg(2, args.get_arg(3))
        else: 
            attachee.float_text_line("Luck Pool depleted")
            attachee.d20_send_signal(S_Spell_End, args.get_arg(0))
            #args.remove_spell()
            #args.remove_spell_mod()
    return 0

def improvisationSpellSkillCheckBonus(attachee, args, evt_obj):
    if args.get_arg(5): #check if enabled
        evt_obj.bonus_list.add(args.get_arg(2), 14, "~Improvisation~[TAG_SPELLS_IMPROVISATION] ~Luck~[TAG_MODIFIER_LUCK] Bonus") # 14 = Luck Bonus
        args.set_arg(3, args.get_arg(3)-args.get_arg(2))
        if args.get_arg(3) > 0:
            attachee.float_text_line("Luck Pool Left: {}".format(args.get_arg(3)))
            if args.get_arg(3) < args.get_arg(2):
                args.set_arg(2, args.get_arg(3))
        else: 
            attachee.float_text_line("Luck Pool depleted")
            attachee.d20_send_signal(S_Spell_End, args.get_arg(0))
            #args.remove_spell()
            #args.remove_spell_mod()
    return 0

def improvisationSpellAttackBonus(attachee, args, evt_obj):
    if not (evt_obj.attack_packet.get_flags() & D20CAF_FINAL_ATTACK_ROLL): #Test to make sure it is not called from the character sheet
        return 0
    if args.get_arg(6): #check if enabled
        evt_obj.bonus_list.add(args.get_arg(2), 14, "~Improvisation~[TAG_SPELLS_IMPROVISATION] ~Luck~[TAG_MODIFIER_LUCK] Bonus") # 14 = Luck Bonus
        args.set_arg(3, args.get_arg(3)-args.get_arg(2))
    return 0

def improvisationSpellfloatAfterAttack(attachee, args, evt_obj): #added because float overlapped while being directly attached to AttackBonus when attack missed
    if args.get_arg(6): #check if enabled
        if args.get_arg(3) > 0:
            attachee.float_text_line("Luck Pool Left: {}".format(args.get_arg(3)))
            if args.get_arg(3) < args.get_arg(2):
                args.set_arg(2, args.get_arg(3))
        else: 
            attachee.float_text_line("Luck Pool depleted")
            attachee.d20_send_signal(S_Spell_End, args.get_arg(0))
            #args.remove_spell()
            #args.remove_spell_mod()
    return 0


def improvisationSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Improvisation (Pool: {}) ({} round)".format(args.get_arg(3), args.get_arg(1)))
    else:
        evt_obj.append("Improvisation (Pool: {}) ({} rounds)".format(args.get_arg(3), args.get_arg(1)))
    return 0

def improvisationSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("IMPROVISATION"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("IMPROVISATION"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def improvisationSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def improvisationSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def improvisationSpellSpellEnd(attachee, args, evt_obj):
    print "Improvisation SpellEnd"
    return 0

improvisationSpell = PythonModifier("sp-Improvisation", 7) # spell_id, duration, bonusToAdd, bonusPool, activateAbility, activateSkill, activateAttack
improvisationSpell.AddHook(ET_OnConditionAdd, EK_NONE, improvisationSpellConditionAdd, ())
improvisationSpell.AddHook(ET_OnBuildRadialMenuEntry, EK_NONE, improvisationSpellRadial, ())
improvisationSpell.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, improvisationSpellAbilityCheckBonus,())
improvisationSpell.AddHook(ET_OnGetSkillLevel, EK_NONE, improvisationSpellSkillCheckBonus, ())
improvisationSpell.AddHook(ET_OnToHitBonus2, EK_NONE, improvisationSpellAttackBonus, ())
improvisationSpell.AddHook(ET_OnD20Signal, EK_S_Attack_Made, improvisationSpellfloatAfterAttack, ())
improvisationSpell.AddHook(ET_OnGetTooltip, EK_NONE, improvisationSpellTooltip, ())
improvisationSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, improvisationSpellEffectTooltip, ())
improvisationSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, improvisationSpellSpellEnd, ())
improvisationSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, improvisationSpellHasSpellActive, ())
improvisationSpell.AddHook(ET_OnD20Signal, EK_S_Killed, improvisationSpellKilled, ())
improvisationSpell.AddSpellDispelCheckStandard()
improvisationSpell.AddSpellTeleportPrepareStandard()
improvisationSpell.AddSpellTeleportReconnectStandard()
improvisationSpell.AddSpellCountdownStandardHook()
