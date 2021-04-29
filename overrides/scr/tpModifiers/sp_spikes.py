from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Spikes"

def spikesSpellChainToWeapon(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    mainhandWeapon.d20_status_init()
    mainhandWeapon.condition_add_with_args('Spikes Weapon Condition', args.get_arg(1))
    return 0

def spikesSpellToHitBonus(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Spikes_Weapon_Effect")
    if isEnchantedWeapon:
        evt_obj.bonus_list.add(2, 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Spikes~[TAG_SPELLS_SPIKES]")
    return 0

def spikesSpellBonusToDamage(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Spikes_Weapon_Effect")
    if isEnchantedWeapon:
        usedWeaponDamageType = usedWeapon.obj_get_int(obj_f_weapon_attacktype)
        if not usedWeaponDamageType == D20DT_BLUDGEONING_AND_PIERCING:
            if not usedWeaponDamageType == D20DT_BLUDGEONING:
                evt_obj.damage_packet.attack_power |= D20DAP_BLUDGEONING
            if not usedWeaponDamageType == D20DT_PIERCING:
                evt_obj.damage_packet.attack_power |= D20DAP_PIERCING
        if not evt_obj.damage_packet.attack_power & D20DAP_MAGIC:
            evt_obj.damage_packet.attack_power |= D20DAP_MAGIC
        evt_obj.damage_packet.bonus_list.add(args.get_arg(2), 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Spikes~[TAG_SPELLS_SPIKES]")
    return 0

def spikesSpellModifyCritRange(attachee, args, evt_obj):
    usedWeapon = evt_obj.attack_packet.get_weapon_used()
    isEnchantedWeapon = usedWeapon.d20_query("Q_Has_Spikes_Weapon_Effect")
    if isEnchantedWeapon:
        weaponKeenRange = usedWeapon.obj_get_int(obj_f_weapon_crit_range)
        evt_obj.bonus_list.add(weaponKeenRange, 12, "~Enhancement~[TAG_ENHANCEMENT_BONUS] : ~Spikes~[TAG_SPELLS_SPIKES]")
    return 0

def spikesSpellTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Spikes_Weapon_Effect")
    if isEnchantedWeapon:
        if args.get_arg(1) == 1:
            evt_obj.append("Spikes ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append("Spikes ({} rounds)".format(args.get_arg(1)))
    return 0

def spikesSpellEffectTooltip(attachee, args, evt_obj):
    mainhandWeapon = attachee.item_worn_at(item_wear_weapon_primary)
    isEnchantedWeapon = mainhandWeapon.d20_query("Q_Has_Spikes_Weapon_Effect")
    if isEnchantedWeapon:
        if args.get_arg(1) == 1:
            evt_obj.append(tpdp.hash("SPIKES"), -2, " ({} round)".format(args.get_arg(1)))
        else:
            evt_obj.append(tpdp.hash("SPIKES"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def spikesSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def spikesSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def spikesSpellSpellEnd(attachee, args, evt_obj):
    print "Spikes SpellEnd"
    return 0

spikesSpell = PythonModifier("sp-Spikes", 3) # spell_id, duration, bonusDamage
spikesSpell.AddHook(ET_OnConditionAdd, EK_NONE, spikesSpellChainToWeapon, ())
spikesSpell.AddHook(ET_OnToHitBonus2, EK_NONE, spikesSpellToHitBonus, ())
spikesSpell.AddHook(ET_OnDealingDamage, EK_NONE, spikesSpellBonusToDamage, ())
spikesSpell.AddHook(ET_OnGetCriticalHitRange, EK_NONE, spikesSpellModifyCritRange, ())
spikesSpell.AddHook(ET_OnGetTooltip, EK_NONE, spikesSpellTooltip, ())
spikesSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spikesSpellEffectTooltip, ())
spikesSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, spikesSpellSpellEnd, ())
spikesSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spikesSpellHasSpellActive, ())
spikesSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spikesSpellKilled, ())
spikesSpell.AddSpellDispelCheckStandard()
spikesSpell.AddSpellTeleportPrepareStandard()
spikesSpell.AddSpellTeleportReconnectStandard()
spikesSpell.AddSpellCountdownStandardHook()

###### Spikes Weapon Condition ######
def spikesWeaponConditionGlowEffect(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def spikesWeaponConditionAnswerToQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def spikesWeaponConditionTickdown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

spikesWeaponCondition = PythonModifier("Spikes Weapon Condition", 1) # duration
spikesWeaponCondition.AddHook(ET_OnWeaponGlowType, EK_NONE, spikesWeaponConditionGlowEffect, ())
spikesWeaponCondition.AddHook(ET_OnD20PythonQuery, "Q_Has_Spikes_Weapon_Effect", spikesWeaponConditionAnswerToQuery, ())
spikesWeaponCondition.AddHook(ET_OnBeginRound , EK_NONE, spikesWeaponConditionTickdown, ())
