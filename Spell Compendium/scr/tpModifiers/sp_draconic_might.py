from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Draconic Might"

def draconicMightSpellAbilityBonus(attachee, args, evt_obj):
    bonusValue = 4 #Draconic Might adds a +4 Enhancement Bonus to Charisma and Constitution and Strength
    bonusType = 12 #ID 12 = Enhancement
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Draconic Might~[TAG_SPELLS_DRACONIC_MIGHT]")
    return 0

def draconicMightSpellArmorBonus(attachee, args, evt_obj):
    bonusValue = 4 #Draconic Might adds a +4 Enhancement Bonus to Natural Armor
    bonusType = 10 #ID 10 = Enhancement Bonus for Natural Armor
    evt_obj.bonus_list.add(bonusValue, bonusType, "Natural Armor : ~Draconic Might~[TAG_SPELLS_DRACONIC_MIGHT]")
    return 0

def sleepParalyzeImmunity(attachee, args, evt_obj):
    if evt_obj.is_modifier("sp-Sleep"):
        evt_obj.return_val = 0
        combatMesLine = 5059 #ID 5059: "Sleep Immunity"
        historyMesLine = 31 #ID 31: {[ACTOR] is immune to ~sleep~[TAG_SPELLS_SLEEP].}
        attachee.float_mesfile_line('mes\\combat.mes', combatMesLine, tf_red)
        game.create_history_from_pattern(historyMesLine, attachee, OBJ_HANDLE_NULL)
    elif evt_obj.is_modifier("Paralyzed"):
        evt_obj.return_val = 0
        attachee.float_text_line("Paralyze Immunity", tf_red)
        game.create_history_freeform("{} is immune to ~paralyze~[TAG_PARALYZED] effects\n\n".format(attachee.description))
    return 0

draconicMightSpell = PythonModifier("sp-Draconic Might", 3) # spell_id, duration, empty
draconicMightSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_CHARISMA, draconicMightSpellAbilityBonus, ())
draconicMightSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_CONSTITUTION, draconicMightSpellAbilityBonus, ())
draconicMightSpell.AddHook(ET_OnAbilityScoreLevel, EK_STAT_STRENGTH, draconicMightSpellAbilityBonus, ())
draconicMightSpell.AddHook(ET_OnGetAC, EK_NONE, draconicMightSpellArmorBonus, ())
draconicMightSpell.AddHook(ET_OnConditionAddPre, EK_NONE, sleepParalyzeImmunity, ())
draconicMightSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
draconicMightSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
draconicMightSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
draconicMightSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
draconicMightSpell.AddSpellDispelCheckStandard()
draconicMightSpell.AddSpellTeleportPrepareStandard()
draconicMightSpell.AddSpellTeleportReconnectStandard()
draconicMightSpell.AddSpellCountdownStandardHook()
