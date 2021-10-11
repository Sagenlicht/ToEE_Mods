from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Distract Assailant"

def distractAssailantSpellSetFlankedCondition(attachee, args, evt_obj):
    attachee.condition_add('Flatfooted')
    return 0

def distractAssailantSpellConditionRemove(attachee, args, evt_obj):
    #There is no way currently to remove the Flatfooted condition I belive
    #As there is no condition_remove
    #This would be important if the spell actually gets dispelled
    if attachee.d20query(Q_Flatfooted) == 1:
        pass
    return 0

#Swift spells with a current round duration do not need a duplicate check
distractAssailantSpell = PythonModifier("sp-Distract Assailant", 3) # spell_id, duration, empty
distractAssailantSpell.AddHook(ET_OnConditionAdd, EK_NONE, distractAssailantSpellSetFlankedCondition,())
distractAssailantSpell.AddHook(ET_OnConditionRemove, EK_NONE, distractAssailantSpellConditionRemove, ())
distractAssailantSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
distractAssailantSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
distractAssailantSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
distractAssailantSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
distractAssailantSpell.AddSpellDispelCheckStandard()
distractAssailantSpell.AddSpellTeleportPrepareStandard()
distractAssailantSpell.AddSpellTeleportReconnectStandard()
distractAssailantSpell.AddSpellCountdownStandardHook()
