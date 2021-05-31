from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Curse of Ill Fortune"

def curseOfIllFortuneSpellPenalty(attachee, args, evt_obj):
    bonusValue = -3 #Curse gives -3 on attack rolls, saves, ability checks and skill checks
    bonusType = 0 #ID 0 = Untyped (stacking)
    evt_obj.bonus_list.add(bonusValue, bonusType, "~Curse of Ill Fortune~[TAG_SPELLS_CURSE_OF_ILL_FORTUNE] penalty")
    return 0

def curseOfIllFortuneSpellCheckRemoveBySpell(attachee, args, evt_obj): #not tested what happens if spell gets interrupted
    spellToCheck = tpdp.SpellPacket(evt_obj.data1)
    spellsThatRemoveCurse = [spell_break_enchantment, spell_remove_curse, spell_miracle, spell_wish]
    if spellToCheck.spell_enum in spellsThatRemoveCurse:
        args.remove_spell()
        args.remove_spell_mod()
    return 0

curseOfIllFortuneSpell = PythonModifier("sp-Curse of Ill Fortune", 2) # spell_id, duration
curseOfIllFortuneSpell.AddHook(ET_OnToHitBonus2, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnSaveThrowLevel, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnGetAbilityCheckModifier, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnGetSkillLevel, EK_NONE, curseOfIllFortuneSpellPenalty,())
curseOfIllFortuneSpell.AddHook(ET_OnD20Signal, EK_S_Spell_Cast, curseOfIllFortuneSpellCheckRemoveBySpell, ())
curseOfIllFortuneSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
curseOfIllFortuneSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
curseOfIllFortuneSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
curseOfIllFortuneSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
curseOfIllFortuneSpell.AddSpellDispelCheckStandard()
curseOfIllFortuneSpell.AddSpellTeleportPrepareStandard()
curseOfIllFortuneSpell.AddSpellTeleportReconnectStandard()
curseOfIllFortuneSpell.AddSpellCountdownStandardHook()
