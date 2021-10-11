from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
import spell_utils
print "Registering sp-Masters Touch"

def mastersTouchSpellOnConditionAdd(attachee, args, evt_obj):
    itemType = args.get_arg(2)
    attachee.item_worn_at(itemType).item_condition_add_with_args("Item Masters Touch", args.get_arg(1))
    return 0

def mastersTouchSpellNullifyProficiencyPenalty(attachee, args, evt_obj):
    if not args.get_arg(2) == item_wear_shield:
        weaponUsedForAttack = evt_obj.attack_packet.get_weapon_used()
        if weaponUsedForAttack.item_has_condition("Item Masters Touch"):
            capValue = 0 #Sets cap to 0 to negate penalty
            bonusType = 37 #ID 37 = Weapon Proficiency Penalty
            bonusMesFileId = 2 #ID 2 in bonus mes is "no penalty due to "
            ### negative cap is not working currently
            #evt_obj.bonus_list.add_cap(bonusType, capValue, bonusMesFileId, "~Masters Gift~[TAG_SPELLS_MASTERS_GIFT] Weapon Proficiency")
            #evt_obj.bonus_list.add(1, 37, "Test")

            ### Workaround modify ###
            evt_obj.bonus_list.modify(4, 37, 138)
            ### Workaround modify ###

    else:
        if attachee.item_worn_at(item_wear_shield).item_has_condition("Item Masters Touch"): #check if shield is still equipped
            print "Inside Shield if condition"
            #evt_obj.bonus_list.add(abs(wornShieldArmorCheckPenalty), 0, "~Masters Gift~[TAG_SPELLS_MASTERS_GIFT] Shield Proficiency") #Generic stacking bonus to counteract the Proficiency Penalty
            capValue = 0 #Sets cap to 0 to negate penalty
            bonusType = 37 #ID 37 = Weapon Proficiency Penalty
            bonusMesFileId = 2 #ID 2 in bonus mes is "no penalty due to "
            evt_obj.bonus_list.add_cap(bonusType, capValue, bonusMesFileId, "~Masters Gift~[TAG_SPELLS_MASTERS_GIFT] Shield Proficiency")

            ### Workaround modify ###
            wornShieldArmorCheckPenalty = attachee.item_worn_at(item_wear_shield).obj_get_int(obj_f_armor_armor_check_penalty) # Get Armor Check Penalty
            evt_obj.bonus_list.modify(abs(wornShieldArmorCheckPenalty), 0, 138)
            ### Workaround modify ###
    return 0

mastersTouchSpell = PythonModifier("sp-Masters Touch", 3) # spell_id, duration, itemType
mastersTouchSpell.AddHook(ET_OnConditionAdd, EK_NONE, mastersTouchSpellOnConditionAdd, ())
mastersTouchSpell.AddHook(ET_OnToHitBonus2, EK_NONE, mastersTouchSpellNullifyProficiencyPenalty,())
mastersTouchSpell.AddHook(ET_OnGetTooltip, EK_NONE, spell_utils.spellTooltip, ())
mastersTouchSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, spell_utils.spellEffectTooltip, ())
mastersTouchSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, spell_utils.queryActiveSpell, ())
mastersTouchSpell.AddHook(ET_OnD20Signal, EK_S_Killed, spell_utils.spellKilled, ())
mastersTouchSpell.AddSpellDispelCheckStandard()
mastersTouchSpell.AddSpellTeleportPrepareStandard()
mastersTouchSpell.AddSpellTeleportReconnectStandard()
mastersTouchSpell.AddSpellCountdownStandardHook()

def mastersTouchItemQuery(attachee, args, evt_obj):
    evt_obj.return_val = 1
    return 0

def mastersTouchItemTickDown(attachee, args, evt_obj):
    args.set_arg(0, args.get_arg(0)-evt_obj.data1) # Ticking down duration
    if args.get_arg(0) < 0:
        args.condition_remove()
    return 0

mastersTouchItem = PythonModifier("Item Masters Touch", 1) #duration
mastersTouchItem.AddHook(ET_OnD20PythonQuery, "Q_Item_Has_Masters_Touch", mastersTouchItemQuery, ())
mastersTouchItem.AddHook(ET_OnBeginRound, EK_NONE, mastersTouchItemTickDown, ())
