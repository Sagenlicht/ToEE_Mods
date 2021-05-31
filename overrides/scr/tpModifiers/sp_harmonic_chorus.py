from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Harmonic Chorus"

def harmonicChorusSpellBonusToDc(attachee, args, evt_obj):
    evt_obj.bonus_list.add(2,13,"~Harmonic Chorus~[TAG_SPELLS_HARMONIC_CHORUS] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #Harmonic Chorus is a +2 morale bouns to caster level and spell dc
    return 0

def harmonicChorusSpellBonusToCasterLevel(attachee, args, evt_obj):
    evt_obj.return_val += 2
    return 0

harmonicChorusSpell = PythonModifier("sp-Harmonic Chorus", 2) # spell_id, duration
harmonicChorusSpell.AddHook(ET_OnGetCasterLevelMod, EK_NONE, harmonicChorusSpellBonusToCasterLevel, ())
harmonicChorusSpell.AddHook(ET_OnGetSpellDcMod , EK_NONE, harmonicChorusSpellBonusToDc,())
harmonicChorusSpell.AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addConcentration, ())
harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Concentration_Broken, spell_utils.checkRemoveSpell, ())
#harmonicChorusSpell.AddHook(ET_OnConditionAdd, EK_NONE, spell_utils.addDimiss, ())
#harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Dismiss_Spells, spell_utils.checkRemoveSpell, ())
harmonicChorusSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
harmonicChorusSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
harmonicChorusSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
harmonicChorusSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
harmonicChorusSpell.AddSpellDispelCheckStandard()
harmonicChorusSpell.AddSpellTeleportPrepareStandard()
harmonicChorusSpell.AddSpellTeleportReconnectStandard()
harmonicChorusSpell.AddSpellCountdownStandardHook()
#harmonicChorusSpell.AddSpellDismissStandardHook()


