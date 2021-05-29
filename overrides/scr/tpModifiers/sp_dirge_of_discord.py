from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
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
    skillCheckDc = args.get_arg(2) + args.get_arg(3) # spellDC + spellLevel
    passedCheck = spell_utils.skillCheck(attachee, skill_concentration, skillCheckDc)
    if passedCheck:
        attachee.float_text_line("success")
    else:
        attachee.float_text_line("failed", tf_red)
        #game.particles('Fizzle', attachee)
        evt_obj.return_val = 100
    return 0

dirgeOfDiscordSpell = PythonModifier("sp-Dirge of Discord", 4) # spell_id, duration, spellDc, spellLevel
dirgeOfDiscordSpell.AddHook(ET_OnToHitBonus2, EK_NONE, dirgeOfDiscordSpellPenalty,())
dirgeOfDiscordSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_DEXTERITY, dirgeOfDiscordSpellPenalty,())
dirgeOfDiscordSpell.AddHook(ET_OnGetMoveSpeedBase, EK_NONE, dirgeOfDiscordSpellMovementPenalty,())
dirgeOfDiscordSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, dirgeOfDiscordSpellGetSpellLevel, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Query, EK_Q_SpellInterrupted, dirgeOfDiscordSpellConcentrationCheck,())
dirgeOfDiscordSpell.AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addConcentration, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, spell_utils.checkRemoveSpell, ())
dirgeOfDiscordSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
dirgeOfDiscordSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
dirgeOfDiscordSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
dirgeOfDiscordSpell.AddSpellDispelCheckStandard()
dirgeOfDiscordSpell.AddSpellTeleportPrepareStandard()
dirgeOfDiscordSpell.AddSpellTeleportReconnectStandard()
dirgeOfDiscordSpell.AddSpellCountdownStandardHook()
