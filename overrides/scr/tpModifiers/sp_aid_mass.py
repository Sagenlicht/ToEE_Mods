from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Aid Mass"

def aidMassSpellOnConditionAdd(attachee, args, evt_obj):
    spell_id = args.get_arg(0)
    duration = args.get_arg(1)
    tempHp = dice_new('1d8')
    tempHp.bonus = min(spell.caster_level, 15)
    tempHpAmount = tempHp.roll()
    attachee.condition_add_with_args('Temporary_Hit_Points', spell_id, duration, tempHpAmount)
    return 0

def aidMassSpellBonusToHit(attachee, args, evt_obj):
    bonusValue = 1
    bonusType = 13 #ID 13 = Morale
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Morale~[TAG_MODIFIER_MORALE] : ~Aid, Mass~[TAG_SPELLS_AID_MASS]")
    return 0

def aidMassSpellSaveBonus(attachee, args, evt_obj):
    if evt_obj.flags & 0x100000: #d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_FEAR = 21, // 0x100000
        bonusValue = 1
        bonusType = 13 #ID 13 = Morale
        evt_obj.bonus_list.add(bonusValue, bonusType, "~Morale~[TAG_MODIFIER_MORALE] : ~Aid, Mass~[TAG_SPELLS_AID_MASS]")
    return 0

aidMassSpell = PythonModifier("sp-Aid Mass", 3, False) # spell_id, duration, empty
aidMassSpell.AddHook(ET_OnConditionAdd, EK_NONE, aidMassSpellOnConditionAdd, ())
aidMassSpell.AddHook(ET_OnToHitBonus2, EK_NONE, aidMassSpellBonusToHit, ())
aidMassSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, aidMassSpellSaveBonus, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, spell_utils.removeTempHp, ())
aidMassSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
aidMassSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
aidMassSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
aidMassSpell.AddSpellDispelCheckStandard()
aidMassSpell.AddSpellTeleportPrepareStandard()
aidMassSpell.AddSpellTeleportReconnectStandard()
aidMassSpell.AddSpellCountdownStandardHook()
