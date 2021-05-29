from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Conviction"

def convictionSpellBonusToSaves(attachee, args, evt_obj):
    evt_obj.bonus_list.add(args.get_arg(2), 13, "~Conviction~[TAG_SPELLS_CONVICTION] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #Bonus is passed by spell
    return 0

convictionSpell = PythonModifier("sp-Conviction", 3) # spell_id, duration, spellBonus
convictionSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, convictionSpellBonusToSaves, ())
convictionSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
convictionSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
convictionSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
convictionSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
convictionSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
convictionSpell.AddSpellDispelCheckStandard()
convictionSpell.AddSpellTeleportPrepareStandard()
convictionSpell.AddSpellTeleportReconnectStandard()
convictionSpell.AddSpellCountdownStandardHook()
