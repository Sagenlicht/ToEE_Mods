from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Blessed Aim"

def blessedAimSpellBonus(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED:
        evt_obj.bonus_list.add(2, 21, "~Blessed Aim~[TAG_SPELLS_BLESSED_AIM] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #Blessed Aim adds a +2 Morale Bonus to Ranged Attack Rolls
    return 0

blessedAimSpell = PythonModifier("sp-Blessed Aim", 2) # spell_id, duration
blessedAimSpell.AddHook(ET_OnToHitBonus2, EK_NONE, blessedAimSpellBonus,())
blessedAimSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
blessedAimSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
blessedAimSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spell_utils.spellEnd, ())
blessedAimSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
blessedAimSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
blessedAimSpell.AddSpellDispelCheckStandard()
blessedAimSpell.AddSpellTeleportPrepareStandard()
blessedAimSpell.AddSpellTeleportReconnectStandard()
blessedAimSpell.AddSpellCountdownStandardHook()
