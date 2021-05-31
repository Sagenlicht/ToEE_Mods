from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Clear Mind"

def clearMindSpellBonusToMindAffecting(attachee, args, evt_obj):
    if evt_obj.flags & 0x8000000: #according to d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_MIND_AFFECTING = 28,  // 0x8000000;
        attachee.float_text_line("Clear Mind")
        bonusValue = 4 #Clear Mind adds a +4 Sacred Bonus vs Mind-Affecting spells
        bonusType = 153 #ID 153 = Sacred
        evt_obj.bonus_list.add(bonusValue, bonusType, "~Clear Mind~[TAG_SPELLS_CLEAR_MIND] ~Sacred~[TAG_MODIFIER_SACRED] Bonus")
    return 0

clearMindSpell = PythonModifier("sp-Clear Mind", 2) # spell_id, duration
clearMindSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, clearMindSpellBonusToMindAffecting,())
clearMindSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
clearMindSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
clearMindSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
clearMindSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
clearMindSpell.AddSpellDispelCheckStandard()
clearMindSpell.AddSpellTeleportPrepareStandard()
clearMindSpell.AddSpellTeleportReconnectStandard()
clearMindSpell.AddSpellCountdownStandardHook()
