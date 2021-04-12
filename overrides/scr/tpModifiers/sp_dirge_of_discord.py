from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Dirge of Discord"

def dirgeOfDiscordSpellPenalty(attachee, args, evt_obj):
    evt_obj.bonus_list.add(-4, 0, "~Dirge of Discord~[TAG_SPELLS_DIRGE_OF_DISCORD] Penalty") #Dirge of Discord is a -4 penalty on Attack Rolls and Dexterity
    return 0

def dirgeOfDiscordSpellMovementPenalty(attachee, args, evt_obj):
    moveSpeedBase = attachee.stat_level_get(stat_movement_speed)
    evt_obj.bonus_list.add(-(moveSpeedBase/2), 0 ,"~Dirge of Discord~[TAG_SPELLS_DIRGE_OF_DISCORD] Penalty") #Dirge of Discord recudes speed by 50% to a minimum of 5
    newSpeed = evt_obj.bonus_list.get_sum()
    if newSpeed < 5:
        speedToAdd = 5 - newSpeed
        evt_obj.bonus_list.add(speedToAdd, 0, "~Dirge of Discord~[TAG_SPELLS_DIRGE_OF_DISCORD] reduces to a minimum of 5 speed")
    return 0

def dirgeOfDiscordSpellGetSpellLevel(attachee, args, evt_obj):
    spellPacket = evt_obj.get_spell_packet()
    spellLevel = spellPacket.spell_known_slot_level #not tested with metamagic hightend spells
    args.set_arg(3, spellLevel)
    return 0

def dirgeOfDiscordSpellConcentrationCheck(attachee, args, evt_obj):
    attachee.float_text_line("Concentration Check", tf_red)
    skillCheckDc = args.get_arg(2) + args.get_arg(3) # spellDC + spellLevel
    concentrationSkillValue = attachee.skill_level_get(skill_concentration)
    if concentrationSkillValue == OBJ_HANDLE_NULL:
        concentrationSkillValue = 0
    skillDice = dice_new('1d20')
    skillDiceRoll = skillDice.roll()
    skillRollResult = skillDiceRoll + concentrationSkillValue
    game.create_history_freeform(attachee.description + " attempts a ~Dirge of Discord~[TAG_SPELLS_DIRGE_OF_DISCORD] concenatration check (dc{}): \n\n".format(skillCheckDc))
    if skillRollResult < skillCheckDc:
        attachee.float_text_line("failed", tf_red)
        game.create_history_freeform("Rolled a ({}) - Failure! \n\n".format(skillRollResult))
        game.particles('Fizzle', attachee)
        evt_obj.return_val = 100
    else:
        attachee.float_text_line("success")
        game.create_history_freeform("Rolled a ({}) - Success! \n\n".format(skillRollResult))
    return 0

def dirgeOfDiscordSpellAddConcentration(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.caster.condition_add_with_args('sp-Concentrating', args.get_arg(0))
    return 0

def dirgeOfDiscordSpellConcentrationBroken(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.spell_enum == 0:
        return 0
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def dirgeOfDiscordSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Dirge of Discord ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Dirge of Discord ({} rounds)".format(args.get_arg(1)))
    return 0

def dirgeOfDiscordSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DIRGE_OF_DISCORD"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DIRGE_OF_DISCORD"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def dirgeOfDiscordSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def dirgeOfDiscordSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def dirgeOfDiscordSpellSpellEnd(attachee, args, evt_obj):
    print "Dirge of Discord SpellEnd"
    return 0

dirgeOfDiscordSpell = PythonModifier("sp-Dirge of Discord", 4) # spell_id, duration, spellDc, spellLevel
dirgeOfDiscordSpell.AddHook(ET_OnToHitBonus2, EK_NONE, dirgeOfDiscordSpellPenalty,())
dirgeOfDiscordSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, dirgeOfDiscordSpellPenalty,())
dirgeOfDiscordSpell.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, dirgeOfDiscordSpellMovementPenalty,())
dirgeOfDiscordSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, dirgeOfDiscordSpellGetSpellLevel, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Query, EK_Q_SpellInterrupted, dirgeOfDiscordSpellConcentrationCheck,())
dirgeOfDiscordSpell.AddHook(ET_OnConditionAdd, EK_NONE, dirgeOfDiscordSpellAddConcentration,())
dirgeOfDiscordSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, dirgeOfDiscordSpellConcentrationBroken, ())
dirgeOfDiscordSpell.AddHook(ET_OnGetTooltip, EK_NONE, dirgeOfDiscordSpellTooltip, ())
dirgeOfDiscordSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, dirgeOfDiscordSpellEffectTooltip, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, dirgeOfDiscordSpellSpellEnd, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, dirgeOfDiscordSpellHasSpellActive, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Signal, EK_S_Killed, dirgeOfDiscordSpellKilled, ())
dirgeOfDiscordSpell.AddSpellDispelCheckStandard()
dirgeOfDiscordSpell.AddSpellTeleportPrepareStandard()
dirgeOfDiscordSpell.AddSpellTeleportReconnectStandard()
dirgeOfDiscordSpell.AddSpellCountdownStandardHook()
