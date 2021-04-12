from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Critical Strike"

def criticalStrikeSpellModifyThreatRange(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED: #only melee attacks qualify for Critical Strike
        return 0

    if evt_obj.attack_packet.get_weapon_used().obj_get_int(obj_f_type) == obj_t_weapon: #Keen requires weapon
        getWeaponKeenRange = evt_obj.attack_packet.get_weapon_used().obj_get_int(obj_f_weapon_crit_range)
    else:
        return 0

    appliedKeenRange =  evt_obj.bonus_list.get_sum()

    if appliedKeenRange == getWeaponKeenRange:
        evt_obj.bonus_list.add(getWeaponKeenRange, 0 , "~Critical Strike~[TAG_SPELLS_CRITICAL_STRIKE] Bonus")
    return 0

def criticalStrikeSpellBonusToConfirmCrit(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED: #only melee attacks qualify for Critical Strike
        return 0

    evt_obj.bonus_list.add(4, 18,"~Critical Strike~[TAG_SPELLS_CRITICAL_STRIKE] Insight Bonus") #Critical Strike adds a +4 Insight Bonus (18) to Confirm Critical Hits
    return 0

def criticalStrikeSpellBonusToDamage(attachee, args, evt_obj):
    if evt_obj.attack_packet.get_flags() & D20CAF_RANGED: #only melee attacks qualify for Critical Strike
        return 0

    targetToHit =  evt_obj.attack_packet.target

    #Check if opponent is immnue to precision damage
    targetRacialImmunity = False
    immunityList = [mc_type_construct, mc_type_ooze, mc_type_plant, mc_type_undead]
    for critterType in immunityList:
        if targetToHit.is_category_type(critterType):
            targetRacialImmunity = True
    if targetToHit.is_category_subtype(mc_subtype_incorporeal):
        targetRacialImmunity = True
    if targetRacialImmunity:
        return 0

    #target needs to be denied its dexterity bonus to AC for whatever reason or be flanked
    if targetToHit.d20_query(Q_Helpless) == 1 or targetToHit.d20_query(Q_Flatfooted) == 1 or (evt_obj.attack_packet.get_flags() & D20CAF_FLANKED):
        bonusDice = dice_new('1d6') #Critical Strike Bonus Damage
        evt_obj.damage_packet.add_dice(bonusDice, D20DT_UNSPECIFIED, 3000) #ID3000 added in damage.mes 
    return 0

def criticalStrikeSpellAnswerToKeenQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def criticalStrikeSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Critical Strike ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append("Critical Strike ({} rounds)".format(args.get_arg(1)))

def criticalStrikeSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("CRITICAL_STRIKE"), -2, " ({} round)".format(args.get_arg(1)))
    else:
        evt_obj.append(tpdp.hash("CRITICAL_STRIKE"), -2, " ({} rounds)".format(args.get_arg(1)))
    return 0

def criticalStrikeSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def criticalStrikeSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def criticalStrikeSpellSpellEnd(attachee, args, evt_obj):
    print "Critical StrikeSpellEnd"
    return 0

criticalStrikeSpell = PythonModifier("sp-Critical Strike", 2) # spell_id, duration
criticalStrikeSpell.AddHook(ET_OnGetCriticalHitRange, EK_NONE, criticalStrikeSpellModifyThreatRange,())
criticalStrikeSpell.AddHook(ET_OnConfirmCriticalBonus, EK_NONE, criticalStrikeSpellBonusToConfirmCrit,())
criticalStrikeSpell.AddHook(ET_OnDealingDamage, EK_NONE, criticalStrikeSpellBonusToDamage,())
#criticalStrikeSpell.AddHook(ET_OnD20Query, EK_Q_Item_Has_Keen_Bonus , criticalStrikeSpellAnswerToKeenQuery, ())
criticalStrikeSpell.AddHook(ET_OnGetTooltip, EK_NONE, criticalStrikeSpellTooltip, ())
criticalStrikeSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, criticalStrikeSpellEffectTooltip, ())
criticalStrikeSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, criticalStrikeSpellSpellEnd, ())
criticalStrikeSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, criticalStrikeSpellHasSpellActive, ())
criticalStrikeSpell.AddHook(ET_OnD20Signal, EK_S_Killed, criticalStrikeSpellKilled, ())
criticalStrikeSpell.AddSpellDispelCheckStandard()
criticalStrikeSpell.AddSpellTeleportPrepareStandard()
criticalStrikeSpell.AddSpellTeleportReconnectStandard()
criticalStrikeSpell.AddSpellCountdownStandardHook()
