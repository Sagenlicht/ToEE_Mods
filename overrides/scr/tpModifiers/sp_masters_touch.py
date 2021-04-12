from templeplus.pymod import PythonModifier
from toee import *
import tpdp
from utilities import *
print "Registering sp-Masters Touch"

def mastersTouchSpellNullifyProficiencyPenalty(attachee, args, evt_obj):
    if not args.get_arg(2) == 0:
        weaponUsedForAttack = evt_obj.attack_packet.get_weapon_used()
        if args.get_arg(2) == weaponUsedForAttack.obj_get_int(obj_f_weapon_type): #check if weapon is still the weapon type Masters Gift was used for
            evt_obj.bonus_list.add(4, 0, "~Masters Gift~[TAG_SPELLS_MASTERS_GIFT] Weapon Proficiency") #Generic stacking bonus to counteract the Proficiency Penalty
    else:
        if not attachee.item_worn_at(item_wear_shield).obj_get_int(obj_f_armor_armor_check_penalty) == OBJ_HANDLE_NULL: #check if shield is still equipped
            wornShieldArmorCheckPenalty = attachee.item_worn_at(item_wear_shield).obj_get_int(obj_f_armor_armor_check_penalty) # Get Armor Check Penalty
            evt_obj.bonus_list.add(abs(wornShieldArmorCheckPenalty), 0, "~Masters Gift~[TAG_SPELLS_MASTERS_GIFT] Shield Proficiency") #Generic stacking bonus to counteract the Proficiency Penalty
    return 0

def mastersTouchSpellTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append("Masters Touch (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append("Masters Touch (" + str(args.get_arg(1)) + " rounds)")
    return 0

def mastersTouchSpellEffectTooltip(attachee, args, evt_obj):
    if args.get_arg(1) == 1:
        evt_obj.append(tpdp.hash("MASTERS_TOUCH"), -2, " (" + str(args.get_arg(1)) + " round)")
    else:
        evt_obj.append(tpdp.hash("MASTERS_TOUCH"), -2, " (" + str(args.get_arg(1)) + " rounds)")
    return 0

def mastersTouchSpellHasSpellActive(attachee, args, evt_obj):
    spellPacket = tpdp.SpellPacket(args.get_arg(0))
    if evt_obj.data1 == spellPacket.spell_enum:
        evt_obj.return_val = 1
    return 0

def mastersTouchSpellKilled(attachee, args, evt_obj):
    args.remove_spell()
    args.remove_spell_mod()
    return 0

def mastersTouchSpellSpellEnd(attachee, args, evt_obj):
    print "Masters TouchSpellEnd"
    return 0

mastersTouchSpell = PythonModifier("sp-Masters Touch", 3) # spell_id, duration, wornItemType
mastersTouchSpell.AddHook(ET_OnToHitBonus2, EK_NONE, mastersTouchSpellNullifyProficiencyPenalty,())
mastersTouchSpell.AddHook(ET_OnGetTooltip, EK_NONE, mastersTouchSpellTooltip, ())
mastersTouchSpell.AddHook(ET_OnGetEffectTooltip, EK_NONE, mastersTouchSpellEffectTooltip, ())
mastersTouchSpell.AddHook(ET_OnD20Signal, EK_S_Spell_End, mastersTouchSpellSpellEnd, ())
mastersTouchSpell.AddHook(ET_OnD20Query, EK_Q_Critter_Has_Spell_Active, mastersTouchSpellHasSpellActive, ())
mastersTouchSpell.AddHook(ET_OnD20Signal, EK_S_Killed, mastersTouchSpellKilled, ())
mastersTouchSpell.AddSpellDispelCheckStandard()
mastersTouchSpell.AddSpellTeleportPrepareStandard()
mastersTouchSpell.AddSpellTeleportReconnectStandard()
mastersTouchSpell.AddSpellCountdownStandardHook()
