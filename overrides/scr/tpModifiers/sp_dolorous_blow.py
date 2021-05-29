from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Dolorous Blow"

def dolorousBlowSpellChainToWeapon(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Dolorous Blow Weapon Condition', args.get_arg(1))
    return 0

def dolorousBlowSpellModifyThreatRange(attachee, args, evt_obj):
    appliedKeenRange =  evt_obj.bonus_list.get_sum()
    weaponUsed = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = weaponUsed.d20_query("Q_Has_Dolorous_Blow_Weapon_Effect")
    if isEnchantedWeapon:
      weaponKeenRange = weaponUsed.obj_get_int(obj_f_weapon_crit_range)
      evt_obj.bonus_list.add(weaponKeenRange, 12, "~Dolorous Blow~[TAG_SPELLS_DOLORUS_BLOW] Bonus")
    return 0

def dolorousBlowSpellAnswerToKeenQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def dolorousBlowSpellAutoConfirmCrit(attachee, args, evt_obj):
    weaponUsed = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = weaponUsed.d20_query("Q_Has_Dolorous_Blow_Weapon_Effect")
    if isEnchantedWeapon:
        evt_obj.return_val = 1
    return 0

def dolorousBlowSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Dolorous_Blow_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append("Dolorous Blow ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Dolorous Blow ({} rounds)".format(args.get_arg(1)))

def dolorousBlowSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Dolorous_Blow_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("DOLOROUS_BLOW"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("DOLOROUS_BLOW"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def dolorousBlowSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def dolorousBlowSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def dolorousBlowSpellSpellEnd(attachee, args, evt_obj):
    print "Dolorous BlowSpellEnd"
    return 0

dolorousBlowSpell = PythonModifier("sp-Dolorous Blow", 2) # spell_id, duration
dolorousBlowSpell.AddHook(ET_OnConditionAdd, EK_NONE, dolorousBlowSpellChainToWeapon,())
dolorousBlowSpell.AddHook(ET_OnD20PythonQuery, "Always Confirm Criticals", dolorousBlowSpellAutoConfirmCrit,())
dolorousBlowSpell.AddHook(ET_OnGetCriticalHitRange, EK_NONE, dolorousBlowSpellModifyThreatRange,())
dolorousBlowSpell.AddHook(ET_OnD20Query, EK_Q_Item_Has_Keen_Bonus, dolorousBlowSpellAnswerToKeenQuery, ())
dolorousBlowSpell.AddHook(ET_OnGetTooltip, EK_NONE, dolorousBlowSpellTooltip, ())
dolorousBlowSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, dolorousBlowSpellEffectTooltip, ())
dolorousBlowSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, dolorousBlowSpellSpellEnd, ())
dolorousBlowSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, dolorousBlowSpellHasSpellActive, ())
dolorousBlowSpell.AddHook(ET_OnD20Signal, EK_S_Killed, dolorousBlowSpellKilled, ())
dolorousBlowSpell.AddSpellDispelCheckStandard()
dolorousBlowSpell.AddSpellTeleportPrepareStandard()
dolorousBlowSpell.AddSpellTeleportReconnectStandard()
dolorousBlowSpell.AddSpellCountdownStandardHook()

###### Dolorous Blow Weapon Condition ######
def dolorousBlowWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 1

def dolorousBlowWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def dolorousBlowWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

dolorousBlowWeaponCondition = PythonModifier("Dolorous Blow Weapon Condition", 1) # duration
dolorousBlowWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, dolorousBlowWeaponConditionGlowEffect, ())
dolorousBlowWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Dolorous_Blow_Weapon_Effect", dolorousBlowWeaponConditionEffectAnswerToQuery, ())
dolorousBlowWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, dolorousBlowWeaponConditionTickdown, ())
