from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Checkmates Light"

def checkmatesLightOnConditionAddActions(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    radiusCheckmatesLight = (20.0 + (attachee.radius / 12.0))
    checkmatesLightId = attachee.object_event_append(OLC_CRITTERS, radiusCheckmatesLight)
    args.set_arg(3, checkmatesLightId)
    attachee.condition_add_with_args('Checkmates Light Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    spellPacket.update_registry()

    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Checkmates Light Weapon Condition', args.get_arg(1))
    return 0

def checkmatesLightSpellOnEntered(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellTarget = evt_obj.target
    checkmatesLightId = args.get_arg(3)

    if checkmatesLightId != evt_obj.evt_id:
        print "ID Mismatch: Returned ID: {}, expected ID: {}".format(args.get_arg(3), evt_obj.evt_id)
        return 0

    if spellPacket.add_target(spellTarget, 0):
        print "Added: ", spellTarget
        spellTarget.condition_add_with_args('Checkmates Light Effect', args.get_arg(0), args.get_arg(1), args.get_arg(2), args.get_arg(3))
    return 0

def checkmatesLightSpellBonusToHit(attachee, args, evt_obj):
    weaponUsed = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = weaponUsed.d20_query("Q_Has_Checkmates_Light_Weapon_Effect")
    if isEnchantedWeapon:
        evt_obj.bonus_list.add(args.get_arg(2), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Checkmates Light~[TAG_SPELLS_CHECKMATES_LIGHT]")
    return 0

def checkmatesLightSpellAddLawfulDamageType(attachee, args, evt_obj):
    weaponUsed = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = weaponUsed.d20_query("Q_Has_Checkmates_Light_Weapon_Effect")
    if isEnchantedWeapon:
        if not evt_obj.damage_packet.attack_power & D20DAP_LAW:
            evt_obj.damage_packet.attack_power |= D20DAP_LAW
        evt_obj.damage_packet.bonus_list.add(args.get_arg(2), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Checkmates Light~[TAG_SPELLS_CHECKMATES_LIGHT]")
    return 0

def checkmatesLightSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def checkmatesLightSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def checkmatesLightSpellSpellEnd(attachee, args, evt_obj):
    print "Checkmates Light SpellEnd"
    return 0

checkmatesLightSpell = PythonModifier("sp-Checkmates Light", 4) # spell_id, duration, spellBonus, eventId
checkmatesLightSpell.AddHook(ET_OnConditionAdd, EK_NONE, checkmatesLightOnConditionAddActions,())
checkmatesLightSpell.AddHook(ET_OnToHitBonus2, EK_NONE, checkmatesLightSpellBonusToHit,())
checkmatesLightSpell.AddHook(ET_OnDealingDamage, EK_NONE, checkmatesLightSpellAddLawfulDamageType,())
checkmatesLightSpell.AddHook(ET_OnObjectEvent, EK_OnEnterAoE, checkmatesLightSpellOnEntered, ())
checkmatesLightSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, checkmatesLightSpellSpellEnd, ())
checkmatesLightSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, checkmatesLightSpellHasSpellActive, ())
checkmatesLightSpell.AddHook(ET_OnD20Signal, EK_S_Killed, checkmatesLightSpellKilled, ())
checkmatesLightSpell.AddSpellDispelCheckStandard()
checkmatesLightSpell.AddSpellTeleportPrepareStandard()
checkmatesLightSpell.AddSpellTeleportReconnectStandard()
checkmatesLightSpell.AddSpellCountdownStandardHook()

### Start Checkmates Light Effect ###

def checkmatesLightEffectSaveBonus(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if spellPacket.get_target(1) == spellPacket.caster.item_worn_at(item_wear_weapon_primary):
        if evt_obj.flags & 0x100000: #d20_defs.h: D20STD_F_SPELL_DESCRIPTOR_FEAR = 21, // 0x100000
            #Checkmates Light grants a +1 morale bonus saves vs. fear
            evt_obj.bonus_list.add(1, 13, "~Checkmates Light~[TAG_SPELLS_CHECKMATES_LIGHT] ~Morale~[TAG_MODIFIER_MORALE] Bonus") #13 = Morale; Bonus is passed from spell(arg3)
    return 0

def checkmatesLightEffectBeginRound(attachee, args, evt_obj):
    args.set_arg(1, args.get_arg(1)-evt_obj.data1) # Ticking down duration
    if args.get_arg(1) < 0:
        args.condition_remove()
    return 0

def checkmatesLightEffectTooltip(attachee, args, evt_obj):
    weaponWornByCaster = spellPacket.caster.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = weaponWornByCaster.d20_query("Q_Has_Checkmates_Light_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0
    
    if args.get_arg(1) == 1:
        evt_obj.append("Checkmates Light ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Checkmates Light ({} rounds)".format(args.get_arg(1)))
    return 0

def checkmatesLightEffectEffectTooltip(attachee, args, evt_obj):
    weaponWornByCaster = spellPacket.caster.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = weaponWornByCaster.d20_query("Q_Has_Checkmates_Light_Weapon_Effect")
    if not isEnchantedWeapon:
        return 0

    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CHECKMATES_LIGHT"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CHECKMATES_LIGHT"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def checkmatesLightEffectSpellKilled(attachee, args, evt_obj):
    args.condition_remove()
    return 0

def checkmatesLightEffectOnLeaveAoE(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    checkmatesLightId = args.get_arg(3)
    if checkmatesLightId != evt_obj.evt_id:
        print "ID Mismach Checkmates Light"
        return 0
    args.condition_remove()
    return 0

def checkmatesLightEffectOnRemove(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    spellPacket.remove_target(attachee)
    return 0

checkmatesLightEffect = PythonModifier("Checkmates Light Effect", 4) #spell_id, duration, spellBonus, eventId
checkmatesLightEffect.AddHook(ET_OnSaveThrowLevel, EK_NONE, checkmatesLightEffectSaveBonus, ())
checkmatesLightEffect.AddHook(ET_OnBeginRound, EK_NONE, checkmatesLightEffectBeginRound, ())
checkmatesLightEffect.AddHook(ET_OnGetTooltip, EK_NONE, checkmatesLightEffectTooltip, ())
checkmatesLightEffect.AddHook(ET_OnGetEffectTooltip, EK_NONE, checkmatesLightEffectEffectTooltip, ())
checkmatesLightEffect.AddHook(ET_OnObjectEvent, EK_OnLeaveAoE, checkmatesLightEffectOnLeaveAoE, ())
checkmatesLightEffect.AddHook(ET_OnConditionRemove, EK_NONE, checkmatesLightEffectOnRemove, ())

## End Checkmates Light Effect ###

###### Checkmates Light Weapon Condition ######
def checkmatesLightWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 1

def checkmatesLightWeaponConditionEffectAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def checkmatesLightWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

checkmatesLightWeaponCondition = PythonModifier("Checkmates Light Weapon Condition", 1) # duration
checkmatesLightWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, checkmatesLightWeaponConditionGlowEffect, ())
checkmatesLightWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Checkmates_Light_Weapon_Effect", checkmatesLightWeaponConditionEffectAnswerToQuery, ()) #not tested
checkmatesLightWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, checkmatesLightWeaponConditionTickdown, ())