from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Distract"

def distractSpellPenaltyToSkills(attachee, args, evt_obj):
    bonusValue = -4 #Distract gives -4 penalty to Concentration, Listen, Search and Spot checks
    bonusType = 0 #ID 0 = Untyped (stacking)
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Distract~[TAG_SPELLS_DISTRACT] penalty")
    return 0

def distractSpellTurnBasedStatusInit(attachee, args, evt_obj):
    if evt_obj.tb_status.hourglass_state > 2:
        attachee.float_text_line("Distracted", tf_red)
        evt_obj.tb_status.hourglass_state = 2 # Limited to a Standard or Move Action only
    return 0

distractSpell = PythonModifier("sp-Distract", 2) # spell_id, duration
distractSpell.AddHook(ET_OnTurnBasedStatusInit, EK_NONE, distractSpellTurnBasedStatusInit, ())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_CONCENTRATION, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_LISTEN, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SEARCH, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetSkillLevel, EK_SKILL_SPOT, distractSpellPenaltyToSkills,())
distractSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
distractSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
distractSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
distractSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
distractSpell.AddSpellDispelCheckStandard()
distractSpell.AddSpellTeleportPrepareStandard()
distractSpell.AddSpellTeleportReconnectStandard()
distractSpell.AddSpellCountdownStandardHook()
