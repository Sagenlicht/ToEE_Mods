from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Rhinos Rush"

def rhinosRushSpellBonusToDamage(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_CHARGE:
        if not evt_obj.attack_packet.get_flags() & D20CAF_CRITICAL:
            evt_obj.damage_packet.critical_multiplier_apply(2) #this doubles the normal weapon damage
    return 0

def rhinosRushSpellModifyCritMulitplier(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_CHARGE:
        bonusValue = 1 #Rhinos Rush deals double damage on non critical hits, but only hightens the multiplier by 1 if it's actually a critical hit!
        bonusType = 0 #Untyped (stacking!)
        evt_obj.bonus_list.add(bonusValue ,bonusType ,"~Rhinos Rush~[TAG_SPELLS_RHINOS_RUSH] Bonus to Crit Multiplier")
    return 0

rhinosRushSpell = PythonModifier("sp-Rhinos Rush", 3) # spell_id, duration, empty
rhinosRushSpell.AddHook(ET_OnDealingDamage, EK_NONE, rhinosRushSpellBonusToDamage,())
rhinosRushSpell.AddHook(ET_OnGetCriticalHitExtraDice, EK_NONE, rhinosRushSpellModifyCritMulitplier,())
rhinosRushSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
rhinosRushSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
rhinosRushSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
rhinosRushSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
rhinosRushSpell.AddSpellDispelCheckStandard()
rhinosRushSpell.AddSpellTeleportPrepareStandard()
rhinosRushSpell.AddSpellTeleportReconnectStandard()
rhinosRushSpell.AddSpellCountdownStandardHook()
