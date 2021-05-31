from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Ironguts"

def irongutsSpellBonusToPoisonSaves(attachee, args, evt_obj):
    if evt_obj.flags & 0x8: #according to d20_defs.h D20STD_F_POISON = 4, // 0x8; so I do use 8 and not D20STD_F_POISON as it returns 4 and is not working
        bonusValue = 5 # Ironguts adds a +5 Alchemical Bonus to Fortitude Saves vs. poison
        bonusType = 151 #ID 151 = Alchemical
        evt_obj.bonus_list.add(bonusValue, bonusType,"~Ironguts~[TAG_SPELLS_IRONGUTS] ~Alchemical~[TAG_MODIFIER_ALCHEMICAL] Bonus")
    return 0

def irongutsSpellSpellEnd(attachee, args, evt_obj):
    attachee.condition_add('Nauseated Condition', 1) #When spell expires target is nauseated for 1 round
    return 0

irongutsSpell = PythonModifier("sp-Ironguts", 2) # spell_id, duration
irongutsSpell.AddHook(ET_OnSaveThrowLevel, EK_SAVE_FORTITUDE, irongutsSpellBonusToPoisonSaves,())
#irongutsSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, irongutsSpellSpellEnd, ()) deactivated for now, until nauseated condition is finalized
irongutsSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
irongutsSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
irongutsSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
irongutsSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
irongutsSpell.AddSpellDispelCheckStandard()
irongutsSpell.AddSpellTeleportPrepareStandard()
irongutsSpell.AddSpellTeleportReconnectStandard()
irongutsSpell.AddSpellCountdownStandardHook()
