from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Aid Mass"

def aidMassSpellBonusToHit(attachee, args, evt_obj):
    evt_obj.bonus_list.add(1, 13,"~Morale~[TAG_MODIFIER_MORALE] : ~Aid, Mass~[TAG_SPELLS_AID_MASS]") #ID 13 = Morale
    return 0

def aidMassSpellSaveBonus(attachee, args, evt_obj):
    if evt_obj.flags & 0x100000: #d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_FEAR = 21, // 0x100000
        evt_obj.bonus_list.add(1, 13,"~Morale~[TAG_MODIFIER_MORALE] : ~Aid, Mass~[TAG_SPELLS_AID_MASS]") #ID 13 = Morale
    return 0

aidMassSpell = PythonModifier("sp-Aid Mass", 2) # spell_id, duration
aidMassSpell.AddHook(ET_OnToHitBonus2, EK_NONE, aidMassSpellBonusToHit, ())
aidMassSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, aidMassSpellSaveBonus, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Temporary_Hit_Points_Removed, spell_utils.removeTempHp, ())
aidMassSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
aidMassSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
aidMassSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
aidMassSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
aidMassSpell.AddSpellDispelCheckStandard()
aidMassSpell.AddSpellTeleportPrepareStandard()
aidMassSpell.AddSpellTeleportReconnectStandard()
aidMassSpell.AddSpellCountdownStandardHook()
